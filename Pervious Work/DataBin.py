#Reads in CSV and formats MyoBand data in proper data bins


class DataBin:
    def __init__(self, movement, ctp, sampleTime, totalSamples, RawEMGData, EMGData, gyroData, accelData):
        self.movement = movement #the type of movement the bin is associated with
        self.ctp = ctp #the contraction time percentage used to create windowed data
        self.sampleTime = sampleTime #total time for the movement
        self.totalSamples = totalSamples #total samples for this movement
        self.RawEMGData = RawEMGData #raw EMG Data from collected data
        self.EMGData = EMGData #window based on CTP
        self.gyroData = gyroData #unwindowed raw gyroscope data
        self.accelData = accelData #unwindowed raw accelerometer data

    def getMovement(self):
        return self.movement

    def getCtp(self):
        return self.ctp

    def setCtp(self,val):
        self.ctp = val

    def getSampleTime(self):
        return self.sampleTime

    def getTotalSamples(self):
        return self.totalSamples

    def getRawData(self):
        return self.rawEMGData

    def getEMGData(self):
        return self.EMGData

    def setEMGData(self,data):
        self.EMGData = data

    def getGyroData(self):
        return self.gyroData

    def getAccelData(self):
        return self.accelData


    
        
        
        
        
