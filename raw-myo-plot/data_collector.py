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
        self.emg = np.array([[]]*EMG_RANGE)
        self.acc = np.array([[]]*ACC_RANGE)
        self.ori = np.array([[]]*ORI_RANGE)
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
            
            self.emg = np.hstack((self.emg, listener.emg.data[:, -1:]))
            self.ori = np.hstack((self.ori, listener.orientation.data[:, -1:]))
            self.acc = np.hstack((self.acc, listener.acc.data[:, -1:]))
                    
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