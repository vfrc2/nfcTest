from NfcReader import NfcReader
import yaml
import os
import asyncio

CONFIG_FILE_PATH = os.environ.get("NFC_LOC_CONFIG_FILE") or "config.yaml"


async def main():
    config = None

    with open(CONFIG_FILE_PATH, 'r') as f:
        config = yaml.safe_load(f)
        
    reader = NfcReader(config['nfc'])

    while True:
        try:
            attrs = await reader.next()
            print(attrs)
        except Exception as ex:
            print("Error", ex)

asyncio.run(main())

