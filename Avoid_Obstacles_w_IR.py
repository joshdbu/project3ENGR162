# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 13:05:59 2024

@author: Elizabeth
"""

import brickpi3 
import ir_sensor_readings  # gets IR values
import IMU_ReadPrint # gets IMU values
from RobotClass import Robot
BP = brickpi3.BrickPi3()
careBot = Robot()


radius = 10; # given radius to avoid in cm
point = [20, 20] # point to drive to 
newRadius = radius + 1.5 # gives extra room for error when going around obs.
reading = 821 * exp(-0.215 * radius)


while True:
    [sensor_1, sensor_2] = ir_sensor_readings()  # gets values of IR sensor
    [x, y, z] = IMU_ReadPrint()
    avgSensorVal = (sensor_1 + sensor_2) / 2 # finds avg value of IR sensors
    avgSensorDist = (avgSensorVal - 163) / -2.76 # distance from IR beacon in cm
    magVal = x # is this the right value to read? or is it y?
    magDistance = 1 # needs correct equation of mag reading to cm
    
    if ((avgSensorDist <= newRadius) || (magDistance <= newRadius)):     # goes around obstacle
        print("within radius")
        
        careBot.gyroTurn(180, -90)
        careBot.driveStraightDist(newRadius)
        careBot.gyroTurn(180, 90)
        careBot.driveStraightDist(newRadius)
        careBot.gyroTurn(180, 90)
        careBot.driveStraightDist(newRadius)
        careBot.gyroTurn(180, -90)
        careBot.driveToPoint(point)
        
    else:                                 # drives to point when no obstacle is detected
        print("not within radius")
        careBot.driveToPoint(point)
