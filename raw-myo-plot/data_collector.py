import pandas as pd
import numpy as np
import time, os

EMG_RANGE = 8
ORI_RANGE = 4
ACC_RANGE = 3

# General output folder and filename for recorded data
OUT_FOLDER = 'myo_data'

# Class for recording MYO data
class myo_data_collector(object):
    def __init__(self):
        self.set_originals()
        self.recording = False
        
        # If output directory does not exist, it is created
        if not os.path.exists(OUT_FOLDER):
            os.mkdir(OUT_FOLDER)
        
    def set_originals(self):
        # Creates numpy arrays for EMG, ACC and ORI data
        self.emg = np.array([[]]*EMG_RANGE)
        self.acc = np.array([[]]*ACC_RANGE)
        self.ori = np.array([[]]*ORI_RANGE)
        
        # Creates time list and samples left
        self.timescale = []
        self.samples_left = -1
        
    def reset_data(self):
        # Resets record buffers
        self.set_originals()
        
    def timed_record(self, sample_rate, record_time):
        self.samples_left = sample_rate*record_time
        #self.toggle_recording()
        
    def toggle_recording(self):
        # Toggles recording bool
        self.recording = not self.recording
        
    def collect(self, listener, ctime):
        # If instance is set to record, record buffers are appended with new
            # input data
        if self.recording:
            self.timescale.append(ctime)
            
            self.emg = np.hstack((self.emg, listener.emg.data[:, -1:]))
            self.ori = np.hstack((self.ori, listener.orientation.data[:, -1:]))
            self.acc = np.hstack((self.acc, listener.acc.data[:, -1:]))
            
            self.samples_left -= 1
            
    def save_plot_data(self, listener, filename):
        self.timescale = range(len(listener.emg.data[0]))
        
        self.emg = np.array(listener.emg.data)
        self.ori = np.array(listener.orientation.data)
        self.acc = np.array(listener.acc.data)

        filename = self.save_record(filename)
        
        self.reset_data()
        
        return filename
                    
    def save_record(self, filename):
        # If recorder is told to save buffers...
        
        # Creates dataframe and inputs time
        out = pd.DataFrame(columns=['time'])
        out['time'] = pd.Series(self.timescale)
        
        # Goes through EMG channels and inputs to df
        for i in range(EMG_RANGE):
            out['emg_%s' % (i+1)] = pd.Series(self.emg[i])
            
        # Goes through ORI channels and inputs to df
        for i in range(ORI_RANGE):
            out['ori_%s' % (i+1)] = pd.Series(self.ori[i])
            
        # Goes through ACC channels and inputs to df
        for i in range(ACC_RANGE):
            out['acc_%s' % (i+1)] = pd.Series(self.acc[i])
            
        # Gets filename to save at then outputs as CSV without df index
        filename = find_filename(filename)
        out.to_csv(filename, index=False)
        
        self.reset_data()
        
        return filename
        
def find_filename(OUT_FILE):
    """
        Function to find next filename to use in records directory so not
        files are overwritten.
    """
    if not '%s' in OUT_FILE:
        print('WARNING: NO %s REPLACEMENT IN SAVE SCHEME! WRITING '
                'FILE AS NAME WAS INPUT!')
        return OUT_FILE
    
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
            print('10000 records present, starting to overwrite last file...')
            break
                    
        
    return temp