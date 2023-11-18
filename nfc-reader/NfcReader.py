import nfc.nfc as nfc
import nfc.bytes_reader as br

APDU_SELECT_AID = (0x00, 0xA4, 0x04, 0x00)
APDU_READ_RECORD = (0x00, 0xB2, 0x00, 0x00)

class NfcReader:
    _device: nfc.NfcDevice
    
    aid: str
    issuer: str
    
    def __init__(self, config = None):
        print('NFC libnfc version ' + nfc.NfcDevice.version())
        self._device = nfc.NfcDevice(config.get('device') if config.get('device') or config.get('device') == 'auto' else None)
        self.aid = config.get('aid') or "A0000001020305"
        self.issuer = config.get('issuer') or "Example"
        
        print(self._device.name, self._device.connection_string)
        
        
    async def next(self):
        tag = self._device.next()
        
        result = list()
        result.append(("X-Reader", "nfc"))
        result.append(("X-Nfc-Issuer", self.issuer))
        
        
        # if tag.type == "tag":
        #     result.append(("X-Nfc-Type", "tag"))
        #     result.append(("X-Nfc-Record-Type", "PAP"))
        #     result.append(("User-Name", "nfc-tag"))
        #     result.append(("Password", tag.uid))
            
        # elif (tag.type == "android"):
        result.append(("X-Nfc-Type", "android"))
        result.append(("X-Nfc-Aid", self.aid))
        
        err = None
        
        try:
            print('Select aid ', self.aid)
            tag.sendApdu(*APDU_SELECT_AID, bytes.fromhex(self.aid), 2)
            print("Read record")
            data: bytes = tag.sendApdu(*APDU_READ_RECORD, self.issuer.encode('utf-8'), 255)
            
            rdr = br.BytesReader(data)

            recordTypeInt = rdr.readInt(1)
            if recordTypeInt == 1:
                recordType = "PAP"
            account = rdr.read(rdr.readInt(1))
            passwd = rdr.read(rdr.readInt(1))

                    
            result.append(("X-Nfc-Record-Type", recordType))
            result.append(("User-Name", account.decode('utf-8')))
            result.append(("Password", passwd.decode('utf-8')))
        except Exception as error:
            err = error
            print(err)
            result = None
        finally:        
            print("Wait tag to be removed...")
            await tag.waitTagRelease()
        
        return result, err
    
    

# for tag in dev:
#     try:
#         print(tag.uid)
#         print(tag.info)
    
#         print("Select app A0000001020304")
#         res = tag.sendApdu(0x00, 0xA4, 0x04, 0x00, bytes.fromhex('A0000001020304'))
#         print("ANS: ", res)
        
        
#     except:
#         pass