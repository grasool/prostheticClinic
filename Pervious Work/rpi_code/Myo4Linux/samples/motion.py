#Contains the motion for the motors
from __future__ import division
from time import sleep
from itertools import repeat
import math
# Import the PCA9685 module.
import Adafruit_PCA9685

class Motion():
	def __init__(self):
		self.open = 130# Min pulse length out of 4096
		self.closed = 600 # Max pulse length out of 4096
		self.rest = 350#int(math.floor((self.closed - self.open)/2))
		self.motor = Adafruit_PCA9685.PCA9685() # Initialise the PCA9685 using the default address (0x40).
		#self.motor2 = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)
		self.motor.set_pwm_freq(60)
		self.motor_order = [0,1,2,3,4] #Thumb to pinky
		self.funcDict = {'thumb':self.thumb,'pointer':self.pointer,'middle':self.middle,'ring':self.ring,'pinky':self.pinky}
		#self.funcList = [self.thumb,self.pointer,self.middle,self.ring,self.pinky]


#Individual Fingers
	def pinky(self,pos):
		self.motor.set_pwm(4,0,pos);

	def ring(self,pos):
		self.motor.set_pwm(3,0,pos)

	def middle(self,pos):
		self.motor.set_pwm(2,0,pos)

	def pointer(self,pos):
		self.motor.set_pwm(1,0,pos)

        def thumb(self,pos):
		self.motor.set_pwm(0,0,pos)
		
        def openWrist(self):
                self.motor.set_pwm(0,0,self.open)
    
        def closeWrist(self):
                self.motor.set_pwm(0,0,self.closed)

#All fingers 		
	def allFingers(self,pos):
		count = 0
		for finger in self.funcDict:
			self.funcDict[finger](pos[count])
			count = count + 1
			
	def allFingers2(self,pos):
		for finger in self.funcDict:
			self.functDict[finger](pos)

	def allClosed(self):
		self.allFingers(list(repeat(self.closed,5)))
		#self.allFingers2(self.closed)

	def allOpen(self):
		self.allFingers(list(repeat(self.open,5)))
		#self.allFingers2(self.open);

	def allRest(self):
		self.allFingers(list(repeat(self.rest,5)))
		#self.allFingers2(self.rest);

	def testEachFinger(self,t):
		mov = [self.closed,self.open]
		for finger in self.funcDict:
			for pos in mov:
				self.funcDict[finger](pos)
				sleep(t)

	def cycle(self,fingerDir,t,cycleDir = 0):
		tempDict = self.funcDict
		tempIndex = []
		if cycleDir == 1: #1 for reversed direction
			tempIndex = list(reversed(list(tempDict)))
			for i in tempIndex:
				tempDict[i] = self.funcDict[i]
		for finger in tempDict:
			tempDict[finger](fingerDir)
			sleep(t)
			
			
	def cycleFingersSeq(self,t = 0.4):
		self.cycle(self.closed,t)
		self.cycle(self.open,t)
		
	def cycleFingersEcho(self,t = 0.4):
		self.cycle(self.closed,t)
		self.cycle(self.open,t,cycleDir = 1)
		
	def pointerFinger(self):
		o = self.open
		c = self.closed
		self.allFingers([o,o,c,c,c])
		
	def pinkyOut(self):
		self.allClosed()
		self.pinky(self.open)

	def rockOut(self):
		o = self.open
		c = self.closed
		self.allFingers([o,o,c,c,o])

	def middleFinger(self):
		self.allClosed()
		self.middle(self.open)
	
	def initialize(self):
		self.allOpen()
		sleep(2)
		self.allClosed()
		sleep(2)
		self.testEachFinger(.5)
		sleep(2)
		self.pointFinger()
		sleep(2)
		self.rockOut()
		sleep(2)
		self.allOpen()
		
def test():
	m = Motion()
	while True:
		m.allOpen()
		sleep(2)
		m.allClosed()
		sleep(2)

#test()		
