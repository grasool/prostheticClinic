import os, pandas as pd, numpy as np
import matplotlib.pyplot as plt

RECORD_DIR = 'myo_data'

EMG_RANGE = 8
ORI_RANGE = 4
ACC_RANGE = 3

def getRecords():
    records = os.listdir(RECORD_DIR)
    
    assert len(records) > 0
    
    RECORD_FILENAME = 'myo_record_%s.csv'
    valid_records = [name.split('_')[-1].split('.')[0] for name in records]
    print('\nList of valid entries:', valid_records, '\n')
    pulls = []
    end = False
    while not end:
        temp = input('Input number of record to pull (enter empty input to continue): ')
        
        if temp in valid_records:
            pulls.append(temp)
        elif temp == '':
            end = True
        else:
            print('\nEntry %s not found...\n' % os.path.join(RECORD_DIR, RECORD_FILENAME%temp))
            
    pulls = [os.path.join(RECORD_DIR, RECORD_FILENAME % entry) for entry in pulls]
    
    print('\nRecords pulled:', pulls, '\n')
    
    return loadFiles(pulls)
    
def loadFiles(fileList):
    fileData = {}
    for _f in fileList:
        fileData[_f] = pd.read_csv(_f, index_col=False)
        
    return fileData
    
def splitData(df):
    EMG = 'emg_%s'
    ACC = 'acc_%s'
    ORI = 'ori_%s'
    TIME = 'time'
    
    emgData = []
    accData = []
    oriData = []
    timeData = np.array(df[TIME].tolist())
    
    for i in range(EMG_RANGE):
        emgData.append(df[EMG % (i+1)].tolist())
        
        if i < ACC_RANGE:
            accData.append(df[ACC % (i+1)].tolist())
        if i < ORI_RANGE:
            oriData.append(df[ORI % (i+1)].tolist())
    
    print(emgData)
    emgData = np.array(emgData)
    accData = np.array(accData)
    oriData = np.array(oriData)
    print(emgData)
    
    return emgData, accData, oriData, timeData
    
def plotData(data):
    nameChange = input('Would you like to rename the data titles? [y\\n]: ')
    if nameChange.lower() == 'y':
        for _f in list(data):
            temp = input('New name for %s (enter empty input to keep the same): ' % _f)
            if temp == '':
                print('Keeping same.')
                continue
                
            data[temp] = data[_f]
            del data[_f]
        
    displayFields = ''
    print('\nWhat data fields would you like to display? Enter emg, acc, ori or all... (Default = \'all\')')
    while not displayFields in ['emg', 'ori', 'acc', 'all']:
        displayFields = input('Display: ')
        if displayFields == '':
            displayFields = 'all'
            
    
    fig = {}
    axes = {}
    print(list(data))
    for _f in list(data):
        emg, acc, ori, time = splitData(data[_f])
        
        dispAll = displayFields == 'all'
        
        # EMG PLOT
        if displayFields == 'emg' or dispAll:
            emgPlot = 'EMG - %s' % _f
            fig[emgPlot], axes[emgPlot] = plt.subplots(4, 2, sharex=True, sharey=True)
            fig[emgPlot].suptitle(emgPlot)
            fig[emgPlot].subplots_adjust(hspace=0.6)
            axes[emgPlot][0, 0].set_xlim(0, len(time))
            
            j = 0
            for i in range(EMG_RANGE):
                if i == EMG_RANGE/2:
                    j+=1
                axes[emgPlot][i-(4*j), j].set_title('EMG Channel %s' % (i+1))
                axes[emgPlot][i-(4*j), j].plot(range(len(time)), emg[i])
            
        # ACC PLOT
        if displayFields == 'acc' or dispAll:
            accPlot = 'Acceleration - %s' % _f
            fig[accPlot], axes[accPlot] = plt.subplots(3, 1, sharex=True, sharey=True)
            fig[accPlot].suptitle(accPlot)
            fig[accPlot].subplots_adjust(hspace=0.6)
            axes[accPlot][0].set_xlim(0, len(time))
            
            for i in range(ACC_RANGE):
                axes[accPlot][i].set_title('Acceleration Channel %s' % (i))
                axes[accPlot][i].plot(range(len(time)), acc[i])
            
        # ORI PLOT
        if displayFields == 'ori' or dispAll:
            pass
            
    plt.show()
        
    
if __name__ == '__main__':
    data = getRecords()
    
    plotData(data)