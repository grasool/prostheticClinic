import sys
sys.path.append('../lib/')

from myo import Myo
from print_pose_listener import PrintPoseListener
from emg_listener import EmgListener
from vibration_type import VibrationType
import struct
import time
import sys

def main():
    print('Start Myo for Linux')
    param = 0
    if len(sys.argv) > 1:
        param = sys.argv[1]
	
	listener = PrintPoseListener()
    if param == 1:
        listener = EmgListener()
	    
    myo = Myo()

    try:
        myo.connect()
        myo.add_listener(listener)
        myo.vibrate(VibrationType.SHORT)
        while True:
            x = myo.run()
            if x != [] or None:
                print(x)
				

    except KeyboardInterrupt:
        pass
    except ValueError as ex:
        print(ex)
    finally:
        myo.safely_disconnect()
        print('Finished.')

if __name__ == '__main__':
    main()
