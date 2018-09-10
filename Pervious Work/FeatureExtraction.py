#Extracts the features from the Data

'''
Any set of features can be added as functions to be extracted
This file is both used to train the algorithms and run live data testing
'''

import numpy as np
import pickle

class FeatureExtraction:
    def extractRMS(null,dataIn):
        dataOut = []
        for i in range(0,len(dataIn[0])):
            dataOut.append(np.sqrt(np.mean(dataIn[:,i]**2)))
        return dataOut

    #Extract Integrated Absolute Value (IAV)
    def extractIAV(null, dataIn):
        dataOut = []
        for i in range(0,len(dataIn[0])):
            dataOut.append(np.sum(np.absolute(dataIn[:,i])))
        return dataOut

    #Extract Mean Absolute Value (MAV)
    def extractMAV(null, dataIn):
        dataOut = []
        for i in range(0,len(dataIn[0])):
            dataOut.append(np.mean(dataIn[:,i]))
        return dataOut

    #Extract Mean Absolute Value Type 1 (MAV1)
    def extractMAV1(null, dataIn):
        dataOut = []
        size = len(dataIn)
        w = 0
        for i in range(0,len(dataIn[0])):
            total = 0
            for j in range(0, size):
                if 0.25*size <= j and j <= 0.25*size:
                    w = 1
                else:
                    w = 0.5 #otherwise weight 0.5
                total = total + w*abs(dataIn[j,i])
            dataOut.append(total/size)
        return dataOut

    #Extract Mean Absolute Value Type 2 (MAV2)
    def extractMAV2(null,dataIn):
        dataOut = []
        size = len(dataIn)
        w = 0
        for i in range(0,len(dataIn[0])):
            total = 0
            for j in range(0,size):
                if 0.25*size <= j and j <= 0.75*size:
                    w = 1
                elif i < 0.25*size:
                    w = 4*j/size
                else:
                    w = 4*(j-size)/size
                    
                    
                total = total + w*abs(dataIn[j,i])
            dataOut.append(total/size)
        return dataOut

    def extractSSI(null, dataIn):
        dataOut = []
        for i in range(0,len(dataIn[0])):
            dataOut.append(np.sum(dataIn[:,i]**2))
        return dataOut

    def extractVariance(null,dataIn):
        dataOut = []
        size = len(dataIn)
        for i in range(0,len(dataIn[0])):
            dataOut.append(1/(size-1)*np.sum(dataIn[:,i]**2))
        return dataOut

    def extractTM3(null,dataIn):
        dataOut = []
        for i in range(0,len(dataIn[0])):
            dataOut.append(np.mean(dataIn[:,i]**3))
        return dataOut

    def extractTM4(null,dataIn):
        dataOut = []
        for i in range(0,len(dataIn[0])):
            dataOut.append(np.mean(dataIn[:,i]**4))
        return dataOut

    def extractTM5(null,dataIn):
        dataOut = []
        for i in range(0,len(dataIn[0])):
            dataOut.append(np.mean(dataIn[:,i]**5))
        return dataOut

    def extractVOrder(null,dataIn,order):
        dataOut = []
        for i in range(0,len(dataIn[0])):
            dataOut.append(np.power(np.mean(dataIn[:,i]**order),(1/order)))
        return dataOut

    def extractWL(null,dataIn):
        dataOut = []
        for i in range(0,len(dataIn[0])):
            total = 0
            for j in range(0, len(dataIn)-1):
                total = total + abs(dataIn[j+1,i] - dataIn[j,i])
            dataOut.append(total)
        return dataOut

    def extractAAC(null,dataIn):
        dataOut = []
        size = len(dataIn)
        for i in range(0,len(dataIn[0])):
            total = 0
            for j in range(0, size -1):
                total = total + abs(dataIn[j+1,i] - dataIn[j,i])
            dataOut.append(total/size)
        return dataOut

    def extractDASDV(null,dataIn):
        dataOut = []
        size = len(dataIn)
        threshold = 50; #Play with this number
        for i in range(0,len(dataIn[0])):
            total = 0
            for j in range(0, size -1):
                total = total + (dataIn[j+1,i] - dataIn[j,i])**2
            dataOut.append(np.sqrt(total/(size-1)))
        return dataOut
    
    def extractZC(null, dataIn, threshold = 20):
        dataOut = []
        size = len(dataIn)
        for i in range(0, len(dataIn[0])):
            zc_count = 0
            for j in range(0, size -1):
                if((dataIn[j,i] > 0 and dataIn[j+1,i] < 0) or (dataIn[j,i] < 0 and dataIn[j+1,i] > 0)):
                    if(abs(dataIn[j+1,i] - dataIn[j,i]) > threshold):
                        zc_count = zc_count+1
            dataOut.append(zc_count)
        return dataOut

    def extractSSC(null, dataIn,threshold = 0): 
        dataOut = []
        size = len(dataIn)
        for i in range(0, len(dataIn[0])):
            ssc_count = 0
            for j in range(1, size -1):            
                if( (dataIn[j,i] > dataIn[j-1,i] and dataIn[j,i] > dataIn[j+1,i]) or (dataIn[j,i] < dataIn[j-1,i] and dataIn[j,i] < dataIn[j+1,i])):
                    print(dataIn[j,i])
                    if( (abs(dataIn[j,i] - dataIn[j+1,i]) > threshold) or (abs(dataIn[j,i] - dataIn[j-1,i]) > threshold) ):
                        ssc_count = ssc_count+1
            dataOut.append(ssc_count)
        #print(dataOut)
        return dataOut

    def extractFFT(null, dataIn):
        dataOut = []

        for i in range(len(dataIn[0])):
            #x = np.fft(dataIn[:,i])
            dataOut.append(np.fft.fft(dataIn[:,i]))
        return dataOut

#Pass a number to this function and the specific feature will be extracted
fe = FeatureExtraction()
def selectFeatures(null,dataIn,number = 0, vOrder = 1):
    if number == 1:
        return fe.extractRMS(dataIn)
    elif number == 2:
        return fe.extractIAV(dataIn)
    elif number == 3:
        return fe.extractMAV(dataIn)
    elif number == 4:
        return fe.extractMAV1(dataIn)
    elif number == 5:
        return fe.extractMAV2(dataIn)
    elif number == 6:
        return fe.extractSSI(dataIn)
    elif number == 7:
        return fe.extractVariance(dataIn)
    elif number == 8:
        return fe.extractTM3(dataIn)
    elif number == 9:
        return fe.extractTM4(dataIn)
    elif number == 10:
        return fe.extractTM5(dataIn)
    elif number == 11:
        return fe.extractVOrder(dataIn,vOrder)
    elif number == 12:
        return fe.extractWL(dataIn)
    elif number == 13:
        return fe.extractDASDV(dataIn)
    elif number == 14:
        return fe.extractZC(dataIn)
    elif number == 15:
        return fe.extractSSC(dataIn)
    elif number == 16:
        return fe.extractAAC(dataIn)
    elif number == 17:
        return fe.extractFFT(dataIn)
        
##pickleIn = open("dataBin.pickle","rb")
##e = pickle.load(pickleIn)
##
##
##
##x = np.array(e["Open"].getEMGData())
##y = selectFeatures(None,x,number = 1)
##print(y)

##temp = []
##temp.append([])
##for q in range(0,len(x)):
##    y = [int(i) for i in x[q]]
##    temp.append(y)
##
##print(temp)
##z = map(int,x)
##print(z)
##zz = set(z)
##print(zz)
###fe.extractRMS(x)
