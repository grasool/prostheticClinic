import keyboard
from time import sleep
from motion import Motion

def print_instructions():
    print('\n\n' + '='*40 + '\n' + 'Press \'1\' to select thumb')
    print('Press \'2\' to select index')
    print('Press \'3\' to select middle')
    print('Press \'4\' to select ring')
    print('Press \'5\' to select pinky')
    print('Press \'6\' to select wrist')
    print('Press \'t\' to toggle back and fourth movement')
    print('Press \'Enter\' to increment server position')
    print('Press \'r\' to reprint these instructions')
    print('Press \'Ctrl + C\' to exit')
    print('='*40 + '\n\n')

if __name__ == '__main__':
    m = Motion()
     
    selection = 0
    finger = m.thumb
    pos = m.positions[selection]
    path = -1
    pathname = {1: 'forward', -1:'backward'}
    #press = keyboard.is_pressed
    
    print_instructions()
    while True:
        press = input()
        #press = keyboard.read_key()
        try:
            if press == '1':
                finger = m.thumb
                selection = 0
                pos = m.positions[selection]
                print('Thumb selected')
            elif press == '2':
                finger = m.pointer
                selection = 1
                pos = m.positions[selection]
                print('Index selected')
            elif press == '3':
                finger = m.middle
                selection = 2
                pos = m.positions[selection]
                print('Middle selected')
            elif press == '4':
                finger = m.ring
                selection = 3
                pos = m.positions[selection]
                print('Ring selected')
            elif press == '5':
                finger = m.pinky
                selection = 4
                pos = m.positions[selection]
                print('Pinky selected')
            elif press == '6':
                finger = m.wrist
                selection = 5
                pos = m.positions[selection]
            elif press == 't':
                path *= -1
                print('Finger direction toggled to %s'% pathname[path])
            elif press == 'r':
                print_instructions()
            elif press == '':
                pos += path
                finger(pos)
                pos = m.positions[selection]
                print('Position:', pos)
        except Exception as e:
            if not (type(e) == ImportError):
                print(e)
            else:
                print(e)
                break


        print('Ready')
