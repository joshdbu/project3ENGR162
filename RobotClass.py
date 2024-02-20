from __future__ import print_function # use python 3 syntax but make it compatible with python 2
import brickpi3 # type: ignore
from RobotGyro import Gyro

import time

BP = brickpi3.BrickPi3()
BP.reset_all()

class Robot:
    def __init__(self):
        
        self.gyro = Gyro()
        self.heading = self.gyro.heading()

        
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

        self.direction = -1
        if degrees > 0:
            self.direction = 1

        gain = 15
        
        try:

            self.gyro.reset()

            while abs(self.gyro.heading())  + 5 < abs(degrees) :
                self.gyro.printHeading()
                BP.set_motor_dps(BP.PORT_B, speed * self.direction)
                BP.set_motor_dps(BP.PORT_C, speed * -self.direction)
            
            start = time.perf_counter()
            
            while True:
            # while (time.perf_counter() - start) < 5:
                currentOffset = degrees - self.gyro.heading()
                self.gyro.printHeading()
                BP.set_motor_dps(BP.PORT_B, gain * currentOffset * -self.direction)
                BP.set_motor_dps(BP.PORT_C, gain * currentOffset * self.direction)

            BP.set_motor_dps(BP.PORT_B, 0)
            BP.set_motor_dps(BP.PORT_C, 0)


        except KeyboardInterrupt:
            BP.reset_all()

    
    def getHeading(self):

        try:
            while True:
                print("current heading is:")
                self.gyro.printHeading()
        except KeyboardInterrupt:
            BP.reset_all()
