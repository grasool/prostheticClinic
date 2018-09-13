#Run Pose Movement
import sys
sys.path.append('../lib/')

from myo import Myo
from print_pose_listener import PrintPoseListener
from vibration_type import VibrationType
import struct
import time
import sys
from motion import Motion

motion = Motion()

def checkMovement(pose):
    if pose == 'REST':
        motion.allRest()
    elif pose == 'FINGERS_SPREAD':
	motion.allOpen()
    elif pose == 'FIST':
        motion.allClosed()


def main():
    print('Start Myo for Linux')
	
    listener = PrintPoseListener()
    myo = Myo()

    try:
        myo.connect()
        myo.add_listener(listener)
        myo.vibrate(VibrationType.SHORT)
        while True:
            x = myo.run()
            if x != [] or None:
                print(x)
                checkMovement(x)
				

    except KeyboardInterrupt:
        pass
    except ValueError as ex:
        print(ex)
    finally:
        myo.safely_disconnect()
        print('Finished.')

if __name__ == '__main__':
    main()
