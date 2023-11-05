import nfc_wrapper as nfc

print('NFC libnfc version ' + nfc.NfcManager.version())

mng = nfc.NfcManager()

# mng.list_devices(2)

dev = mng.open()

print(dev.name, dev.connection_string)

for tag in dev:
    print(tag)