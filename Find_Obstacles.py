# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 18:04:23 2024

@author: 13017
"""

import brickpi3
import grovepi

import IR_Sensor_Functions # gets IR values
from RobotClass import Robot
from MPU9250 import MPU9250
import math
import time

# Initialize the MPU9250 library
mpu9250 = MPU9250()

BP = brickpi3.BrickPi3()
careBot = Robot()
radius = 10;

time.sleep(5)
# Reset encoders to 0
BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))

try:
    [sensor_1, sensor_2] = IR_Sensor_Functions.IR_Read(grovepi) # gets values of IR sensor
    IR_Sensor_Functions.IR_PrintValues(grovepi)
    [xMag, y, z] = mpu9250.readMagnet() # magnet sensor values

    avgSensorVal = (sensor_1 + sensor_2) / 2 # finds avg value of IR sensors
    avgSensorDist = (avgSensorVal - 163) / 2.76 # distance from IR beacon in cm
    
    if xMag > 0:
        magDistance = -4.581 * math.log(abs(xMag)) + 30.833 # distance from magnet in cm
    else:
        xMag = 1000
    
    if (avgSensorDist <= radius):
        print("within radius of IR")
    elif (magDistance <= radius):  # maybe it's 5 * radius, not just radius 
        print("within radius of magnet")
    
except KeyboardInterrupt:
    BP.reset_all()

    
