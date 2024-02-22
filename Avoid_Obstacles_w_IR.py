# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 13:05:59 2024

@author: Elizabeth
"""

import brickpi3 
import ir_sensor_readings  # gets IR values
from RobotClass import Robot
from MPU9250 import MPU9250

# Initialize the MPU9250 library
mpu9250 = MPU9250()

BP = brickpi3.BrickPi3()
careBot = Robot()

# Reset encoders to 0
BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))

radius = 10; # given radius to avoid in cm
point = [200, 150] # point to drive to
[x, y] = point
newRadius = radius + 1.5 # gives extra room for error when going around obs.

# Calculate angle to reach final point. Turn robot in that direction
angle = math.degrees(math.atan(y / x))
careBot.gyroTurn(200, angle)

try:
    while True:
        [sensor_1, sensor_2] = ir_sensor_readings()  # gets values of IR sensor
        [x, y, z] = mpu9250.readMagnet()
        avgSensorVal = (sensor_1 + sensor_2) / 2 # finds avg value of IR sensors
        avgSensorDist = (avgSensorVal - 163) / -2.76 # distance from IR beacon in cm
        magVal = x
        magDistance = -4.581 * math.log(magVal) + 30.833 # distance from magnet in cm
        
        if ((avgSensorDist <= newRadius) || (magDistance <= newRadius)):   # goes around obstacle
            print("within radius")
            
            careBot.gyroTurn(200, -90)
            careBot.driveStraightDist(newRadius)
            careBot.gyroTurn(200, 90)
            careBot.driveStraightDist(2 * newRadius)
            careBot.gyroTurn(200, 90)
    
            # Before driving back to line, check to make sure obstacle has been passed.
            # Maxes out at driving an additional distance '1.5 * radius' to prevent errors.
            count = 0
            while ((avgSensorDist <= newRadius) || (magDistance <= newRadius)) && (count < 3):
                careBot.gyroTurn(200, -90)
                careBot.driveStraightDist(newRadius / 2)
                careBot.gyroTurn(200, 90)
                count += 1
            
            careBot.driveStraightDist(newRadius)
            careBot.gyroTurn(200, -90)
            
        else:     # drives to point when no obstacle is detected
            print("not within radius")
            careBot.moveForward(200)
        time.sleep(0.02)
    
except KeyboardInterrupt:
    BP.reset_all()
