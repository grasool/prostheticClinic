#Convolutional Neural Network for emg data

#Test Script 2 
import Algorithms as alg
from DataIO import DataIO
import FeatureExtraction as featExt
import os
import numpy as np
import random
import sys
from itertools import combinations as comb

import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from keras.layers.core import Dropout
import matplotlib.pylab as plt

movements= ["Open", "Rest","Closed"]
path = ""
try:
    path = sys.argv[1]
except:
    path = os.getcwd()+ "\\Data2" #Path to CSVs
dataSets = {}

dio = DataIO(movements,ctp=70)
dataDir = dio.folderToBin(path) #only necessary when bins have not been created
#print(dataDir)
#dataDir = "pickled_Data2"
#print(os.listdir(dataDir))

contents = os.listdir(dataDir)
numDataSets = len(contents)
print(numDataSets)
fe = featExt.FeatureExtraction()


def convertToIntMatrix(dataIn):
        #needs numpy package
        temp = []
        for q in range(0,len(dataIn)):
            y = np.array([int(i) for i in dataIn[q]])
            temp.append(y)
        return np.array(temp)

f = [1,2,3,4,5,6,7,8,9,10,12,14,16]
c = "4"


#f = range(1,16)
#c = "AllFeatures"


#f = [1]
#c = "RMS"
#array of features to extract
featuresToExtract = f
#classifier name - What to name the LDA
classifierName = c

numFeatures = len(featuresToExtract)

def createFeatureDict(dataBin):
    temp = []
    featureExtDict = {}
    for i in range(0,len(movements)):
        temp = []
        tempEMGData = convertToIntMatrix(dataBin[movements[i]].getEMGData())
        for num in featuresToExtract:
            temp.append(featExt.selectFeatures(None,tempEMGData,number = num))
        featureExtDict[movements[i]] = temp
    
    return featureExtDict

def getDataSets():
    dirList = os.listdir(dataDir)
    #print(dirList)
    dataSets = {}
    for i in dirList:
        num,trash = i.split(".")
        trash,num = num.split("test")
        dataSets[num] = createFeatureDict(dio.getDataBin(dataDir + "\\" + i,cwd = False))
    return dataSets 
    
dataSets = getDataSets()
#print(dataSets["17"])
#the above, has a third index pointer to get a specific extracted feature

def createFeatArray(movement,iD):
    featureArray = []
    for j in range(numFeatures):
        
        null,dtype = contents[iD - 1].split("_")
        null,dtype = dtype.split("test")
        dtype,null = dtype.split(".")
        
        temp = dataSets[str(dtype)][movement][j]
        #featureArray = list(np.hstack((featureArray,temp)))
        featureArray.append(temp)
    return featureArray



def chooseTrainTestSets(testSetSize):
    #There is definitely a better way to choose and remove values
    #this works for now
    arr = list(range(1,numDataSets + 1))
    testSet = random.sample(range(1,numDataSets),testSetSize)
    for e in testSet:
        arr.remove(e)
    return arr,testSet


def createSets(size = 2, trainIndex = [], testIndex = []):
    if len(trainIndex) == 0:
        trainIndex,testIndex = chooseTrainTestSets(size)
        print("Train numbers: " + str(trainIndex))
        print('Test numbers: ' + str(testIndex))
    
   
    arr = []
    labelsTest = []
    for mov in range(len(movements)):
        #print(mov)
        for j in testIndex:
            #print(j)
            arr.append(createFeatArray(movements[mov],j))
            labelsTest.append(mov)
    test = np.array(arr)
    #print(test)
    #print(labelsTest)
    labelsTrain = []
    arr = []
    for mov in range(len(movements)):
        for j in trainIndex:
            arr.append(createFeatArray(movements[mov],j))
            labelsTrain.append(mov)
    #print(arr)
    #print(createFeatArray("",1))
    train = np.array(arr)
    #print(train)
    #print(labelsTrain)
    return train, labelsTrain, test, labelsTest

testSetSize = int(numDataSets*.3) #30% of the data should be for training
train, trainLabels, test, testLabels = createSets(size = testSetSize)
        

trainLabels = keras.utils.to_categorical(trainLabels)
testLabels = keras.utils.to_categorical(testLabels)
   
model = Sequential()
model.add(LSTM(150, input_shape=(train.shape[1],train.shape[2]), dropout_U=0.3))
model.add(Dense(100))
model.add(Dropout(0.2))
model.add(Dense(len(movements), activation="softmax"))
model.compile(loss="categorical_crossentropy",
                  optimizer="adam",
                  metrics=["accuracy"])
model.summary()

epochs = 10
model.fit(train,trainLabels, epochs=epochs, verbose=1)
model.save("testEMGLSTM.h5")
score = model.evaluate(x = test,y = testLabels, verbose=1)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

def fullTest():
    
    results = []
    arrInit = list(range(1,numDataSets + 1))
    x = list(comb(arrInit,3))
    for i in x:
        arr = arrInit.copy()
        for e in i:
            arr.remove(e)
        train, trainLabels, test, testLabels =createSets(trainIndex = arr, testIndex = i)
        trainLabels = keras.utils.to_categorical(trainLabels)
        testLabels = keras.utils.to_categorical(testLabels)
        
        model.fit(train,trainLabels, epochs=epochs, verbose=1)
        #results.append(LDA.getScore(test,testLabels))
    #accuracy = np.mean(results)
    #print("Accuracy: ",accuracy)
#fullTest()

