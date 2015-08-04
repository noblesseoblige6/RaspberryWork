'''
convert 'uint8_t' message to 'double' message
'''

# -*- coding: utf-8 -*-
import serial
import time
from ctypes import *

class UNION(Union):
    _fields_ = [("ub",c_ubyte*8),("db",c_double)
                ]


#serial port open
serial_port = serial.Serial('/dev/ttyUSB0',9600)

print 'connection'

#read message
str_bytes = serial_port.read(8)
byte_arr = bytearray(str_bytes)

x = UNION()
x.ub = (c_ubyte*8)(*(byte_arr))
print x.db

##for i in [0,1,2,3,4,5,6,7]:
##    x.ub[i] = str[i]


#print message(not converted)
##print 'not converted: \n%s.\n' %str

#convert the message
#l = float(str.replace(',',''))
#p_c = c_char_p()#create_string_buffer('\000'*4)
##p_d = c_double()

#print message(converted)
##print 'converted: \n%f.\n' %p_d.value

##serial_port.close()
