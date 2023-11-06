import nfc.nfc as nfc

APDU_SELECT_AID = (0x00, 0xA4, 0x04, 0x00)
APDU_READ_RECORD = (0x00, 0xB2, 0x00, 0x00)

class NfcReader:
    _device: nfc.NfcDevice
    
    aid: str
    issuer: str
    
    def __init__(self, config = None):
        print('NFC libnfc version ' + nfc.NfcDevice.version())
        self._device = nfc.NfcDevice(config.dev if config.dev else None)
        self.aid = config.aid or "A000000001020304"
        self.issuer = config.issuer or "Example"
        
        print(self._device.name, self._device.connection_string)
        
        
    def next(self):
        tag = self._device.next()
        
        result = list(("X-Reader", "nfc"))
        result.append(("X-Nfc-Issuer", self.issuer))
        
        result.append(())
        
        if tag.type == "tag":
            result.append(("X-Nfc-Type", "tag"))
            result.append(("X-Nfc-Record-Type", "PAP"))
            result.append(("User-Name", "nfc-tag"))
            result.append(("Password", tag.uid))
            
        elif (tag.type == "android"):
            result.append(("X-Nfc-Type", "android"))
            result.append(("X-Nfc-Aid", self.aid))
            
            tag.sendApdu(*APDU_SELECT_AID, bytes.fromhex(self.aid))
            data: bytes = tag.sendApdu(*APDU_READ_RECORD, bytes.fromhex(self.issuer))
            
            # | 1 byte | 1 byte  |  *   |  1 byte  |  *     |
            # |  type  | acc len | acc* | pass len | pass * |
            
            offset = 0
            recordType = "Unknown"
            recordTypeInt = data[0]
            if recordTypeInt == 1:
                recordType = "PAP"
            offset += 1 
            accountLength = data[offset]
            offset += 1 
            account = data[offset: offset + accountLength]
            offset += accountLength
            passwdLength = data[offset]
            offset += 1 
            passwd = data[offset: offset + passwdLength]
                   
            result.append(("X-Nfc-Record-Type", recordType))
            result.append(("User-Name", account.decode('utf-8')))
            result.append(("Password", passwd.decode('utf-8')))
        
        return result
    
    

# for tag in dev:
#     try:
#         print(tag.uid)
#         print(tag.info)
    
#         print("Select app A0000001020304")
#         res = tag.sendApdu(0x00, 0xA4, 0x04, 0x00, bytes.fromhex('A0000001020304'))
#         print("ANS: ", res)
        
        
#     except:
#         pass