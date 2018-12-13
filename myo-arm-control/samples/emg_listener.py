import sys
sys.path.append('../lib/')

from device_listener import DeviceListener2

class EmgListener(DeviceListener2):
	def on_emg(self,emg):
		#print("EMG Data: ",emg)
		
		return emg