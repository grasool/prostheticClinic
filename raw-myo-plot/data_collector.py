import pandas as pd
import numpy as np
import time, os

EMG_RANGE = 8
ORI_RANGE = 4
ACC_RANGE = 3

OUT_FOLDER = 'myo_data'
OUT_FILE = os.path.join(OUT_FOLDER, 'myo_record_%s.csv')

class myo_data_collector(object):
    def __init__(self):
        self.emg = [[]]*EMG_RANGE
        self.acc = [[]]*ACC_RANGE
        self.ori = [[]]*ORI_RANGE
        self.timescale = []
        self.recording = False
        
        if not os.path.exists(OUT_FOLDER):
            os.mkdir(OUT_FOLDER)
        
    def reset_data(self):
        self.__init__()
        
    def toggle_recording(self):
        self.recording = not self.recording
        
    def collect(self, listener, ctime):
        if self.recording:
            self.timescale.append(ctime)
            for i in range(EMG_RANGE):
                print(len(listener.emg.data))
                print(len(listener.emg.data[i]))
                print()
                self.emg[i].append(listener.emg.data[i, -1])
                
                if i < ORI_RANGE:
                    self.ori[i].append(listener.orientation.data[i, -1])
                if i < ACC_RANGE:
                    self.acc[i].append(listener.acc.data[i, -1])
                    
    def save_record(self):
        out = pd.DataFrame(columns=['time'])
        out['time'] = pd.Series(self.timescale)
        
        for i in range(EMG_RANGE):
            out['emg_%s' % (i+1)] = pd.Series(self.emg[i])
            
        for i in range(ORI_RANGE):
            out['ori_%s' % (i+1)] = pd.Series(self.ori[i])
            
        for i in range(ACC_RANGE):
            out['acc_%s' % (i+1)] = pd.Series(self.acc[i])
            
        filename = find_filename()
        out.to_csv(filename, index=False)
        
        return filename
        
def find_filename():
    i = 0
    temp = OUT_FILE % i
    
    while os.path.exists(temp):
        i += 1
        temp = OUT_FILE % i
        
        if i == 9000:
            print('WARNING: 9000+ records found. Files '
                'will start to be overwritten at 10000 records. '
                'Please move or delete some records from '
                '%s directory.' % OUT_FOLDER)
        elif i == 10000:
            break
                    
        
    return temp