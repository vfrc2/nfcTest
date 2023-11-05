import ctypes
import enum

_libnfc = ctypes.CDLL('./deps/libnfc/libnfc.dll')

class _nfc_context(ctypes.Structure):
    __fields__ = []

class _nfc_device(ctypes.Structure):
    __fields__ = []
    
class _nfc_modulation(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("nmt", ctypes.c_uint),
        ("nbr", ctypes.c_uint)
    ]
    
class _nfc_dep_info(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ( "abtNFCID3", ctypes.c_uint8 * 10 ),
        ( "btDID", ctypes.c_uint8 ),
        ( "btBS", ctypes.c_uint8 ),
        ( "btBR", ctypes.c_uint8 ),
        ( "btTO", ctypes.c_uint8 ),
        ( "btPP", ctypes.c_uint8 ),
        ( "abtGB", ctypes.c_uint8 * 48 ),
        ( "szGB", ctypes.c_size_t ),
        ( "ndm", ctypes.c_uint )
    ]

class _nfc_iso14443a_info(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ( "abtAtqa", ctypes.c_uint8 * 2 ),
        ( "btSak", ctypes.c_uint8 ),
        ( "szUidLen", ctypes.c_size_t ),
        ( "abtUid", ctypes.c_uint8 * 10 ),
        ( "szAtsLen", ctypes.c_size_t ),
        ( "abtAts", ctypes.c_uint8 * 254 )
    ]

class _nfc_felica_info(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ( "szLen", ctypes.c_size_t ),
        ( "btResCode", ctypes.c_uint8 ),
        ( "abtId", ctypes.c_uint8 * 8 ),
        ( "abtPad", ctypes.c_uint8 * 8 ),
        ( "abtSysCode", ctypes.c_uint8 * 2 )
    ]

class _nfc_iso14443b_info(ctypes.Structure):
    _pack_ = 1
    _fields_= [
        ( "abtPupi", ctypes.c_uint8, 4 ),
        ( "abtApplicationData", ctypes.c_uint8 * 4 ),
        ( "abtProtocolInfo", ctypes.c_uint8 * 3 ),
        ( "ui8CardIdentifier", ctypes.c_uint8 )
    ]

class _nfc_iso14443bi_info(ctypes.Structure):
    _pack_ = 1
    _fields_ = [ 
        ( "abtDIV", ctypes.c_uint8 * 4 ),
        ( "btVerLog", ctypes.c_uint8 ),
        ( "btConfig", ctypes.c_uint8 ),
        ( "szAtrLen", ctypes.c_size_t ),
        ( "abtAtr", ctypes.c_uint8 * 33 )
    ]

class _nfc_iso14443biclass_info(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ( "abtUID", ctypes.c_uint8 * 8 )
    ]

class _nfc_iso14443b2sr_info(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ( "abtUID", ctypes.c_uint8 * 8 )
    ]

class _nfc_iso14443b2ct_info(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ( "abtUID", ctypes.c_uint8 * 4 ),
        ( "btProdCode", ctypes.c_uint8 ),
        ( "btFabCode", ctypes.c_uint8 )
    ]

class _nfc_jewel_info(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ( "btSensRes", ctypes.c_uint8 * 2 ),
        ( "btId", ctypes.c_uint8 * 4 )
    ]
class _nfc_barcode_info(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ( "szDataLen", ctypes.c_size_t ),
        ( "abtData", ctypes.c_uint8 * 32 )
    ]

class _nfc_target_info(ctypes.Union):
    _pack_ = 1
    _fields_ = [
        ( "nai", _nfc_iso14443a_info ),
        ( "nfi", _nfc_felica_info ),
        ( "nbi", _nfc_iso14443b_info ),
        ( "nii", _nfc_iso14443bi_info ),
        ( "nsi", _nfc_iso14443b2sr_info ),
        ( "nci", _nfc_iso14443b2ct_info ),
        ( "nji", _nfc_jewel_info ),
        ( "ndi", _nfc_dep_info ),
        ( "nti", _nfc_barcode_info ) ,
        ( "nhi", _nfc_iso14443biclass_info )
    ]

class _nfc_target(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("nti", _nfc_target_info ),
        ("nm", _nfc_modulation),
    ]    

_nfc_context_p = ctypes.POINTER(_nfc_context)
_nfc_connstr = ctypes.c_char * 1024
_nfc_device_p = ctypes.POINTER(_nfc_device)

_libnfc.nfc_version.restype = ctypes.c_char_p

_libnfc.nfc_init.argtypes = [ctypes.POINTER(_nfc_context_p)]

_libnfc.nfc_open.argtypes = [_nfc_context_p , ctypes.POINTER(_nfc_connstr)]
_libnfc.nfc_open.restype = _nfc_device_p

_libnfc.nfc_list_devices.argtypes = [_nfc_context_p ,ctypes.POINTER(_nfc_connstr), ctypes.c_int]
_libnfc.nfc_list_devices.restype = ctypes.c_int

