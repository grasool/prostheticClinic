#Run Custom demo movements
import tty, termios, sys, time, os
from motion import Motion

m = Motion()
def getchar():
   #Returns a single character from standard input
   
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch
   
def switch(letter = ''):
	letter = getchar()
	print(letter)
        if letter == '1':
		m.allOpen()
	elif letter == '2':
		m.allClosed()
	elif letter == '3':
		m.allRest()
	elif letter == '4':
		m.initialize()
	elif letter == '5':
		m.pinkyOut()
	elif letter == '6':
		m.rockOut()
	elif letter == '7':
		m.cycleFingersEcho()
	elif letter == '8':
		m.cycleFingerSeq()
	elif letter == '9':
		m.middleFinger()
        elif letter == '0':
                m.pointerFinger()
        elif letter == 'z':
                m.openWrist()
        elif letter == 'x':
                m.closedWrist()
        elif letter == 'p':
               # m.pointer(600)
                pass
        elif letter == '[':
                #m.pointer(150)
                pass
        elif letter == 'q' or letter == 'c':
		return True
	return False

def printMove():
	print("Motion List:\n")
	print("1:Open\n2:Closed\n3:Rest\n4:Init\n5:PinkyOut")
        print("6:RockOut\n7:FingersEcho\n8:FingersSeq\n9:Middle\n0:pointerFinger")
        print("\nq:quit\n")
 
m.allOpen()
exit = False
while not exit:
	printMove()
	exit = switch()
	
	
