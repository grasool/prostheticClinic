#Test Script 2

'''
Test Script made to:
    -create databin from csv
    -read pickled bins
    -create dataset based on specific features to extract
    -manipulate data to be inserted into LDA

This Script should be separated into a data preprocessing script
and another script should be written for the training of other algorithms

'''

import Algorithms as alg
from DataIO import DataIO
import FeatureExtraction as featExt
import os
import numpy as np
import random
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import sys
from itertools import combinations as comb

#The specfic movements that we are working with at the moment
#More to be added
movements= ["Open", "Rest","Closed"]

path = ""
try:
    path = sys.argv[1]
except:
    path = os.getcwd()+ "\\Data2" #Path to CSVs
dataSets = {}

#Create a dataset from the csvs
dio = DataIO(movements,ctp=70)

dataDir = dio.folderToBin(path) #only necessary when bins have not been created
#print(dataDir)
#dataDir = "pickled_Data2"
#print(os.listdir(dataDir))

contents = os.listdir(dataDir)
numDataSets = len(contents)
print(numDataSets)
fe = featExt.FeatureExtraction()

#Formats datatypes of data being read from pickled databins
def convertToIntMatrix(dataIn):
        #needs numpy package
        temp = []
        for q in range(0,len(dataIn)):
            y = np.array([int(i) for i in dataIn[q]])
            temp.append(y)
        return np.array(temp)


#array of features to extract
featuresToExtract = [1,12,14]
#classifier name - What to name the LDA
classifierName = "4"
numFeatures = len(featuresToExtract)

#extracts the specfic features and creates a dictionary entry based on the mov
#This can be combined with 'getDataSets()' as it is only called once
def createFeatureDict(dataBin):
    temp = []
    featureExtDict = {}
    for i in range(0,len(movements)):
        temp = []
        tempEMGData = convertToIntMatrix(dataBin[movements[i]].getEMGData())
        print(len(tempEMGData))
        for num in featuresToExtract:
            temp.append(featExt.selectFeatures(None,tempEMGData,number = num))
        featureExtDict[movements[i]] = temp
    
    return featureExtDict

#Retrieves/creates the full dataset of movements
#can be combined with 'createFeatureDict'
def getDataSets():
    dirList = os.listdir(dataDir)
    #print(dirList)
    dataSets = {}
    #goes through all pickled objects in the bin folder
    for i in dirList:
        num,trash = i.split(".")
        trash,num = num.split("test")
        dataSets[num] = createFeatureDict(dio.getDataBin(dataDir + "\\" + i,cwd = False))
    return dataSets 

#Create dataset    
dataSets = getDataSets()

#Concatenates feature array of a specific file in one large array
def createFeatArray(movement,iD):
    featureArray = []
    for j in range(numFeatures):
        
        null,dtype = contents[iD - 1].split("_")
        null,dtype = dtype.split("test")
        dtype,null = dtype.split(".")
        
        temp = dataSets[str(dtype)][movement][j]
        featureArray = list(np.hstack((featureArray,temp)))
    return featureArray


#randomly chooses which sets are training / test sets
def chooseTrainTestSets(testSetSize):
    #There is definitely a better way to choose and remove values
    #this works for now
    arr = list(range(1,numDataSets + 1))
    testSet = random.sample(range(1,numDataSets),testSetSize)
    for e in testSet:
        arr.remove(e)
    return arr,testSet

#creats train / test sets
def createSets(size = 2, trainIndex = [], testIndex = []):
    if len(trainIndex) == 0:
        trainIndex,testIndex = chooseTrainTestSets(size)
        print("Train numbers: " + str(trainIndex))
        print('Test numbers: ' + str(testIndex))
    
   
    arr = []
    labelsTest = []
    #creates a test set of features from each movement from specific bins
    for mov in movements:
        for j in testIndex:
            arr.append(createFeatArray(mov,j))
            labelsTest.append(mov)
    test = np.array(arr)
    labelsTrain = []
    arr = []
    #creates a training set of features from each movement from specific bins
    for mov in movements:
        for j in trainIndex:
            arr.append(createFeatArray(mov,j))
            labelsTrain.append(mov)
    train = np.array(arr)
    return train, labelsTrain, test, labelsTest

#tests the accuracy of the LDA versus each combination of train / test sets
#n choose m combinations
# this function most likely should be in the 'Algorithms.py' file
def fullLDATest():
    LDA = alg.LDA()
    results = []
    arrInit = list(range(1,numDataSets + 1))
    x = list(comb(arrInit,3))
    for i in x:
        arr = arrInit.copy()
        for e in i:
            arr.remove(e)
        train, trainLabels, test, testLabels =createSets(trainIndex = arr, testIndex = i)
        LDA.train(train, trainLabels)
        results.append(LDA.getScore(test,testLabels))
    accuracy = np.mean(results)
    print("Accuracy: ",accuracy)
 
def runRandomTest(): 
        testSetSize = int(numDataSets*.3) #30% of the data should be for training
        #testSetSize = 0 
        train, trainLabels, test, testLabels = createSets(size = testSetSize)
        LDA = alg.LDA()
        LDA.train(train, trainLabels)
        print("Predicted: " + str(LDA.predict(test)))
        print("Actuals: ", str(testLabels))
        print(LDA.getScore(test,testLabels))
        LDA.saveLDA("testLDA")
        
#Trains the LDA from all the sets of data.
#method should be in the Algorithms file
def trainFromAll():
        testSetSize = 0 #To train the algorithm on all the datasets
        train, trainLabels, test, testLabels = createSets(testSetSize)
        #print(train)
        #print(len(train))
        LDA = alg.LDA()
        LDA.train(train, trainLabels)
        LDA.saveLDA("testAng" + classifierName)
       

       
fullLDATest()       
#runRandomTest()
#trainFromAll()
        

