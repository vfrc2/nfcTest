import enum
from nfc.libnfc_wraper import *


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
    
    def sendApdu(self, cla: bytes, ins: bytes, p1: bytes, p2: bytes, data: bytes = None, resLen: bytes = None):
        cmd = bytearray([cla,ins,p1,p2])
        
        dataLen = None
        
        if not data == None:
            dataLen = len(data)
            
        if not dataLen == None:
            cmd.append(dataLen)
        
        cmd.extend(data)
        
        if not resLen == None:
            cmd.append(resLen)
            
        cmd_c = (ctypes.c_uint8 * len(cmd))(*cmd)
        
        cmd_c_p = ctypes.cast(cmd_c, ctypes.POINTER(ctypes.c_uint8))
        
        resCount = libnfc.nfc_target_send_bytes(self._device, cmd_c_p, len(cmd), 0)
        if resCount < 0:
            error = libnfc.nfc_strerror(self._device)
            raise Exception('Error send data to target', error.decode('utf-8'))

        print(f"Send {resCount} of {len(cmd)}")
        
        total_res_len = 2 + (resLen if resLen != None else 0) 
        
        res_c = (ctypes.c_uint8 * total_res_len)()
        res_c_p = ctypes.cast(res_c, ctypes.POINTER(ctypes.c_uint8))
        
        resCount = libnfc.nfc_target_receive_bytes(self._device, res_c_p, total_res_len, 0)
        
        if resCount < 0:
            error = libnfc.nfc_strerror(self._device)
            raise Exception('Error read data from target', error.decode('utf-8'))
        
        print(f"Receive {resCount}: {res_c[0]} {res_c[1]}")
        pass
    
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