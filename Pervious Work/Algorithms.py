#Algorithms
'''
File is meant to contain all the possible algorithms that could possibly be
implemented.

LDA is currently the algorithm implemented

LSTM is is the next to be implemented

'''
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import pickle

#Saves the Algorithm as a file
def saveAlg(fileName, alg):
    pickleOut = open(fileName + ".pickle","wb")
    pickle.dump(alg, pickleOut)
    pickleOut.close()

#Retrieves the algorithm
def getAlg(fileName):
    pickleIn = open(fileName + ".pickle","rb")
    return pickle.load(pickleIn)

#Linear Discriminant Analysis
class LDA:
    def __init__(self, dataProcess = None):
        self.movements = []
        self.clf = LinearDiscriminantAnalysis()
        self.labels = []
        self.data = []
        self.dp = dataProcess

    def train(self,data,labels):
        self.clf.fit(data,labels)

    def predict(self,data):
        return self.clf.predict(data)

    def saveLDA(self,fileName):
        print(fileName)
        saveAlg(fileName + "_LDA",self.clf)

    def getLDA(self,fileName):
        self.clf = getAlg(fileName + "_LDA")
        return self.clf

    def getScore(self,data,labels):
        return self.clf.score(data,labels)

    def fullLDATest(self):
        results = []
        arrInit = list(range(1,self.dp.getNumSets() + 1))
        x = list(comb(arrInit,3))
        for i in x:
            arr = arrInit.copy()
            for e in i:
                arr.remove(e)
            train, trainLabels, test, testLabels = dp.createSets(trainIndex = arr, testIndex = i)
            self.train(train, trainLabels)
            results.append(self.getScore(test,testLabels))
        accuracy = np.mean(results)
        print("Accuracy: ",accuracy)

    def runRandomTest(self): 
        testSetSize = int(self.dp.getNumSets()*.3) #30% of the data should be for training
        #testSetSize = 0 
        train, trainLabels, test, testLabels = self.dp.createSets(size = testSetSize)
        self.train(train, trainLabels)
        print("Predicted: " + str(self.predict(test)))
        print("Actuals: ", str(testLabels))
        print(self.getScore(test,testLabels))

    def trainFromAll(self,fileName):
        testSetSize = 0 #To train the algorithm on all the datasets
        train, trainLabels, test, testLabels = self.dp.createSets(testSetSize)
        self.train(train, trainLabels)
        self.saveLDA(fileName)

    

class KalmanFilter:
    pass

class ParticleFilter:
    pass

class NeuralNet:
    pass

    