_libnfc.nfc_initiator_init.argtypes = [_nfc_device_p]
_libnfc.nfc_initiator_init.restype = ctypes.c_int

_libnfc.nfc_device_get_name.argtypes = [_nfc_device_p]
_libnfc.nfc_device_get_name.restype = ctypes.c_char_p

# NFC_EXPORT int nfc_initiator_poll_target(nfc_device *pnd, const nfc_modulation *pnmTargetTypes, const size_t szTargetTypes, const uint8_t uiPollNr, const uint8_t uiPeriod, nfc_target *pnt);
_libnfc.nfc_initiator_poll_target.argtypes = [_nfc_device_p, ctypes.POINTER(_nfc_modulation), ctypes.c_size_t, ctypes.c_uint8, ctypes.c_uint8, ctypes.POINTER(_nfc_target)]
_libnfc.nfc_initiator_poll_target.restype = ctypes.c_int

_libnfc.nfc_strerror.argtypes = [_nfc_device_p]
_libnfc.nfc_strerror.restype = ctypes.c_char_p

# _libnfc.str_nfc_target.argtypes = [ctypes.par(ctypes.c_char), ctypes.POINTER(_nfc_target)]

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
  
nfc_modulation = (NfcModulations, NfcBaudRate)
  
class NfcManager:
    pass

class NfcDeviceMeta:
    connection_string: str
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

class NfcDevice:
    _manager: NfcManager
    connection_string: str
    _device: _nfc_device_p
    name: str
    pollCount = 20
    pollWait = 2
    
    _modulations: list[nfc_modulation]
    
    def __iter__(self):
        return self
    
    def __next__(self):
        return self.next()
    
    def __init__(self, manager: NfcManager, connection_string: str, modulations: list[nfc_modulation]):
        self._manager = manager
        self.connection_string = connection_string
        self._modulations = modulations
        
        _d = ctypes.POINTER(_nfc_connstr)()
        
        self._device = _libnfc.nfc_open(self._manager._context, _d)
        
        if not self._device:
            raise Exception("Error open nfc device")
        
        if _libnfc.nfc_initiator_init(self._device) < 0:
            raise Exception("Error init nfc device")
        
        self.name = _libnfc.nfc_device_get_name(self._device).decode('utf-8')
        
    def next(self) -> str:
        target = _nfc_target()
        modulations = (_nfc_modulation * len(self._modulations))()
        
        for index, modulation in enumerate(self._modulations):
            nmt, nbr = modulation
            modulations[index].nmt = nmt.value
            modulations[index].nbr = nbr.value
        
        res = _libnfc.nfc_initiator_poll_target(
            self._device, 
            ctypes.pointer(modulations[0]), len(modulations), 
            self.pollCount,
            self.pollWait, 
            ctypes.pointer(target)
        )
        
        if (res < 0):
            error = _libnfc.nfc_strerror(self._device)
            raise Exception('Error poll target', error.decode('utf-8'))
        
        if (res == 0):
            raise Exception('No device found')
        
        strBuf = ctypes.c_char_p()
        
        _libnfc.str_nfc_target(ctypes.pointer(strBuf), ctypes.pointer(target), True)
        
        print(strBuf.value.decode('utf-8'))
        
        return target
        
        
class NfcManager:
    _context = _nfc_context_p()
    _device = _nfc_device_p()
    
    _default_modulations = [
        (NfcModulations.NMT_ISO14443A, NfcBaudRate.NBR_106),
        # (NfcModulations.NMT_ISO14443B, NfcBaudRate.NBR_106),
        # (NfcModulations.NMT_FELICA, NfcBaudRate.NBR_212),
        # (NfcModulations.NMT_FELICA, NfcBaudRate.NBR_424),
        # (NfcModulations.NMT_JEWEL, NfcBaudRate.NBR_106),
        # (NfcModulations.NMT_ISO14443BICLASS, NfcBaudRate.NBR_106),
    ]
    
    @staticmethod
    def version():
        result: bytes = _libnfc.nfc_version()
        return result.decode('utf-8')
    
    @staticmethod
    def list_devices(max_device: int = 10) -> list[str]:
        local_context = _nfc_context_p()
        _libnfc.nfc_init(ctypes.pointer(local_context))
        
        if not local_context:
            raise Exception("Unable to init libnfc")
        
        conn_strs = (_nfc_connstr * max_device)()
        
        count = _libnfc.nfc_list_devices(local_context, ctypes.pointer(conn_strs[0]), max_device)
        
        print(f"Found {count} devices:")
        return [NfcDeviceMeta(dev.value.decode('utf-8')) for dev in conn_strs]
        
    
    def __init__(self):
       self._context = _nfc_context_p()
       _libnfc.nfc_init(ctypes.pointer(self._context))
       
       if not self._context:
           raise Exception("Unable to init libnfc")
        
    def open(self, device = None):
        dev = NfcDevice(self, device, self._default_modulations)
        return dev

