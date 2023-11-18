
class BytesReader():
    raw: bytearray
    
    position = 0
    
    def __init__(self, data: bytearray):
        self.raw = data

        
    def read(self, num: int = 1):
        result = self.raw[self.position: self.position+num]
        self.seek(num)
        return result
    
    def readInt(self, num: int = 4):
        return int.from_bytes(self.read(num))
    
    def seek(self, num: int):
        self.position += num
        
        
    
        