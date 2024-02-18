import brickpi3
from RobotGyro import Gyro
from __future__ import print_function # use python 3 syntax but make it compatible with python 2
import time

class Robot:
    def __init__(self):
        self.turnSpeed = 50 #random thing
        self.BP = brickpi3.BrickPi3()
        self.gyro = Gyro(3)
        heading = self.gyro.heading()

        
    def moveForward(self, speed):
        try:
            while True:
                self.BP.set_motor_dps(self.BP.PORT_B, speed)
                self.BP.set_motor_dps(self.BP.PORT_C, speed)
                try:
                    print(self.heading)   # print the gyro sensor values
                except brickpi3.SensorError as error:
                    print(error)

        except KeyboardInterrupt:
            self.BP.reset_all() 
    def turnDeg(self, speed, degrees):
        
        motorDeg = 2.4 * degrees

        headingStart = self.heading

        try:
            while True:

                self.BP.offset_motor_encoder(self.BP.PORT_B, self.BP.get_motor_encoder(self.BP.PORT_B))
                self.BP.set_motor_limits(self.BP.PORT_B, 90, speed)
                self.BP.set_motor_position(self.BP.PORT_B, motorDeg)
                    
                self.BP.offset_motor_encoder(self.BP.PORT_C, self.BP.get_motor_encoder(self.BP.PORT_C))
                self.BP.set_motor_limits(self.BP.PORT_C, 90, speed) 
                self.BP.set_motor_position(self.BP.PORT_C, -motorDeg)

                while abs(self.BP.get_motor_encoder(self.BP.PORT_B) - motorDeg) > 1:
                    self.gyro.printHeading()
        except KeyboardInterrupt:
            self.BP.reset_all()