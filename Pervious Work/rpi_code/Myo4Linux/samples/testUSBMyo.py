#Myo USB
import sys
sys.path.append('../lib/')

from myo import Myo
from packet import Packet
import utilities
import struct

myo = Myo()
myo.connect()

while True:
	x = myo.read_attribute(0x27)
	#print(type(x))
	print(x.getData())
	#x.getD()
	#print(struct.unpack("8HB",x.payload))
	#print(struct.unpack("<11B",x))

