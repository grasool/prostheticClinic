import myo as libmyo
import numpy as np
import config

config_data = config.load_config()
SDK_BIN_PATH = config_data['sdk_path']
libmyo.init(dist_path=SDK_BIN_PATH)

class DataBuffer:
	def __init__(self, size=1000, nChans=3, initVal=0):
		self.bufferSize = size
		self.nChans = nChans
		self.initVal = initVal
		
		self.data = initVal*np.ones([nChans,size])

	def push(self,dataVec):
		self.data[:,:-1] = self.data[:,1:]
		self.data[:,-1] = dataVec
		
	def reset_buffer(self):
		self.__init__(self.bufferSize, self.nChans, self.initVal)

class Listener(libmyo.DeviceListener):
    def __init__(self, pyqtApp):
        super(Listener, self).__init__()
        self.emg_enabled = True
        self.pose = libmyo.Pose.rest
        self.rssi = None
        self.locked = False
        self.last_time = 0
        
        self.pyqtApp = pyqtApp
        
        # Data
        self.emg = DataBuffer(nChans=8)
        self.acc = DataBuffer(nChans=3)
        self.orientation = DataBuffer(nChans=4)
        self.gyro = None

    def on_connect(self, myo, timestamp, something):
        myo.set_stream_emg(libmyo.StreamEmg.enabled)
    
    def on_disconnect(self, myo, timestamp, something):
        pass

    def on_pose(self, myo, timestamp, pose):
        #print("In pose...")
        """
        if pose == libmyo.Pose.double_tap:
            myo.set_stream_emg(libmyo.StreamEmg.enabled)
            self.emg_enabled = True
        elif pose == libmyo.Pose.fingers_spread:
            myo.set_stream_emg(libmyo.StreamEmg.disabled)
            self.emg_enabled = False
        """
        self.pose = pose
        #print(str(self.pose))

    def on_rssi(self, myo, timestamp, rssi):
        pass

    def on_event(self, kind, event):
        """
        Called before any of the event callbacks
        """

    def on_event_finished(self, kind, event):
        """
        Called after the respective event callbacks
        """
        self.pyqtApp.update_plots()

    def on_pair(self, myo, timestamp, firmware):
        pass

    def on_orientation_data(self, myo, timestamp, orientation):
        #print "In orientation"
        ori = orientation
        self.orientation.push(np.array([ori.x,ori.y,ori.z,ori.w]))

    def on_accelerometor_data(self, myo, timestamp, acceleration):
        #print "In acc..."
        acc = acceleration
        self.acc.push(np.array([acc[0],acc[1],acc[2]]))

    def on_gyroscope_data(self, myo, timestamp, gyroscope):
        self.gyro = gyroscope 

    def on_unlock(self, myo, timestamp):
        self.locked = False

    def on_lock(self, myo, timestamp):
        self.locked = True

    def on_emg_data(self, myo, timestamp, emg):
        self.emg.push(emg)
