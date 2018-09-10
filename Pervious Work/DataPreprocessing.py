#Data_Preprocessing Python Arm
from DataIO import DataIO
import FeatureExtraction as featExt
import os,random
import numpy as np

class DataPreprocessing:
    def __init__(self,path,movements,features,ctp = 100):
        self.movements = movements
        self.features = features
        self.dio = DataIO(movements, ctp = ctp)
        self.path = self.dio.folderToBin(path)
        self.dataDir = os.listdir(self.path)
        self.numDataSets = len(self.dataDir)
        

    #Formats datatypes of data being read from pickled databins
    def convertToIntMatrix(self,dataIn):
        #needs numpy package
        temp = []
        for q in range(0,len(dataIn)):
            y = np.array([int(i) for i in dataIn[q]])
            temp.append(y)
        return np.array(temp)

    #extracts the specfic features and creates a dictionary entry based on the mov
    #This can be combined with 'getDataSets()' as it is only called once
    def createFeatureDict(self,dataBin):
        temp = []
        featureExtDict = {}
        for i in range(0,len(self.movements)):
            temp = []
            tempEMGData = self.convertToIntMatrix(dataBin[self.movements[i]].getEMGData())
            for num in self.features:
                temp.append(featExt.selectFeatures(None,tempEMGData,number = num))
            featureExtDict[self.movements[i]] = temp
        
        return featureExtDict

    #Retrieves/creates the full dataset of movements
    #can be combined with 'createFeatureDict'
    def getDataSets(self):
        dataSets = {}
        #goes through all pickled objects in the bin folder
        for i in self.dataDir:
            num,trash = i.split(".")
            trash,num = num.split("test")
            dataSets[num] = self.createFeatureDict(
                self.dio.getDataBin(self.path + "\\" + i,cwd = False))
        return dataSets

    #Concatenates feature array of a specific file in one large array
    def createFeatArray(self,movement,iD):
        featureArray = []
        dataSets = self.getDataSets()
        for j in range(len(self.features)):
            null,dtype = self.dataDir[iD - 1].split("_")
            null,dtype = dtype.split("test")
            dtype,null = dtype.split(".")
            
            temp = dataSets[str(dtype)][movement][j]
            featureArray = list(np.hstack((featureArray,temp)))
        return featureArray

    #randomly chooses which sets are training / test sets
    def chooseTrainTestSets(self,testSetSize):
        #There is definitely a better way to choose and remove values
        #this works for now
        arr = list(range(1,self.numDataSets + 1))
        testSet = random.sample(range(1,self.numDataSets),testSetSize)
        for e in testSet:
            arr.remove(e)
        return arr,testSet

    #creats train / test sets
    def createSets(self, size = 2, trainIndex = [], testIndex = []):
        if len(trainIndex) == 0:
            trainIndex,testIndex = self.chooseTrainTestSets(size)
            print("Train numbers: " + str(trainIndex))
            print('Test numbers: ' + str(testIndex))
        
        arr = []
        labelsTest = []
        #creates a test set of features from each movement from specific bins
        for mov in self.movements:
            for j in testIndex:
                arr.append(self.createFeatArray(mov,j))
                labelsTest.append(mov)
        test = np.array(arr)
        labelsTrain = []
        arr = []
        #creates a training set of features from each movement from specific bins
        for mov in self.movements:
            for j in trainIndex:
                arr.append(self.createFeatArray(mov,j))
                labelsTrain.append(mov)
        train = np.array(arr)
        return train, labelsTrain, test, labelsTest

    def getDir(self):
        return self.dir

    def getNumSets(self):
        return self.numDataSets


