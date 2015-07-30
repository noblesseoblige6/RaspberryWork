from serial import Serial
import RPi.GPIO as GPIO
import time

def nSignal(index):
  index+=1
  if index >= 4:
    return 0
  return index

def pSignal(index):
  index-=1
  if index < 0:
    return 3
  return index

def MotorBehavior(interval, lpins, rpins, lh, rh):
  signales = [
      [GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.LOW],
      [GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.LOW],
      [GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.LOW],
      [GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.HIGH]
      ]
  for i in range(4):
    GPIO.output(lpins[i], signales[lh][i])
    GPIO.output(rpins[i], signales[rh][i])


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
  
  rMotorH = 0 
  lMotorH = 0

  while True:
    tmp = s.readline(timeout=0.001)
    # if tmp == '':
    #   tmp = op;
    print tmp, op
    #@comment Motor behavior
    if tmp == 't':
      break
    elif tmp == 'f':
      rMotorH = nSignal(rMotorH)
      lMotorH = nSignal(lMotorH)
      if  op != 'f':
        op = tmp
    elif tmp == 'b':
      rMotorH = pSignal(rMotorH)
      lMotorH = pSignal(lMotorH)
      if  op != 'b':
        op = tmp
    elif tmp == 'r':
      rMotorH = nSignal(rMotorH)
      lMotorH = pSignal(lMotorH)
      if op != 'r':
        op = tmp
    elif tmp == 'l':
      rMotorH = pSignal(rMotorH)
      lMotorH = nSignal(lMotorH)
      if  op != 'l':
        op = tmp
    elif tmp == 's':
      if  op != 's':
        op = tmp
    MotorBehavior(timeInterval, oPinsL, oPinsR, rMotorH, lMotorH) 
GPIO.cleanup()
