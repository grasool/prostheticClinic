import csv
from DataBin import DataBin
import time
import pickle
from FeatureExtraction import FeatureExtraction as featExt
import numpy as np

#need a data object to store the bins 
rawData = []
sampleTime = 5 #sec
movements = ["Open","Rest","Closed","Flex","Extend","Pronation","Supination"]
movDataDic = {}
dataBinDictionary = {}

def csvReader(fileName, dataBeginDelimeter):
    with open(fileName + '.csv',newline = '') as file:
        reader = csv.reader(file)
        for row in reader:
           rawData.append(row)

    count = 0
    dataIndex =[]
    for i in range(0,len(rawData)):
        temp = rawData[i][0]
       #print(movements[count])
        if count < len(movements) and str(temp) == movements[count]:
           dataIndex.append(i+1)
           count = count + 1
        if count == len(movements) and str(temp) == 'Rest':
            dataIndex.append(i+1)
   
    movDataDic["index"] = dataIndex
    for i in range(0,len(dataIndex) - 1):
        y = dataIndex[i]
        tempData = []
        for y in range(dataIndex[i],dataIndex[i] + 1080): #dataIndex[i+1] - 1):
            tempX = []
            for x in range(0, len(rawData[y])):
                tempX.append(rawData[y][x])
            tempData.append(tempX)
        movDataDic[movements[i]] = tempData
        
       
def make():
    dataBinDictionary["Name"] = "Test"    
    for i in range(0,len(movements)):
        temp = movDataDic[movements[i]]
        temp = ctpWindow(temp,100)
        #add method to calculate ctp here, pass temp (matrix) and truncate quant of rows
        tempEMG = []
        tempGyro = []
        tempAccel = []
        for j in range(0,len(temp)):
            tempEMG.append(temp[j][1:9])
            tempGyro.append(temp[j][9:12])
            tempAccel.append(temp[j][12:16])
        dataBinDictionary[movements[i]] = DataBin(movements[i],100,0,0,tempEMG,tempEMG,tempGyro,tempAccel)
        

def ctpWindow(arr, ctp):
    
    if ctp != 100:
        adjArr = []
        truncVal = int((100 - ctp)*.01*len(arr)/2)
        for i in range(truncVal,len(arr)-truncVal):
            adjArr.append(arr[i][:])
        return adjArr
    else:
        return arr


def convertMatToInt(x):
    #needs numpy package
    temp = []
    for q in range(0,len(x)):
        y = np.array([int(i) for i in x[q]])
        temp.append(y)
    
    return np.array(temp)

csvReader("data3","")
make()
#print(movDataDic[movements[0]][1][0])
#print(movDataDic["index"])
#print(rawData[0][0])
#print(dataBinDictionary["Open"].getAccelData()[3][0])

pickleOut = open("dataBin.pickle","wb")
pickle.dump(dataBinDictionary, pickleOut)
pickleOut.close()
#retrieve pickle

pickleIn = open("dataBin.pickle","rb")
e = pickle.load(pickleIn)
#print(e["Open"].getAccelData()[3][0])


fe = featExt()
#print(e["Open"].getEMGData())
tempData = e["Open"].getEMGData()
#print(tempData)
tempData = convertMatToInt(tempData)
#print(tempData)

rms = fe.extractRMS(tempData)
print("Root Means Squared (RMS): \n")
print(rms)
print("\n--------")


iav = fe.extractIAV(tempData)
print("Integraged Absolute Mean (IAV): \n")
print(iav)
print("\n--------")

mav = fe.extractMAV(tempData)
print("Mean Absolute Value (MAV): \n")
print(mav)
print("\n--------")

mav1 = fe.extractMAV1(tempData)
print("Meav Absolute Value Type 1 (MAV1)\n")
print(mav1)
print("\n--------")

mav2 = fe.extractMAV2(tempData)
print("Meav Absolute Value Type 2 (MAV2)\n")
print(mav2)
print("\n--------")

ssi = fe.extractSSI(tempData)
print("Simple Square Integral (SSI) \n")
print(ssi)
print("\n--------")

var = fe.extractVariance(tempData)
print("Variance: \n")
print(var)
print("\n--------")

tm3 = fe.extractTM3(tempData)
print("Temporal Movements 3 \n")
print(tm3)
print("\n--------")

tm4 = fe.extractTM4(tempData)
print("Temporal Movements 4 \n")
print(tm4)
print("\n--------")

tm5 = fe.extractTM5(tempData)
print("Temporal Movements 5 \n")
print(tm5)
print("\n--------")

vOrder = fe.extractVOrder(tempData, order = 2)
print("V Order: \n")
print(vOrder)
print("\n--------")

waveformLength = fe.extractWL(tempData)
print("Waveform Length (WL):\n")
print(waveformLength)
print("\n--------")

aac = fe.extractAAC(tempData)
print("Average Amplitude Change (AAC): \n")
print(aac)
print("\n--------")

dasdv = fe.extractDASDV(tempData)
print("Difference Absolute Standard Deviation Value: \n")
print(dasdv)
print("\n--------")








