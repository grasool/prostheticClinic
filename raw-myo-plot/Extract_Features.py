# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 12:54:07 2018

@author: bsala_000
"""
import os
import numpy as np
import pandas as pd



def getFilename(RECORDS_DIR='myo_data'):
    """
        Function to allow user to pick filename of CSV to load in the
            input records directory. Filename is picked by its
            index within the directory which is output to the user
            along with the associated filename. If an invalid
            file index is entered, the function keeps asking for
            a correct index until one is entered.
    """
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
            
def print_record_features(data):
    """
        Function to print results of all feature extracting functions
            based on data input
            
        :data: - Dataframe of loaded EMG data from CSV
    """
    print(get_RMS(data))
    print(get_Var(data))
    print(get_MAV(data))
    print('Zero Crossings:\n',get_zero_crossings(data))
    print('Waveform Lengths:\n',get_waveform_length(data))
    
def get_record_features(data, savefile=False):
    """
        Function to return all feature results based on data input
        
        INPUT
        :data: - Dataframe of loaded EMG data from CSV
        
        OUTPUT
        :features: - Dictionary of dataframes for extracted features
    """
    features = {}
    features['rms'] = get_RMS(data)
    features['var'] = get_Var(data)
    features['mav'] = get_MAV(data)
    features['zc'] = get_zero_crossings(data)
    features['wfl'] = get_waveform_length(data)
    
    if savefile:
        save_features(features, savefile)
        
    return features
    
def save_features(data_dict, f):
    """
        Function to save extracted features in specified filename
        
        INPUTs
        :data_dict: - Dictionary of dataframes like the one output from 
                        get_record_features()
        :f: - CSV filename to save features to
        
    """
    out = pd.DataFrame(columns=list(data_dict[0]))
    for i in list(data_dict):
        data_dict[i].loc[0, ('feature')] = id
        out = pd.concat([out, data_dict[i]], ignore_axis=True)
        
    out.to_csv(f, index=False)
    
def get_RMS(data):
    """
        Function to get root mean squared value for each dataframe column.
            
        INPUT
        :data: - Dataframe of loaded EMG data from CSV
        
        OUTPUT
        :RMS: - Dataframe of RMS values from input in each column
    """
    
    # Get number of rows
    n = data.shape[0] 
    # Square each value in table
    data = data.apply(lambda x:x**2)
    # Sum each column values
    s = data.apply(np.sum,axis = 0)
    # SQRT resulting single value within each column
    RMS = s.apply(lambda x:np.sqrt(x/n))
    return RMS

def get_Var(data):
    """
        Function to get variance feature for each column.
        
        INPUT
        :data: - Dataframe of loaded EMG data from CSV
        
        OUTPUT
        :data: - Dataframe of varience values for each input column
    """
    # Gets standard deviation by column then squares that value
    data = (np.std(data,axis = 0))**2
    return data

def get_MAV(data):
    """
        Function to get mean absolute value feature for each column.
        
        INPUT
        :data: - Dataframe of loaded EMG data from CSV
        
        OUTPUT
        :data: - Dataframe of MAV for each input column
    """
    # Gets absolute value for each value in table then gets mean of each column.
    data = np.mean(np.abs(data), axis = 0)
    return data

def get_zero_crossing_matlab():
    """
        DEPRECIATED - See get_zero_crossings() function below
        
        Function to get number of zero crossings feature by using MATLAB script
    """
    Z = eng.Zero_Crossing()
     
    return np.array(Z).astype(int)

def get_zero_crossings(data):
    """
        Function to get number of zero crossings feature for each column
        
        INPUT
        :data: - Dataframe of loaded EMG data from CSV
        
        OUTPUT
        :data: - Dataframe of zero crossings count per column
    """
    
    crossings = pd.DataFrame(0, index=[0], columns=list(data))
    for col in list(data):
        crossings[col].loc[0] = len(np.where(np.diff(np.sign(data[col])))[0])
        
    return crossings

def get_waveform_length_matlab():
    """
        DEPRECIATED
        
        Use function below instead (get_waveform_length)
    """
    W = eng.Waveform_Length()
    return np.array(W).astype(int) 
    
def get_waveform_length(data):
    """
        Function to get waveform length feature for each column
        
        INPUT
        :data: - Dataframe of loaded EMG data from CSV
        
        OUTPUT
        :data: - Dataframe of waveform length sums per column
    """
    data = data.diff().abs().sum(axis=0)
    
    return data

def get_all_files(dir):
    c = input('Select specific files (enter 0) or select based on regex (enter 1)? ')
    if c == '0':
        files = select_batch(dir)
    elif c == '1':
        files = regex_batch(dir)
    else:
        files = []
        
    return files
        
def select_batch(dir):
    print('\n' + '='*40 + '\nSELECT FILES\n')
    for i, f in enumerate(sorted(set(os.listdir(dir)))):
        print(i, ':', f)
        
    c = input('\nInput number choices separated by commas or -1 for all: ')
    c = c.replace(' ', '').split(',')
        
    if c[0] == '-1':
        c = range(len(os.listdir(dir)))
        
    files = []
    for e in c:
        try:
            int(c[0])
        except:
            print('Could not use %s as index. Not an integer.' % e)
            continue
            
        f = sorted(set(os.listdir(dir)))[int(e)]
        alternate_file = os.path.join(dir, '.'.join(f.split('.')[:-1]) + '_snipped.csv')
        if '_snipped' in f or os.path.exists(alternate_file):
            continue
        files.append(os.path.join(dir, f))
        
    return files
    
def regex_batch(dir):
    print('Regex functionality not complete yet, please '
            'select by specific files for now... Exiting...')
    return []
    
if __name__ == '__main__':
    c = input('Batch or test (b/t): ')
    if c == 'b':
        c = input('Select specific files (enter 0) or select based on regex (enter 1)? ')
        if c == '0':
            select_batch('myo_data')
        elif c == '1':
            regex_batch('myo_data')
    elif c == 't':
        f = os.path.join('myo_data','myo_record_0.csv')
        df = pd.read_csv(f)
        get_record_features(df)