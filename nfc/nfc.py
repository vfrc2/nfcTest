import enum
from nfc.libnfc_wraper import *
from struct import pack, unpack

class NfcModulations(enum.Enum):
  NMT_ISO14443A = 1
  NMT_JEWEL = 2
  NMT_ISO14443B = 3
  NMT_ISO14443BI = 4 # pre-ISO14443B aka ISO/IEC 14443 B' or Type B'
  NMT_ISO14443B2SR = 5 # ISO14443-2B ST SRx
  NMT_ISO14443B2CT = 6 # ISO14443-2B ASK CTx
  NMT_FELICA = 7
  NMT_DEP = 8
  NMT_BARCODE = 9    # Thinfilm NFC Barcode
  NMT_ISO14443BICLASS = 10 # HID iClass 14443B mode
  
class NfcBaudRate(enum.Enum):
  NBR_UNDEFINED = 0
  NBR_106 = 1
  NBR_212 = 2
  NBR_424 = 3
  NBR_847 = 4
  
NfcModulation = (NfcModulations, NfcBaudRate)
  
class NfcTag:
    pass

class NfcDevice:
    _context = nfc_context_p()
    _device: nfc_device_p
        
    _default_modulations = [
        (NfcModulations.NMT_ISO14443A, NfcBaudRate.NBR_106),
        # (NfcModulations.NMT_ISO14443B, NfcBaudRate.NBR_106),
        # (NfcModulations.NMT_FELICA, NfcBaudRate.NBR_212),
        # (NfcModulations.NMT_FELICA, NfcBaudRate.NBR_424),
        # (NfcModulations.NMT_JEWEL, NfcBaudRate.NBR_106),
        # (NfcModulations.NMT_ISO14443BICLASS, NfcBaudRate.NBR_106),
    ]
    _modulations: list[nfc_modulation]
    
    name: str
    connection_string: str
    pollCount = 20
    pollWait = 2
    
    @staticmethod
    def version():
        result: bytes = libnfc.nfc_version()
        return result.decode('utf-8')
    
    @staticmethod
    def list_devices(max_device: int = 10) -> list[str]:
        local_context = nfc_context_p()
        libnfc.nfc_init(ctypes.pointer(local_context))
        
        if not local_context:
            raise Exception("Unable to init libnfc")
        
        conn_strs = (nfc_connstr * max_device)()
        
        count = libnfc.nfc_list_devices(local_context, ctypes.pointer(conn_strs[0]), max_device)
        
        print(f"Found {count} devices:")
        return [dev.value.decode('utf-8') for dev in conn_strs]
    
    def __iter__(self):
        return self
    
    def __next__(self):
        return self.next()
    
    def __init__(self, connection_string: str = None, modulations: list[nfc_modulation] = None):
        self.connection_string = connection_string
        self._modulations = modulations or self._default_modulations
        
        self._context = nfc_context_p()
        libnfc.nfc_init(ctypes.pointer(self._context))
       
        if not self._context:
           raise Exception("Unable to init libnfc")
        
        _d = ctypes.POINTER(nfc_connstr)()
        
        self._device = libnfc.nfc_open(self._context, _d)
        
        if not self._device:
            raise Exception("Error open nfc device")
        
        if libnfc.nfc_initiator_init(self._device) < 0:
            raise Exception("Error init nfc device")
        
        self.name = libnfc.nfc_device_get_name(self._device).decode('utf-8')
    
    def sendApdu(self, cla: bytes, ins: bytes, p1: bytes, p2: bytes, data: bytes = None, mrl=0):
        apdu = bytearray([cla, ins, p1, p2])

        # if not self._extended_length_support:
        if data and len(data) > 255:
            raise ValueError("unsupported command data length")
        if mrl and mrl > 256:
            raise ValueError("unsupported max response length")
        if data:
            apdu += pack('>B', len(data)) + bytes(data)
        if mrl > 0:
            apdu += pack('>B', 0 if mrl == 256 else mrl)
        
        cdata = (ctypes.c_char * len(apdu))(*apdu)
        
        cdata_p = ctypes.cast(cdata, ctypes.POINTER(ctypes.c_char))
        crecieve = (ctypes.c_char * 6)()
        crecieve_p = ctypes.cast(crecieve, ctypes.POINTER(ctypes.c_char))
        
        recCount = libnfc.nfc_initiator_transceive_bytes(self._device, 
                                                       cdata_p, len(apdu),
                                                       crecieve_p, 6,
                                                       0)        

        apdu = bytes(crecieve)

        if not apdu or len(apdu) < 2:
            raise Exception('PROTOCOL_ERROR')

        if apdu[-2:] != b"\x90\x00":
            return False

        return True

    
    def next(self) -> NfcTag:
        target = nfc_target()
        modulations = (nfc_modulation * len(self._modulations))()
        
        for index, modulation in enumerate(self._modulations):
            nmt, nbr = modulation
            modulations[index].nmt = nmt.value
            modulations[index].nbr = nbr.value
        
        res = libnfc.nfc_initiator_poll_target(
            self._device, 
            ctypes.pointer(modulations[0]), len(modulations), 
            self.pollCount,
            self.pollWait, 
            ctypes.pointer(target)
        )
        
        if (res < 0):
            error = libnfc.nfc_strerror(self._device)
            raise Exception('Error poll target', error.decode('utf-8'))
        
        if (res == 0):
            raise Exception('No device found')
        
        return NfcTag(self, target)
        
class NfcTag:
    _target = nfc_target()
    _device = NfcDevice
    
    type: str
    info: str
    
    uid: str
    
    def _to_hex_str(self, data):
        return ''.join('{:02x}'.format(x) for x in data)
    
    def __init__(self, device: NfcDevice, target: nfc_target):
        self._target = target
        self._device = device
        
        strBuf = ctypes.c_char_p()
        
        libnfc.str_nfc_target(ctypes.pointer(strBuf), ctypes.pointer(target), True)\
        
        self.info = strBuf.value.decode('utf-8')
        
        if (target.nm.nmt == 1):
            self.type = NfcModulations.NMT_ISO14443A
            self.uid = self._to_hex_str(target.nti.nai.abtUid)
    
    # |   cla   |   ins   |   p1    |   p2    |   LC           |   data    |   LE           |
    # |  1 byte |  1 byte |  1 byte |  1 byte |  0,1 or 3 byte |  LC bytes |  0,1 or 3 byte |
    def sendApdu(self, *args):
        self._device.sendApdu(*args)