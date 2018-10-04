from utilities import *
from pose_type import PoseType

class DeviceListener(object):
	movements = {0:'REST',1:'FIST',2:'WAVE_IN',3:'WAVE_OUT',4:'FINGERS_SPREAD',5:'DOUBLE_TAP',255:'UNKNOWN'}
	def handle_data(self, data):
		if data.cls != 4 and data.command != 5:
			return

		connection, attribute, data_type = unpack('BHB', data.payload[:4])
		payload = data.payload[5:]

		if attribute == 0x23:
			data_type, value, address, _, _, _ = unpack('6B', payload)

			if data_type == 3:
				return self.movements[value]
				
	##def on_pose(self, pose):
	##	pass
		
class DeviceListener2(object):
	def handle_data(self, data):
		if data.cls != 4 and data.command != 5:
			return
		
		#print("Full Payload: ",data.payload)
		connection, attribute, data_type = unpack('BHB', data.payload[:4])
		payload = data.payload[5:]
		#print("Listener Payload",payload)
		if attribute == 0x27:
			#print("Listener Payload 0x27",payload)
			#print("Length Payload 0x27",len(payload))
			vals = unpack('8HB', payload)
			#print("Vals: ",vals)
			self.on_emg(vals)
			return vals
	def on_emg(self, emg):
		pass
