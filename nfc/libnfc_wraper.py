import sys
import ctypes

libnfc: ctypes.CDLL

if sys.platform == 'win32':
    libnfc = ctypes.CDLL('./deps/libnfc/libnfc.dll')
else:
    libnfc = ctypes.CDLL('libnfc')

class nfc_context(ctypes.Structure):
    __fields__ = []

class nfc_device(ctypes.Structure):
    __fields__ = []
    
class nfc_modulation(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("nmt", ctypes.c_uint),
        ("nbr", ctypes.c_uint)
    ]
    
class nfc_dep_info(ctypes.Structure):
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

class nfc_iso14443a_info(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ( "abtAtqa", ctypes.c_uint8 * 2 ),
        ( "btSak", ctypes.c_uint8 ),
        ( "szUidLen", ctypes.c_size_t ),
        ( "abtUid", ctypes.c_uint8 * 10 ),
        ( "szAtsLen", ctypes.c_size_t ),
        ( "abtAts", ctypes.c_uint8 * 254 )
    ]

class nfc_felica_info(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ( "szLen", ctypes.c_size_t ),
        ( "btResCode", ctypes.c_uint8 ),
        ( "abtId", ctypes.c_uint8 * 8 ),
        ( "abtPad", ctypes.c_uint8 * 8 ),
        ( "abtSysCode", ctypes.c_uint8 * 2 )
    ]

class nfc_iso14443b_info(ctypes.Structure):
    _pack_ = 1
    _fields_= [
        ( "abtPupi", ctypes.c_uint8, 4 ),
        ( "abtApplicationData", ctypes.c_uint8 * 4 ),
        ( "abtProtocolInfo", ctypes.c_uint8 * 3 ),
        ( "ui8CardIdentifier", ctypes.c_uint8 )
    ]

class nfc_iso14443bi_info(ctypes.Structure):
    _pack_ = 1
    _fields_ = [ 
        ( "abtDIV", ctypes.c_uint8 * 4 ),
        ( "btVerLog", ctypes.c_uint8 ),
        ( "btConfig", ctypes.c_uint8 ),
        ( "szAtrLen", ctypes.c_size_t ),
        ( "abtAtr", ctypes.c_uint8 * 33 )
    ]

class nfc_iso14443biclass_info(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ( "abtUID", ctypes.c_uint8 * 8 )
    ]

class nfc_iso14443b2sr_info(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ( "abtUID", ctypes.c_uint8 * 8 )
    ]

class nfc_iso14443b2ct_info(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ( "abtUID", ctypes.c_uint8 * 4 ),
        ( "btProdCode", ctypes.c_uint8 ),
        ( "btFabCode", ctypes.c_uint8 )
    ]

class nfc_jewel_info(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ( "btSensRes", ctypes.c_uint8 * 2 ),
        ( "btId", ctypes.c_uint8 * 4 )
    ]
class nfc_barcode_info(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ( "szDataLen", ctypes.c_size_t ),
        ( "abtData", ctypes.c_uint8 * 32 )
    ]

class nfc_target_info(ctypes.Union):
    _pack_ = 1
    _fields_ = [
        ( "nai", nfc_iso14443a_info ),
        ( "nfi", nfc_felica_info ),
        ( "nbi", nfc_iso14443b_info ),
        ( "nii", nfc_iso14443bi_info ),
        ( "nsi", nfc_iso14443b2sr_info ),
        ( "nci", nfc_iso14443b2ct_info ),
        ( "nji", nfc_jewel_info ),
        ( "ndi", nfc_dep_info ),
        ( "nti", nfc_barcode_info ) ,
        ( "nhi", nfc_iso14443biclass_info )
    ]

class nfc_target(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("nti", nfc_target_info ),
        ("nm", nfc_modulation),
    ]    

nfc_context_p = ctypes.POINTER(nfc_context)
nfc_connstr = ctypes.c_char * 1024
nfc_device_p = ctypes.POINTER(nfc_device)

libnfc.nfc_version.restype = ctypes.c_char_p

libnfc.nfc_init.argtypes = [ctypes.POINTER(nfc_context_p)]

libnfc.nfc_open.argtypes = [nfc_context_p , ctypes.POINTER(nfc_connstr)]
libnfc.nfc_open.restype = nfc_device_p

libnfc.nfc_list_devices.argtypes = [nfc_context_p ,ctypes.POINTER(nfc_connstr), ctypes.c_int]
libnfc.nfc_list_devices.restype = ctypes.c_int

libnfc.nfc_initiator_init.argtypes = [nfc_device_p]
libnfc.nfc_initiator_init.restype = ctypes.c_int

libnfc.nfc_device_get_name.argtypes = [nfc_device_p]
libnfc.nfc_device_get_name.restype = ctypes.c_char_p

# NFC_EXPORT int nfc_initiator_poll_target(nfc_device *pnd, const nfc_modulation *pnmTargetTypes, const size_t szTargetTypes, const uint8_t uiPollNr, const uint8_t uiPeriod, nfc_target *pnt);
libnfc.nfc_initiator_poll_target.argtypes = [nfc_device_p, ctypes.POINTER(nfc_modulation), ctypes.c_size_t, ctypes.c_uint8, ctypes.c_uint8, ctypes.POINTER(nfc_target)]
libnfc.nfc_initiator_poll_target.restype = ctypes.c_int

libnfc.nfc_strerror.argtypes = [nfc_device_p]
libnfc.nfc_strerror.restype = ctypes.c_char_p

libnfc.nfc_target_send_bytes.argtypes = [nfc_device_p,ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t, ctypes.c_int]
libnfc.nfc_target_send_bytes.restype = ctypes.c_int

libnfc.nfc_target_receive_bytes.argtypes = [nfc_device_p,ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t, ctypes.c_int]
libnfc.nfc_target_send_bytes.restype = ctypes.c_int