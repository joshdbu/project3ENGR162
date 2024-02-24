# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 13:05:59 2024

@author: Elizabeth
"""

import brickpi3 
import ir_sensor_readings  # gets IR values
from RobotClass import Robot
from MPU9250 import MPU9250
import math

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
pointDist = math.sqrt(x ** 2 + y ** 2) # distance to the point
newRadius = radius + 1.5 # gives extra room for error when going around obs.

# Calculate angle to reach final point. Turn robot to face that direction.
angle = math.degrees(math.atan(y / x))
careBot.gyroTurn(200, angle)

horizontalDist = 0 # Tracks distance traveled horizontally to subtract from encoder value
totalDist = 0 # Tracks total distance in direction of point
rawDist = 0 # Tracks total distance according to motor encoder

try:
    # Continue looping while the distance traveled in direction of point is less than the calculatd distance to point
    while totalDist < pointDist:
        [sensor_1, sensor_2] = ir_sensor_readings()  # gets values of IR sensor
        [x, y, z] = mpu9250.readMagnet() # magnet sensor values
        avgSensorVal = (sensor_1 + sensor_2) / 2 # finds avg value of IR sensors
        avgSensorDist = (avgSensorVal - 163) / -2.76 # distance from IR beacon in cm
        magDistance = -4.581 * math.log(x) + 30.833 # distance from magnet in cm

        # Drive around obstacle if distance calculated to either type of obstacle is less than radius
        if ((avgSensorDist <= newRadius) || (magDistance <= newRadius)):
            print("within radius")

            # Drive around obstacle
            careBot.gyroTurn(200, -90)
            careBot.driveStraightDist(newRadius)
            careBot.gyroTurn(200, 90)
            careBot.driveStraightDist(2 * newRadius)
            careBot.gyroTurn(200, 90)

            #------------ This part is optional feel free to get rid of it if it's too complicated ----------------
    
            # Before driving back to line, turn back towards obstacle and check to make sure obstacle has been passed.
            # Turn, take measurements and check against radius. Repeat until onstacle is passed. 
            # Should be useful to guard against errors in the functions estimating distance to obstacles.
            # Maxes out at driving an additional distance = radius in case of errors.
            count = 0
            while count < 4:
                sensor_1, sensor_2] = ir_sensor_readings()  # gets values of IR sensor
                [x, y, z] = mpu9250.readMagnet() # magnet sensor values
                avgSensorVal = (sensor_1 + sensor_2) / 2 # finds avg value of IR sensors
                avgSensorDist = (avgSensorVal - 163) / -2.76 # distance from IR beacon in cm
                magDistance = -4.581 * math.log(x) + 30.833 # distance from magnet in cm

                if ((avgSensorDist <= newRadius) || (magDistance <= newRadius)):
                    careBot.gyroTurn(200, -90)
                    careBot.driveStraightDist(newRadius / 4)
                    careBot.gyroTurn(200, 90)
                else:
                    count =  4 # end loop if past obstacle
                count += 1

            #-----------------------------------------------------------------------------------------------------
            
            careBot.driveStraightDist(newRadius)
            careBot.gyroTurn(200, -90)

            horizontalDist += (newRadius * 2) # Add amount of horizontal distance covered while avoiding obstacle
            
        else:  # drives forward when no obstacle is detected
            print("not within radius")
            careBot.moveForward(200)

        avgEncoder = (BP.get_motor_encoder(BP.PORT_B) + BP.get_motor_encoder(BP.PORT_C)) / 2 # average encoder value of each motor
        rawDist = avgEncoder * 4.3 * math.pi # theoretical based on circumference could need slight adjustment
        totalDist = rawDist - horizontalDist 
        time.sleep(0.02)
    
except KeyboardInterrupt:
    BP.reset_all()
