from __future__ import print_function # use python 3 syntax but make it compatible with python 2
import brickpi3 # type: ignore
from RobotGyro import Gyro
from GroveUltrasonic import GroveUltra
from EV3Ultrasonic import EV3Ultra
import math
from statistics import mean

import time

BP = brickpi3.BrickPi3()
BP.reset_all()

class Robot:
    def __init__(self):
        
        self.frontUltraPort = 5
        self.leftFrontUP = 6
        self.leftBackUP = 7

        self.gyro = Gyro()
        self.frontUltra = GroveUltra(self.frontUltraPort)
        self.frontLeftUltra = GroveUltra(self.leftFrontUP)
        self.backLeftUltra = GroveUltra(self.leftBackUP)
        self.rightUltra = EV3Ultra()

        self.heading = self.gyro.heading()
        self.wheelDia = 4.07 
        self.timeConst = 0.5

        
    def move(self, speed):
        try:
            while True:
                BP.set_motor_dps(BP.PORT_B, speed)
                BP.set_motor_dps(BP.PORT_C, speed)

        except KeyboardInterrupt:
            BP.reset_all() 
  
    def gyroTurn(self, speed, degrees):

        direction = -1
        if degrees > 0:
            direction = 1

        gain = 15
        
        try:
            
            self.gyro.reset()
            
            time.sleep(self.timeConst)
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
            
            time.sleep(self.timeConst)
            
            


        except KeyboardInterrupt:
            BP.reset_all()

    
    def driveStraightDist(self, speed, dist):

        degrees = round((360 * dist) / (math.pi * self.wheelDia))
        
        try:
            
            self.gyro.reset()
            time.sleep(self.timeConst)
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
            time.sleep(self.timeConst) # for reasons unknow to me this MUST be > 1. <= 1 stops folowing actions from executing? 

           
                
        
        except KeyboardInterrupt:
            BP.reset_all()

    def driveStraightUltra(self, speed, dist):
        
        # speed is speed of robot- 200 is good
        # dist is stop distance from wall

        try:
            
            self.gyro.reset()
            
            gain = 10 # tuning drive straight
            gain2 = 75 # tuning stop at value
            
            while True:
                if self.frontUltra.getDistance() < dist + 5:
                    break    
                currentOffset = self.gyro.heading()
                
                BP.set_motor_dps(BP.PORT_B, speed - gain * currentOffset)
                BP.set_motor_dps(BP.PORT_C, speed + gain * currentOffset)


            start = time.perf_counter()
            while (time.perf_counter() - start) < 5:
                currentOffset = dist - self.frontUltra.getDistance()
                print(currentOffset)
                BP.set_motor_dps(BP.PORT_B, gain2 * -currentOffset)
                BP.set_motor_dps(BP.PORT_C, gain2 * -currentOffset)
                

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
    
    def getFrontUltraDist(self):

        try:
            while True:

                self.frontUltra.printDistance()
        except KeyboardInterrupt:
            BP.reset_all()
            
    def squareUp(self, speed):
        # squares up robot on left wall and resets gyro
        try:
            gain = 15
            while True:
                if abs(self.frontLeftUltra.getDistance() - self.backLeftUltra.getDistance()) < 2:
                    break
                left = self.frontLeftUltra.getDistance()
                right = self.backLeftUltra.getDistance()
                
                currentOffset = left - right
                BP.set_motor_dps(BP.PORT_B, speed * (currentOffset / abs(currentOffset)))
                BP.set_motor_dps(BP.PORT_C, speed * (-currentOffset / abs(currentOffset)))

            start = time.perf_counter()
            while (time.perf_counter() - start) < 4:
                
                left = self.frontLeftUltra.getDistance()
                right = self.backLeftUltra.getDistance()
                
                currentOffset = left - right

                BP.set_motor_dps(BP.PORT_B, gain * currentOffset * 1)
                BP.set_motor_dps(BP.PORT_C, gain * currentOffset * -1)
             
            BP.set_motor_dps(BP.PORT_B, 0)
            BP.set_motor_dps(BP.PORT_C, 0)
            
            self.gyro.reset()

            time.sleep(2)

            dist = 0.5 * (self.frontLeftUltra.getDistance() + self.backLeftUltra.getDistance())
            print("dist is", dist)

            if (dist < 6):
                
                self.gyroTurn(100, -90)
                self.driveStraightDist(100, abs(12 - dist))
                self.gyroTurn(100, 90)

                BP.set_motor_dps(BP.PORT_B, 0)
                BP.set_motor_dps(BP.PORT_C, 0)

                dist = 0.5 * (self.frontLeftUltra.getDistance() + self.backLeftUltra.getDistance())
                print("dist is", dist)

            while True:
                if abs(self.frontLeftUltra.getDistance() - self.backLeftUltra.getDistance()) < 2:
                    break
                left = self.frontLeftUltra.getDistance()
                right = self.backLeftUltra.getDistance()
                
                currentOffset = left - right
                BP.set_motor_dps(BP.PORT_B, speed * (currentOffset / abs(currentOffset)))
                BP.set_motor_dps(BP.PORT_C, speed * (-currentOffset / abs(currentOffset)))

            start = time.perf_counter()
            while (time.perf_counter() - start) < 4:
                
                left = self.frontLeftUltra.getDistance()
                right = self.backLeftUltra.getDistance()
                
                currentOffset = left - right
                
                BP.set_motor_dps(BP.PORT_B, gain * currentOffset * 1)
                BP.set_motor_dps(BP.PORT_C, gain * currentOffset * -1)
             
            BP.set_motor_dps(BP.PORT_B, 0)
            BP.set_motor_dps(BP.PORT_C, 0)


        
        except KeyboardInterrupt:
            BP.reset_all()

        
    def explore(self):
        # returns distances of surrounding walls

        walls = []
        walls.append(0.5 * (self.frontLeftUltra.getDistance() + self.backLeftUltra.getDistance()))
        walls.append(self.frontUltra.getDistance())
        walls.append(self.rightUltra.getDistance())
        walls.append(-1) # we just came from this direction

        
        
        return walls





