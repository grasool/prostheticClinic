import keyboard
from time import sleep

while True:
    key = keyboard.is_pressed
    try:
        if key('a'):
            print('Keypress found!')
    except:
        pass

    sleep(0.065)
