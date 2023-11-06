import nfc.nfc as nfc

print('NFC libnfc version ' + nfc.NfcDevice.version())

dev = nfc.NfcDevice()

print(dev.name, dev.connection_string)

for tag in dev:
    print(tag.uid)
    print(tag.info)
    
    tag.sendApdu(0x00, 0xA4, 0x04, 0x00, bytes.fromhex('A0000001020304'), 2)