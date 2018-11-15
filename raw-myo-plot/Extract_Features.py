# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 12:54:07 2018

@author: bsala_000
"""
import os
import numpy as np
import pandas as pd
#import matlab.engine
#eng = matlab.engine.start_matlab()

f = os.path.join('myo_data','myo_record_0.csv')
df = pd.read_csv(f)

def getFilename(RECORDS_DIR='myo_data'):
    if len(os.listdir(RECORDS_DIR)):
        print('Records found:')
        for i, f in enumerate(sorted(set(os.listdir(RECORDS_DIR)))):
            print(i, ':', f)
            
        f = input('Enter number of file to load: ')
        
        fileFound = False
        while not fileFound:
            try:
                i = int(f)
                f = sorted(set(os.listdir(RECORDS_DIR)))[i]
                fileFound = True
            except:
                print('Incorrect input... Must be number listed above.')
                
        return os.path.join(RECORDS_DIR, f)
        
    else:
        print('No records found.')
        return ''
            
def get_record_features(data):
    print(get_RMS(data))
    print(get_Var(data))
    print(get_MAV(data))
    print('Zero Crossings:',zero_crossings2(data))
    #print ('Waveform Lengths:',get_waveform_length())
    
def get_RMS(data):
    n = data.shape[0] 
    data = data.apply(lambda x:x**2)
    s = data.apply(np.sum,axis = 0)
    RMS = s.apply(lambda x:np.sqrt(x/n))
    return RMS

def get_Var(data):
    data = (np.std(data,axis = 0))**2
    return data

def get_MAV(data):
    data = np.mean(np.abs(data), axis = 0)
    return data

def get_zero_crossing():
     Z = eng.Zero_Crossing()
     
     return np.array(Z).astype(int)

def zero_crossings2(data):
    crossings = {}
    for col in list(data):
        crossings[col] = np.where(np.diff(np.sign(data[col])))[0]
        crossings[col] = len(crossings[col])
        
    return crossings

def get_waveform_length():
    W = eng.Waveform_Length()
    return np.array(W).astype(int) 

if __name__ == '__main__':
    get_record_features(df)