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
    def turnDeg(self, speed, degrees):
        print("do we get here")
        motorDeg = 2.4 * degrees

        try:
            while True:
                
                print("what about here")
                BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
                BP.set_motor_limits(BP.PORT_B, 90, speed)
                BP.set_motor_position(BP.PORT_B, motorDeg)
                    
                BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))
                BP.set_motor_limits(BP.PORT_C, 90, speed) 
                BP.set_motor_position(BP.PORT_C, -motorDeg)

                start = time.perf_counter()

                while (time.perf_counter() - start) < 20:
                    print(time.perf_counter() - start)
                
                # while True:
                # while abs(BP.get_motor_encoder(BP.PORT_B) - motorDeg) > 1:
                #     self.gyro.printHeading()
        except KeyboardInterrupt:
            BP.set_motor_dps(BP.PORT_B, 0)
            BP.set_motor_dps(BP.PORT_C, 0)
            BP.reset_all()
    def getHeading(self):

        try:
            while True:
                
                self.gyro.printHeading()
        except KeyboardInterrupt:
            BP.set_motor_dps(BP.PORT_B, 0)
            BP.set_motor_dps(BP.PORT_C, 0)
            BP.reset_all()
