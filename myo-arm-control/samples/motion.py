#Contains the motion for the motors
from __future__ import division
from time import sleep
from itertools import repeat
import math
# Import the PCA9685 module.
import Adafruit_PCA9685
#import msvcrt

class Motion():
    def __init__(self):
        self.open = 130# Min pulse length out of 4096
        self.closed = 600 # Max pulse length out of 4096
        self.rest = 350#int(math.floor((self.closed - self.open)/2))
        self.motor = Adafruit_PCA9685.PCA9685() # Initialise the PCA9685 using the default address (0x40).
        #self.motor2 = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)
        self.motor.set_pwm_freq(60)
        self.motor_order = [3,2,4,0,1] #Thumb to pinky
        self.funcDict = {'thumb':self.thumb,'pointer':self.pointer,'middle':self.middle,'ring':self.ring,'pinky':self.pinky}
        #self.funcList = [self.thumb,self.pointer,self.middle,self.ring,self.pinky]
        self.positions = {num: self.closed for num in self.motor_order}
        self.positions[5] = 130
        self.allClosed()

#Individual Fingers
    def pinky(self,pos):
        self.motor.set_pwm(self.motor_order[4],0,pos)
        self.updatePosition(4, pos)

    def ring(self,pos):
        self.motor.set_pwm(self.motor_order[3],0,pos)
        self.updatePosition(3, pos)

    def middle(self,pos):
        self.motor.set_pwm(self.motor_order[2],0,pos)
        self.updatePosition(2, pos)

    def pointer(self,pos):
        self.motor.set_pwm(self.motor_order[1],0,pos)
        self.updatePosition(1, pos)

    def thumb(self,pos):
        self.motor.set_pwm(self.motor_order[0],0,pos)
        self.updatePosition(0, pos)
    
    def wrist(self, pos):
        self.motor.set_pwm(5, 0, pos)
        self.updatePosition(5, pos)

    def openWrist(self):
        self.wrist(self.open)
        #self.motor.set_pwm(5,0,self.open)

    def closeWrist(self):
        self.wrist(self.closed)
        #self.motor.set_pwm(5,0,self.closed)

    def updatePosition(self, joint, pos):
        if pos > 600 or pos < 130:
            print('Position out of range')
            return
        self.positions[joint] = pos
        
#All fingers         
    def allFingers(self,pos):
        for i, finger in enumerate(self.funcDict):
            self.funcDict[finger](pos[i])
            self.updatePosition(i, pos[i])
        
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
        for i in self.motor_order:
            finger = list(self.funcDict)[i]
            print('Testing', finger)
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
        self.pointerFinger()
        sleep(2)
        self.rockOut()
        sleep(2)
        self.allOpen()
        
def test():
    m = Motion()
    #m.initialize()
    #sleep(5)
    while True:
        m.testEachFinger(0.5)
        sleep(2)
        #m.allOpen()
        #sleep(2)
        #m.allClosed()
        #sleep(2)

def keyControl():
    pass  

if __name__ == '__main__':    
    test()        
