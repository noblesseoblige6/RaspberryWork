import smbus
import time

def convertAccel(h, l):
  out = 0
  if h & 0b10000000 == 0b10000000:
    val = (h<<8) | l
    val_inv = val^0b1111111111111111
    val_inv = val_inv+1
    out = val_inv*(-1)
  else:
    out = (h<<8) | l

  # return 2.0*out/32768.0
  return out


def convertGyro(h, l):
  out = 0
  if h & 0b10000000 == 0b10000000:
    val = (h<<8) | l
    val_inv = val^0b1111111111111111
    val_inv = val_inv+1
    out = val_inv*(-1)
  else:
    out = (h<<8) | l

  # return 250.0*out/32768.0
  return out

#@comment Initialize
busNumber = 1
addr = 0x68
bus = smbus.SMBus(busNumber)
#@comment Wake up sensors
bus.write_byte_data(addr, 0x6b, 0b00000000)
bus.write_byte_data(addr, 0x6c, 0b00000000)
#@comment config gyro
bus.write_byte_data(addr, 0x1b, 0x00)
# bus.write_byte_data(addr, 0x1b, 0b11100000)
#@comment accel
# bus.write_byte_data(addr, 0x1c, 0b11100000)
bus.write_byte_data(addr, 0x1c, 0x00)

while True:
  accels = bus.read_i2c_block_data(addr, 0x3b, 6)
  accelX = convertAccel(accels[0], accels[1])
  accelY = convertAccel(accels[2], accels[3])
  accelZ = convertAccel(accels[4], accels[5])

  gyoros = bus.read_i2c_block_data(addr, 0x43, 6)
  gyoroX = convertGyro(gyoros[0], gyoros[1])
  gyoroY = convertGyro(gyoros[2], gyoros[3])
  gyoroZ = convertGyro(gyoros[4], gyoros[5])

  print accelX, accelY, accelZ
  print gyoroX, gyoroY, gyoroZ
  print 
  time.sleep(0.5)
