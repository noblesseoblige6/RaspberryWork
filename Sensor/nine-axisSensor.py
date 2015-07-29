import smbus
import time

def mergeHL(h, l):
  out = 0
  if h & 0b10000000 == 0b10000000:
    val = (h<<8) | l
    val_inv = val^0b1111111111111111
    val_inv = val_inv+1
    out = val_inv*(-1)
  else:
    out = (h<<8) | l
  return out/256.0 
  

#@comment Initialize
busNumber = 1
addr = 0x68
bus = smbus.SMBus(busNumber)
#@comment Wake up sensors
bus.write_byte_data(addr, 0x6b, 0x00)
bus.write_byte_data(addr, 0x6c, 0x00)

# bus.write_byte_data(addr, 0x1b, 0x00)
bus.write_byte_data(addr, 0x1b, 0x18)
bus.write_byte_data(addr, 0x1c, 0x18)

while True:
  accels = bus.read_i2c_block_data(addr, 0x3b, 6)
  accelX = mergeHL(accels[0], accels[1])
  accelY = mergeHL(accels[2], accels[3])
  accelZ = mergeHL(accels[4], accels[5])

  gyoros = bus.read_i2c_block_data(addr, 0x43, 6)
  gyoroX = mergeHL(gyoros[0], gyoros[1])
  gyoroY = mergeHL(gyoros[2], gyoros[3])
  gyoroZ = mergeHL(gyoros[4], gyoros[5])

  print accelX, accelY, accelZ
  print gyoroX, gyoroY, gyoroZ
  print 
  time.sleep(0.5)
