import serial
import time
import sys

ser = serial.Serial('/dev/ttyUSB0', 9600)
while True:
  inputChar = sys.stdin.readline()
  if inputChar == 'q\n':
    break
  #Sending data
  ser.write('%s' % inputChar)

ser.close()
