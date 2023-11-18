import nfc.bytes_reader as br

data = b'\x01\x05vfrc2\x06\x124Vx\x91#\x90\x00'

rdr = br.BytesReader(data)

recordTypeInt = rdr.readInt(1)
if recordTypeInt == 1:
    recordType = "PAP"
account = rdr.read(rdr.readInt(1))
passwd = rdr.read(rdr.readInt(1))

print(account.decode('utf-8'),passwd)