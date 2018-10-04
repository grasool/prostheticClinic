#EMG Movements classified from Custom LDA Classifier

#As of 4/17/18 receiving data from matlab via a bluetooth module 
#Serial data in to pi

import serial
from motion import Motion

motion = Motion()


ser = serial.Serial('/dev/ttyS0')

def run():
  print("Begin RealTime Classification")
  while True:
    data = ser.read()
    if data == 'R':
      print('Rest')
      motion.allRest()
    elif data == 'O':
      print('Open')
      motion.allOpen()
    elif data == 'C':
      print('Closed')
      motion.allClosed()
    
run()
