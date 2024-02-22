from __future__ import print_function # use python 3 syntax but make it compatible with python 2
import brickpi3 # type: ignore
from RobotGyro import Gyro
import math

import time

BP = brickpi3.BrickPi3()
BP.reset_all()

class Robot:
    def __init__(self):
        
        self.gyro = Gyro()
        self.heading = self.gyro.heading()
        self.wheelDia = 4.07 # 

        
    def moveForward(self, speed):
        try:
            while True:
                BP.set_motor_dps(BP.PORT_B, speed)
                BP.set_motor_dps(BP.PORT_C, speed)
                # try:
                #     print(self.heading, end="\r")   # print the gyro sensor values
                # except brickpi3.SensorError as error:
                #     print(error)

        except KeyboardInterrupt:
            BP.reset_all() 
    def turnDeg(self, speed, degrees): # this function usless now?
        motorDeg = 2.4 * degrees

        try:

            BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
            BP.set_motor_limits(BP.PORT_B, 90, speed)

            BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))
            BP.set_motor_limits(BP.PORT_C, 90, speed) 

            while True:
                self.gyro.printHeading()
    
                BP.set_motor_position(BP.PORT_B, motorDeg)
                    
                BP.set_motor_position(BP.PORT_C, -motorDeg)

        except KeyboardInterrupt:
            BP.reset_all()
    def gyroTurn(self, speed, degrees):

        direction = -1
        if degrees > 0:
            direction = 1

        gain = 15
        
        try:
            
            self.gyro.reset()
            
            time.sleep(2)
            #print(degrees)
            while abs(self.gyro.heading())  + 5 < abs(degrees) :
                self.gyro.printHeading()
                BP.set_motor_dps(BP.PORT_B, speed * direction)
                BP.set_motor_dps(BP.PORT_C, speed * -direction)
            
            start = time.perf_counter()
            
            
            while (time.perf_counter() - start) < 3:
                currentOffset = degrees - self.gyro.heading()
                
                self.gyro.printHeading()
                BP.set_motor_dps(BP.PORT_B, gain * currentOffset * 1)
                BP.set_motor_dps(BP.PORT_C, gain * currentOffset * -1)

            BP.set_motor_dps(BP.PORT_B, 0)
            BP.set_motor_dps(BP.PORT_C, 0)
            
            time.sleep(3)
            
            


        except KeyboardInterrupt:
            BP.reset_all()

    def drive(self):
        try:
            while True:
                BP.set_motor_dps(BP.PORT_B, -150)
                BP.set_motor_dps(BP.PORT_C, 350)
        except KeyboardInterrupt:
            BP.reset_all()
    
    def driveStraightDist(self, speed, dist):

        degrees = round((360 * dist) / (math.pi * self.wheelDia))
        
        try:
            
            self.gyro.reset()
            
            BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
            BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))

            gain = 10
            gain2 = 15
            average = 0
            

            while average < degrees - 3:
                
                
                currentOffset = self.gyro.heading()
                

                BP.set_motor_dps(BP.PORT_B, speed - gain * currentOffset)
                BP.set_motor_dps(BP.PORT_C, speed + gain * currentOffset)

                average = (BP.get_motor_encoder(BP.PORT_B) + BP.get_motor_encoder(BP.PORT_C)) / 2
                


            start = time.perf_counter()
            while (time.perf_counter() - start) < 3:
                currentOffset = degrees - average
                BP.set_motor_dps(BP.PORT_B, gain2 * currentOffset)
                BP.set_motor_dps(BP.PORT_C, gain2 * currentOffset)
                average = (BP.get_motor_encoder(BP.PORT_B) + BP.get_motor_encoder(BP.PORT_C)) / 2
                

            BP.set_motor_dps(BP.PORT_B, 0)
            BP.set_motor_dps(BP.PORT_C, 0)
            time.sleep(3)

           
                
        
        except KeyboardInterrupt:
            BP.reset_all()


    def getHeading(self):

        try:
            while True:
                
                self.gyro.printHeading()
        except KeyboardInterrupt:
            BP.reset_all()

    def updateHeading(self):

        try:
            self.heading = self.gyro.heading()
        except KeyboardInterrupt:
            BP.reset_all()

