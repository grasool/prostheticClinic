import serial
import time

ser = serial.Serial()
ser.baudrate = 9600
ser.port = "COM18"
ser.open()
count = 0
try:
    while True:
        ser.write(b'0\n')
        print("CLOSED")
        time.sleep(1)
        ser.write(b'1\n')
        print("OPEN")
        time.sleep(1)
        ser.write(b'2\n')
        print("REST")
        time.sleep(1)
finally:
    ser.close()
