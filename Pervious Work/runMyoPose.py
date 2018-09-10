#MYO Band Pose
'''
File that retrieves the classification from the band itself
Outputs to arduino
Is essentially a test script

'''


from __future__ import print_function
import collections
import myo
import threading

import time
import FeatureExtraction as featExt
import numpy as np
import Algorithms as alg
from itertools import islice
import serial
import math
import time

class MyListener(myo.DeviceListener):

    def __init__(self, queue_size=8):
        self.lock = threading.Lock()
        self.pose = ""
    def on_connect(self, device, timestamp, firmware_version):
        device.set_stream_emg(myo.StreamEmg.enabled)
	
    def on_pose(self, myo, timestamp, pose):
        #print(myo.Pose)
        self.pose = pose
        #print(pose)
            

    def get_pose(self):
        with self.lock:
            return self.pose
serialOn = False
try:
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = "COM5"
    ser.open()
    serialOn = True
except:
    serialOn = False
    pass

def movement(mov,on):
    
    if on:
        if mov == 0:    
            ser.write(b'0\n')
        if mov == 1:
            ser.write(b'1\n')
        if mov == 2:
            ser.write(b'2\n')
    

myo.init("C:\\myo-sdk-win-0.9.0\\bin")
hub = myo.Hub()
listener = MyListener()
hub.run(5, listener)


poseArr = []
restCount = 0
openCount = 0
closedCount = 0
temp = [0,0,0]
x = 0
try:
    while True:
        p = listener.get_pose()
        if p == "":
            print("Myo Not Connected")
        else:
            poseArr.append(str(p))
            print(p)
            if len(poseArr) >= 5:
                for i in poseArr:
                    if p == "rest":
                        restCount = restCount + 1
                        temp[2] = restCount
                    elif p == "fingers_spread":
                        openCount = openCount + 1
                        temp[0] = openCount
                    elif p == "fist":
                        closedCount = closedCount + 1
                        temp[1] = closedCount
                movement(x,serialOn)
                x = np.argmax(temp)
                poseArr.clear()
                restCount = 0
                openCount = 0
                closedCount = 0
                temp = [0,0,0]
                #print(temp[x])
            
            
            time.sleep(.05)
finally:
	hub.shutdown()
