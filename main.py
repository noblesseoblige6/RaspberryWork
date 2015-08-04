from serial import Serial
import RPi.GPIO as GPIO
import time
import math 
import sys 

def MotorBehavior(interval, lpins, rpins, op):
  signales = [
      [GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.LOW],
      [GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.LOW],
      [GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.LOW],
      [GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.HIGH]
      ]
  if op == 'f':
    for i in range(4):
      GPIO.output(lpins[0], signales[i][0])
      GPIO.output(rpins[0], signales[i][0])

      GPIO.output(lpins[1], signales[i][1])
      GPIO.output(rpins[1], signales[i][1])
      
      GPIO.output(lpins[2], signales[i][2])
      GPIO.output(rpins[2], signales[i][2])

      GPIO.output(lpins[3], signales[i][3])
      GPIO.output(rpins[3], signales[i][3])
      time.sleep(interval)
  elif op == 'b':
    for i in range(4):
      GPIO.output(lpins[3] ,signales[i][0])
      GPIO.output(lpins[2] ,signales[i][1])
      GPIO.output(lpins[1] ,signales[i][2])
      GPIO.output(lpins[0] ,signales[i][3])
      time.sleep(interval)
  elif op == 'l':
    for i in range(4):
      GPIO.output(rpins[0] ,signales[i][0])
      GPIO.output(rpins[1] ,signales[i][1])
      GPIO.output(rpins[2] ,signales[i][2])
      GPIO.output(rpins[3] ,signales[i][3])
      time.sleep(interval)
  elif op == 'r':
    for i in range(4):
      GPIO.output(lpins[0] ,signales[i][0])
      GPIO.output(lpins[1] ,signales[i][1])
      GPIO.output(lpins[2] ,signales[i][2])
      GPIO.output(lpins[3] ,signales[i][3])
      time.sleep(interval)

def findRad(op):
  rot =5.0
  rWheel = 30.0
  wBody = 200.0
  deg2rad = math.pi/180.0
  robotRad = rWheel/wBody*rot*deg2rad

  if op == 'r':
    return robotRad
  elif op == 'l':
    return -robotRad

class EnhancedSerial(Serial):
  def __init__(self, *args, **kwargs):
    #ensure that a reasonable timeout is set
        timeout = kwargs.get('timeout',0.1)
        if timeout < 0.01: timeout = 0.1
        kwargs['timeout'] = timeout
        Serial.__init__(self, *args, **kwargs)
        self.buf = ''
  
  def readline(self, maxsize=None, timeout=1):
    """maxsize is ignored, timeout in seconds is the max time that is way for a complete line"""
    tries = 0
    while 1:
        self.buf += self.read(512)
        pos = self.buf.find('\n')
        if pos >= 0:
            line, self.buf = self.buf[:pos+1], self.buf[pos+1:]
            return line
        tries += 1
        if tries * self.timeout > timeout:
            break
    line, self.buf = self.buf, ''
    return line

  def readlines(self, sizehint=None, timeout=1):
      """read all lines that are available. abort after timout
        when no more data arrives."""
      lines = []
      while 1:
          line = self.readline(timeout=timeout)
          if line:
              lines.append(line)
          if not line or line[-1:] != '\n':
              break
      return lines

if __name__=='__main__':
  PORT = '/dev/ttyUSB0'
  oPinsR = [8, 25, 24, 23]
  oPinsL = [12, 16, 20, 21]
  # s = EnhancedSerial(PORT)
  timeInterval = 0.01
  op = '' 
  GPIO.setmode(GPIO.BCM)
  for i in oPinsR+oPinsL:
    GPIO.setup(i, GPIO.OUT)
  rad = 0 
  iRad = (math.pi*3)/2.0
  e = 1e-3
  while True:
    # sys.stdout.write("\r%f" % rad) 
    # sys.stdout.flush() 
    # tmp = s.readline(timeout=0.001)
    forward = True
    if abs(rad - iRad) > math.pi*0.5:
      rad += math.pi
      forward = False
      if(rad == math.pi*2):
        rad = 0
    
    if rad - iRad < -e:
      MotorBehavior(timeInterval, oPinsL, oPinsR, 'r') 
      print "R"
      rad += findRad('r') 
      rad = rad-2*math.pi if rad >= 2*math.pi else rad 
    elif rad - iRad > e:
      MotorBehavior(timeInterval, oPinsL, oPinsR, 'l') 
      print "L"
      rad += findRad('l') 
      rad = 2*math.pi-rad if rad < 0.0 else rad 
    else:
      if forward:
        print "F"
        MotorBehavior(timeInterval, oPinsL, oPinsR, 'f') 
      else:
        print "B"
        MotorBehavior(timeInterval, oPinsL, oPinsR, 'b') 
      
GPIO.cleanup()
