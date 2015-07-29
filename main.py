from serial import Serial
import RPi.GPIO as GPIO
import time

def MotorBehavior(interval, pins, op):
  signales = [
      [GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.LOW],
      [GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.LOW],
      [GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.LOW],
      [GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.HIGH]
      ]
  if op == 'w':
    for i in range(4):
      GPIO.output(pins[0], signales[i][0])
      GPIO.output(pins[1], signales[i][1])
      GPIO.output(pins[2], signales[i][2])
      GPIO.output(pins[3], signales[i][3])
      time.sleep(interval)
  elif op == 's':
    for i in range(4):
      GPIO.output(pins[3] ,signales[i][0])
      GPIO.output(pins[2] ,signales[i][1])
      GPIO.output(pins[1] ,signales[i][2])
      GPIO.output(pins[0] ,signales[i][3])
      time.sleep(interval)
  elif op == 'x':
    for i in range(4):
      GPIO.output(pins[i], GPIO.LOW)

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
  oPinsR = [23, 24, 25, 8]
  oPinsL = [12, 16, 20, 21]
  s = EnhancedSerial(PORT)
  timeInterval = 0.05
  op = '' 
  GPIO.setmode(GPIO.BCM)
  for i in oPinsR+oPinsL:
    GPIO.setup(i, GPIO.OUT)

  while True:
    tmp = s.readline(timeout=0.001)
    if tmp == '':
      tmp = op;
    print tmp, op
    #@comment Motor behavior
    if tmp == 'q':
      break
    elif tmp == 'f':
      MotorBehavior(timeInterval, oPinsR, 'w') 
      MotorBehavior(timeInterval, oPinsL, 'w') 
      if  op != 'f':
        op = tmp
    elif tmp == 'b':
      MotorBehavior(timeInterval, oPinsR, 's') 
      MotorBehavior(timeInterval, oPinsL, 's') 
      if  op != 'b':
        op = tmp
    elif tmp == 'r':
      MotorBehavior(timeInterval, oPinsR, 'w') 
      MotorBehavior(timeInterval, oPinsL, 'x') 
      if op != 'r':
        op = tmp
    elif tmp == 'l':
      MotorBehavior(timeInterval, oPinsR, 'x') 
      MotorBehavior(timeInterval, oPinsL, 'w') 
      if  op != 'l':
        op = tmp

GPIO.cleanup()
