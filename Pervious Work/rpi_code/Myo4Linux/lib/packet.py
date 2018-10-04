from utilities import *

class Packet():
    def __init__(self, ords):
        self.ords = ords
        self.data_type = ords[0]
        self.cls = ords[2]
        self.command = ords[3]
        self.payload = multichr(ords[4:])
        self.temp = multiord(multichr(ords[5:]))
        self.ret = ''
        #self.temp2 = unpack('8HB', self.payload[5:])
        #self.temp2 = self.test()		
		
    def __repr__(self):
        self.ret = '[%s]' % (' '.join('%02X' % b for b in multiord(self.payload)))
        #print("ret:",self.ret)
        return self.ret
    
    def getData(self):
        print("Ords: ",self.ords)
        print("Payload: ", self.payload)
        print("Length payload: ",len(self.payload))
        print("Temp: ",self.temp)
        x = len(self.ords)
        return x
		
    def getD(self):
        print("Len Ord: ",len(self.ords[:4]))
        connection, attribute, data_type = unpack('BHB', self.ords[:4])
        print(attribute)
        if attribute == 0x27:
            print("EMG")