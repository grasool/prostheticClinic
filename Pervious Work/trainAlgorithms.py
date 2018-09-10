#trainAlgorithms

from DataPreprocessing import DataPreprocessing as dataProcess
import os
import Algorithms

#The specfic movements that we are working with at the moment
#More to be added

movements= ["Open", "Rest","Closed"]

path = ""
try:
    path = sys.argv[1]
except:
    path = os.getcwd()+ "\\Data2" #Path to CSVs
dataSets = {}


#fe = featExt.FeatureExtraction()
features = [1,2,12,14]
dp = dataProcess(path,movements,features,ctp = 70)

#dp.createSets()
LDA = Algorithms.LDA(dp)
LDA.trainFromAll("testNewRev")
