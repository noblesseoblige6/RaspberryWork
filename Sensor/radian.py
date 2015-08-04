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

#@comment this is a good time to set any fusion parameters
imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(False)

poll_interval = imu.IMUGetPollInterval()
print("Recommended Poll Interval: %dmS\n" % poll_interval)

rad2deg = 180.0/math.pi; 
deg2rad = math.pi/(180.0)
rad = 0.0
DT = 1.0

while True:
  if imu.IMURead():
    gyro = imu.getGyro()
    #@comment convert tuole to float
    gyro = [float(i) for i in gyro]
    rad = rad + (gyro[2]*DT)*deg2rad
    sys.stdout.write("\r%f" % rad)
    sys.stdout.flush()
