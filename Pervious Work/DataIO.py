#Data input/output
#reads in csvs
#outputs and reads in pickled python objects

'''
Depending on how the EMG Data is collected will determine how the
data should be parsed.


'''
import csv
import pickle
from DataBin import DataBin
import os


class DataIO:
    def __init__(self, movements = [],ctp = 100):
        #self.rawData = []
        self.movements = movements
        self.movDataDic = {}
        self.dataBinDictionary = {}
        self.ctp = ctp

    #Reads in the raw csv from disk
    def csvReader(self,fileName):
        rawData = []
        with open(fileName,newline = '') as file:
            reader = csv.reader(file)
            for row in reader:
               rawData.append(row)
        return rawData

    #Parses the data based on certain deliminters 
    def parseData(self, rawData):
        count = 0
        dataIndex =[]
        for i in range(0,len(rawData)):
            temp = rawData[i][0]
           #print(movements[count])
            if count < len(self.movements) and str(temp) == self.movements[count]:
               dataIndex.append(i+1)
               count = count + 1
            if count == len(self.movements) and str(temp) == 'Rest':
                dataIndex.append(i+1)
       
        #self.movDataDic["index"] = dataIndex
        print(dataIndex)
        dataPoints = dataIndex[1] - dataIndex[0]
        self.dataBinDictionary["dataPoints"] = dataPoints
        print("Length Open: " + str(dataPoints))
        print("Length Rest: " + str(dataIndex[2] -dataIndex[1]))
        print("Length Closed: " + str(dataIndex[3] - dataIndex[2]))
        
        for i in range(0,len(dataIndex) - 1):
            y = dataIndex[i]
            tempData = []
            for y in range(y,y + dataPoints - 10):
                tempX = []
                for x in range(0, len(rawData[y])):
                    tempX.append(rawData[y][x])
                tempData.append(tempX)
            self.movDataDic[self.movements[i]] = tempData

    #Calls DataIO and creates a bin for each movement
    def makeBin(self,personName = "test",dataType = "None"):
        self.dataBinDictionary["Name"] = personName #going to be then name of person parsed from csv
        self.dataBinDictionary["DataSet"] = dataType
        for i in range(0,len(self.movements)):
            temp = self.movDataDic[self.movements[i]]
            temp = self.ctpWindow(temp,self.ctp)
            #add method to calculate ctp here, pass temp (matrix) and truncate quant of rows
            tempEMG = []
            tempGyro = []
            tempAccel = []
            for j in range(0,len(temp)):
                tempEMG.append(temp[j][1:9])
                #tempGyro.append(temp[j][9:12])
                #tempAccel.append(temp[j][12:16])
            self.dataBinDictionary[self.movements[i]] = DataBin(self.movements[i]
                                        ,self.ctp,0,0,tempEMG,tempEMG,tempGyro,tempAccel)

    '''
    Creates a C-Contraction, T-Time, P-Percentage window
    Truncates n/2 percentage from the beginning and end
    '''
    def ctpWindow(self, arr, ctp):
        if ctp < 100:
            adjArr = []
            truncVal = int((100 - ctp)*.01*len(arr)/2)
            for i in range(truncVal,len(arr)-truncVal):
                adjArr.append(arr[i][:])
            return adjArr
        else:
            return arr

    #Saves the full databin to disk
    def saveDataBin(self, fileName):
        pickleOut = open(fileName + ".pickle","wb")
        pickle.dump(self.dataBinDictionary, pickleOut)
        pickleOut.close()
        
    #Retrieve databin from disk
    def getDataBin(self, filePath, cwd = True):
        #print(filePath)
        if cwd:
            fileName,null,null = self.getInfo(filePath)
            filePath = fileName + ".pickle"
        
        pickleIn = open(filePath,"rb")
        return pickle.load(pickleIn)

    #Converts a specific csv to a bin
    def dataToBin(self, filePath, cwd = False, newDir = ""):
        
        self.parseData(self.csvReader(filePath))
        #print(fileName)
        fileName, personName,dataType = self.getInfo(filePath)
        self.makeBin(personName,dataType)
        if cwd:
            filePath = fileName
        else:
            filePath = os.getcwd() + "\\" + newDir + "\\" + fileName
            
        self.saveDataBin(filePath)

    #converts all the data in a folder into a bin
    def folderToBin(self, path):
        dirList = os.listdir(path)
        p = path.split("\\")
        newDir = "pickled_" + p[len(p)-1]
        if not os.path.exists(newDir):
            os.mkdir(newDir)
        for i in dirList:
            self.dataToBin(path + "\\" + i,newDir = newDir)
        return newDir

    #retrieves the information from the file extension
    def getInfo(self,fileName):
        temp = fileName.split("\\")
        fileName,trash = temp[len(temp)-1].split(".")
        personName,dataType = fileName.split("_")
        return fileName,personName,dataType


movements = ["Open","Rest","Closed","Flex","Extend","Pronation","Supination"]
def test():
    dio = DataIO(movements)
    dio.parseData(dio.csvReader("data3"))
    dio.makeBin()
    dio.saveDataBin()

#test()

    
