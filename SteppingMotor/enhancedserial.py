#!/usr/bin/env python
"""Enhanced Serial Port class
part of pyserial (http://pyserial.sf.net)  (C)2002 cliechti@gmx.net

another implementation of the readline and readlines method.
this one should be more efficient because a bunch of characters are read
on each access, but the drawback is that a timeout must be specified to
make it work (enforced by the class __init__).

this class could be enhanced with a read_until() method and more
like found in the telnetlib.
"""

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
    oPins = [23, 24, 25, 8]
    s = EnhancedSerial(PORT)
    timeInterval = 0.01
    char = '' 
    GPIO.setmode(GPIO.BCM)
    for i in oPins:
     GPIO.setup(i, GPIO.OUT)

    while True:
      tmp = s.readline(timeout=0.001)
      print 'char: %s' % char
      print ' tmp: %s\n' % tmp
      if tmp == '':
        tmp = char;

      #@comment Motor behavior
      if tmp == 'q':
        break
      elif tmp == 'w':
       MotorBehavior(timeInterval, oPins, tmp) 
       if  char != 'w':
          char = tmp
      elif tmp == 's':
       MotorBehavior(timeInterval, oPins, tmp) 
       if  char != 's':
          char = tmp
      elif tmp == 'x':
       MotorBehavior(timeInterval, oPins, tmp) 
       if  char != 'x':
          char = tmp
GPIO.cleanup()
