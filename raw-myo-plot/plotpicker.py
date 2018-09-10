import os, pandas as pd, numpy as np
import matplotlib.pyplot as plt

RECORD_DIR = 'myo_data'
if not os.path.exists(RECORD_DIR):
    os.mkdir(RECORD_DIR)
    
EMG_RANGE = 8
ORI_RANGE = 4
ACC_RANGE = 3

def getRecords():
    """
        Function to get records to plot based on user input
    """
    # Gets all records in records directory
    records = os.listdir(RECORD_DIR)
    
    # Check that there are records in the dir
    assert len(records) > 0
    
    # Creates dictionary to associate each file with a number.
    # NOTE: This method is used although general nomeclature is default for output
        # incase files get renamed by user
    valid_records = {str(i): os.path.join(RECORD_DIR, name) for i, name in enumerate(records)}
    print('\nList of valid entries:')
    
    # Files and associated entry ints are output to user
    for i in list(valid_records):
        print('Enter %s for %s' % (i, valid_records[i]))
    print()
    
    # Creates list for files and bool for exiting loop
    pulls = []
    end = False
    while not end:
        # Gets user input and checks if it is valid
        temp = input('Input number of record to pull (enter empty input to continue): ')

        if temp in list(valid_records):
            pulls.append(temp)
        elif temp == '': # If entry is empty, exit loop
            end = True
        else:
            print('\nEntry %s not found...\n' % os.path.join(RECORD_DIR, RECORD_FILENAME%temp))
        
    # Convert list from ints to actual filenames associated with inputs
    pulls = [valid_records[entry] for entry in pulls]
    
    print('\nRecords pulled:', pulls, '\n')
    
    # Return dictionary of loaded file dataframes
    return loadFiles(pulls)
    
def loadFiles(fileList):
    # Function to load CSVs into dataframes then input to dictionary
    fileData = {}
    for _f in fileList:
        fileData[_f] = pd.read_csv(_f, index_col=False)
        
    return fileData
    
def splitData(df):
    # Function to split up data fields within df
    
    # General header names
    EMG = 'emg_%s'
    ACC = 'acc_%s'
    ORI = 'ori_%s'
    TIME = 'time'
    
    # Creates lists for data to plot
    emgData = []
    accData = []
    oriData = []
    timeData = np.array(df[TIME].tolist())
    
    # Propogates lists with df data
    for i in range(EMG_RANGE):
        emgData.append(df[EMG % (i+1)].tolist())
        
        if i < ACC_RANGE:
            accData.append(df[ACC % (i+1)].tolist())
        if i < ORI_RANGE:
            oriData.append(df[ORI % (i+1)].tolist())
    
    # Converts lists to numpy arrays then returns
    emgData = np.array(emgData)
    accData = np.array(accData)
    oriData = np.array(oriData)
    
    return emgData, accData, oriData, timeData
    
def plotData(data):
    # Function to put selected records into plots
    
    # Input to allow user to rename titles other than default filename titles
    nameChange = input('Would you like to rename the data titles? [y\\n]: ')
    if nameChange.lower() == 'y':
        for _f in list(data):
            temp = input('New name for %s (enter empty input to keep the same): ' % _f)
            if temp == '':
                print('Keeping same.')
                continue
                
            data[temp] = data[_f]
            del data[_f]
        
    # Input to allow user to de-clutter plots by only selecting plots of interest
    displayFields = ''
    print('\nWhat data fields would you like to display? Enter emg, acc, ori or all... (Default = \'all\')')
    while not displayFields in ['emg', 'ori', 'acc', 'all']:
        displayFields = input('Display: ')
        if displayFields == '':
            displayFields = 'all'
            
    # Creates figure and axes dictionaries for plot records
    fig = {}
    axes = {}
    for _f in list(data):
        # Splits data for one record
        emg, acc, ori, time = splitData(data[_f])
        
        # Bool shorthand for if all plots to be displayed
        dispAll = displayFields == 'all'
        
        # EMG PLOT
        if displayFields == 'emg' or dispAll: # Display EMG plot
            # Creates plot key and overall subplot
            emgPlot = 'EMG - %s' % _f
            fig[emgPlot], axes[emgPlot] = plt.subplots(4, 2, sharex=True, sharey=True)
            
            # Sets figure title, subplot layout and xlim
            fig[emgPlot].suptitle(emgPlot)
            fig[emgPlot].subplots_adjust(hspace=0.6)
            axes[emgPlot][0, 0].set_xlim(0, len(time))
            
            # Places channel data on plots
            j = 0
            for i in range(EMG_RANGE):
                if i == EMG_RANGE/2:
                    j+=1
                axes[emgPlot][i-(4*j), j].set_title('EMG Channel %s' % (i+1))
                axes[emgPlot][i-(4*j), j].plot(range(len(time)), emg[i])
            
        # ACC PLOT
        if displayFields == 'acc' or dispAll: # Display ACC plot
            # Creates plot key and overall subplot
            accPlot = 'Acceleration - %s' % _f
            fig[accPlot], axes[accPlot] = plt.subplots(3, 1, sharex=True, sharey=True)
            
            # Sets figure title, suplot layout and xlim
            fig[accPlot].suptitle(accPlot)
            fig[accPlot].subplots_adjust(hspace=0.6)
            axes[accPlot][0].set_xlim(0, len(time))
            
            # Places channel data on plots
            for i in range(ACC_RANGE):
                axes[accPlot][i].set_title('Acceleration Channel %s' % (i))
                axes[accPlot][i].plot(range(len(time)), acc[i])
            
        # ORI PLOT
        if displayFields == 'ori' or dispAll: # Display ORI plot
            # TODO: Input code for creating ORI plots
            oriPlot = 'Orientation - %s' % _f
            fig[oriPlot], axes[oriPlot] = plt.subplots(3, 1, sharex=True, sharey=True)
            
            # Sets figure title, suplot layout and xlim
            fig[oriPlot].suptitle(oriPlot)
            fig[oriPlot].subplots_adjust(hspace=0.6)
            axes[oriPlot][0].set_xlim(0, len(time))
            
            # Places channel data on plots
            for i in range(ORI_RANGE):
                axes[oriPlot][i].set_title('Acceleration Channel %s' % (i))
                axes[oriPlot][i].plot(range(len(time)), ori[i])
            
    plt.show()
        
    
if __name__ == '__main__':
    data = getRecords()
    
    plotData(data)