from DataIO import DataIO
from FeatureExtraction import FeatureExtraction as featExt
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

#---------------------------------------------------------
#Note: This script is out of date as of 3/9/18
#       refer to the testScript with the highest number
#---------------------------------------------------------

movements = ["Open","Rest","Closed","Flex","Extend","Pronation","Supination"]
movements= ["Open", "Rest","Closed"]
def convertToIntMatrix(dataIn):
        #needs numpy package
        temp = []
        for q in range(0,len(dataIn)):
            y = np.array([int(i) for i in dataIn[q]])
            temp.append(y)
        
        return np.array(temp)
    

dio = DataIO(movements)
path = "Data\ChrisAngelini_test1"
dio.dataToBin(path + ".csv")

retBin = dio.getDataBin(path)
emgData = retBin[movements[0]].getEMGData()
#print(convertToIntMatrix(emgData))

#test extracting current features
#from testExtractFeatures import testRunFeatExt as trfe
#trfe(convertToIntMatrix(emgData))

fe = featExt()
#print()
#print(fe.extractRMS(convertToIntMatrix(emgData)))

featureExtDict = {}
def createFeatureDict():
    temp = []
    for i in range(0,len(movements)):
        temp = []
        tempEMGData = convertToIntMatrix(retBin[movements[i]].getEMGData())
        temp.append(fe.extractRMS(tempEMGData))
        #temp.append(fe.extractIAV(tempEMGData))
        #temp.append(fe.extractMAV(tempEMGData))
        featureExtDict[movements[i]] = temp

    return featureExtDict

#for i in range(len(emgData)):
#    print(convertToIntMatrix(emgData)[i])
#returns feature dictionary 
retDict = createFeatureDict()
#print(retDict[movements[0]])
#testDict = {}

#variable based on the number of features extract
numFeatures = 3
#temp - hardcoded labels
labels = [1,1,1,2,2,2,3,3,3]
def createLabels():
    for i in range(numFeatures*len(movements)):
        labels.append(0)


def createFeatMatrix():
    for i in range(len(movements)):
        temp.append(retDict[movements[i]])
    return temp

#X = np.array(createFeatMatrix())

x = np.array(retDict[movements[0]])
print(x)
#print(len(x))
y = np.array(retDict[movements[1]])
w = np.array(retDict[movements[2]])
z = np.vstack((x,y,w))
print(z)
#z = np.vstack((z,w))
#print(x[3])
#x.append(retDict[movements[1]])

#print(z[1])
##print(len(z))
#dictlist = []
##for key, value in retDict.iteritems():
##    temp = [key,value]
##    dictlist.append(temp)


##print(dictlist)
#print(X[0][0])



def Alg():
    clf = LinearDiscriminantAnalysis()
    clf.fit(z, labels)
    print(clf.predict(z))
    #print(clf)

Alg()


#Dictionary Structure Test
#testDict["joe"] = retDict #Proof that a dictionary of names can
#testDict["Chris"] = ["Hello","World"]
							
#x = list(testDict.keys())
#print(testDict[x[1]])
#print(testDict[x[0]]["Rest"])
