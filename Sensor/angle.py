import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import time
import math

SETTINGS_FILE = "RTIMULib"

print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
  print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)

print("IMU Name: " + imu.IMUName())

if (not imu.IMUInit()):
    print("IMU Init Failed")
    sys.exit(1)
else:
    print("IMU Init Succeeded")

# this is a good time to set any fusion parameters

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(False)

poll_interval = imu.IMUGetPollInterval()
print("Recommended Poll Interval: %dmS\n" % poll_interval)

g2mPerSecSq = 9.806650000008927
rad2deg = 20*180.0/math.pi; 
angle = 0.0
DT = 0.001

while True:
  if imu.IMURead():
    accel = imu.getAccel() 
    gyro = imu.getGyro()
    #@comment convert tuole to float
    accel = [float(i) * g2mPerSecSq  for i in accel]
    gyro = [float(i) * rad2deg  for i in gyro]
    angle += gyro[2]*DT
    sys.stdout.write("\r%f" % angle)
    sys.stdout.flush()
    # print(accel)
    # print(gyro)    
    time.sleep(poll_interval*1.0/1000.0)

