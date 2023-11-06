import NfcReader
import yaml
import os

CONFIG_FILE_PATH = os.environ["NFC_LOC_CONFIG_FILE"] or "config.yaml"

config = None

with open(CONFIG_FILE_PATH, 'r') as f:
    config = yaml.safe_load(f)
    
reader = NfcReader(config.nfc)

while True:
    attrs = reader.next()
    
    print(attrs)



