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
from keras.models import load_model

class MyListener(myo.DeviceListener):

  def __init__(self, queue_size=8):
    self.lock = threading.Lock()
    self.emg_data = []
  def on_connect(self, device, timestamp, firmware_version):
    device.set_stream_emg(myo.StreamEmg.enabled)

  def on_emg_data(self, device, timestamp, emg_data):
    with self.lock:
      self.emg_data = emg_data

  def get_emg_data(self):
    with self.lock:
      return self.emg_data



def convertToIntMatrix(dataIn):
        #needs numpy package
        temp = []
        for q in range(0,len(dataIn)):
            y = np.array([int(i) for i in dataIn[q]])
            temp.append(y)
        return np.array(temp)

def window(arr, ctp):
    if ctp < 100:
        l = len(arr)
        index = math.floor(l*(100-ctp)*.01/2)
        adjArr = arr[(index - 1):(l-index - 1)]
        return adjArr
    else:
        return arr

myo.init("C:\\myo-sdk-win-0.9.0\\bin")
hub = myo.Hub()

fe = featExt.FeatureExtraction()
data = []
dataStruct = []
LDA = alg.LDA()
#Name of Pickled LDA goes here
#clf = LDA.getLDA("testAng4")

clf = load_model("testEMGLSTM.h5")

listener = MyListener()
hub.run(5, listener)
time.sleep(3)


def getData():
    t = time.time()
    count = 0 
    while True:
        ti = time.time() - t
        if ti > 0.005:
            dataStruct.append(listener.get_emg_data())
            t = time.time()
            count = count + 1
        
           
comPort = True
try:
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = "COM5"
    ser.open()
except:
    comPort = False


th = threading.Thread()

#Features to extract
featuresToExtract = [1,2,3,4,5,6,7,8,9,10,12,14,16]
numFeatures = len(featuresToExtract)
movements= ["Open", "Rest","Closed"]
try:
    th = threading.Thread(target=getData)
    th.daemon = True
    th.start()
    
    t2 = time.time()
    start = t2
    stack = list([])
    while True:
        qq = time.time() - t2
        if qq >= 1:
            t2 = time.time()        
            data = convertToIntMatrix(dataStruct)
            dataStruct.clear()
            #print(list(data))
            #print("Length Before: ",len(data))
            data = window(data,ctp = 70)
            #print("Length After: ",len(data))
            #print(list(data))
            
            for num in featuresToExtract:
                #stack = list(np.hstack((stack,featExt.selectFeatures(None,data,num))))
                stack.append(featExt.selectFeatures(None,data,num))
            dstack = []
            stack = np.array(stack)
            stack = stack.reshape(1,stack.shape[0],stack.shape[1])
            #predict = clf.predict([stack]) #LDA
            predict = clf.predict(stack) #LSTM
            index = np.argmax(predict)
            print(movements[index], "Accuracy: ", predict[0][index] , ":", time.time() - start)
            if comPort:
                if predict == "Closed":
                    ser.write(b'0\n')
                if predict == "Open":
                    ser.write(b'1\n')
                if predict == "Rest":
                    ser.write(b'2\n')
            #dstack.delete()
        
            stack = list([])
finally:
    hub.shutdown()

