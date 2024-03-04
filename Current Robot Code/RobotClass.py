from __future__ import print_function # use python 3 syntax but make it compatible with python 2
import brickpi3 # type: ignore
from RobotGyro import Gyro
from GroveUltrasonic import GroveUltra
from EV3Ultrasonic import EV3Ultra
import math
import sys
import time

BP = brickpi3.BrickPi3()
print("current battery voltage:", BP.get_voltage_battery())
BP.reset_all()
# sys.tracebacklimit = -1

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
        self.timeConst = 0.01
    
    def turnDeg(self, speed, degrees): # this function usless now?
        motorDeg = 2.44 * degrees
        try:

            BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
            BP.set_motor_limits(BP.PORT_B, 90, speed)

            BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))
            BP.set_motor_limits(BP.PORT_C, 90, speed) 
            start = time.perf_counter()
            while (time.perf_counter() - start) < 3:
                
                BP.set_motor_position(BP.PORT_B, motorDeg)

                BP.set_motor_position(BP.PORT_C, -motorDeg)


        except KeyboardInterrupt:
            self.reset()
        
    def reset(self):
        self.reset()

    def move(self, speed):
        try:
            while True:
                BP.set_motor_dps(BP.PORT_B, speed)
                BP.set_motor_dps(BP.PORT_C, speed)

        except KeyboardInterrupt:
            self.reset() 
  
    def gyroTurn(self, speed, degrees):

        direction = -1
        if degrees > 0:
            direction = 1

        gain = 15
        
        try:
            
            self.gyro.reset()
            # print("heading at begining of turn is", self.gyro.heading())
            # start = time.perf_counter()
            # while (time.perf_counter() - start) < 1:
            #     pass           
            # print("if this val different than ^ somthing is wrong", self.gyro.heading())
            # print("compared vals: heading and degrees", abs(self.gyro.heading()), abs(degrees))
            while abs(self.gyro.heading())  + 5 < abs(degrees) :
                # self.gyro.printHeading()
                BP.set_motor_dps(BP.PORT_B, speed * direction)
                BP.set_motor_dps(BP.PORT_C, speed * -direction)
            
            start = time.perf_counter()
            
            
            while (time.perf_counter() - start) < 2:
                currentOffset = degrees - self.gyro.heading()
                
                # self.gyro.printHeading()
                BP.set_motor_dps(BP.PORT_B, gain * currentOffset * 1)
                BP.set_motor_dps(BP.PORT_C, gain * currentOffset * -1)

            BP.set_motor_dps(BP.PORT_B, 0)
            BP.set_motor_dps(BP.PORT_C, 0)
            
            # start = time.perf_counter()
            # print("heading at begining end turn is", self.gyro.heading())
            self.gyro.reset()
            # print("reset heading is", self.gyro.heading())
            # while (time.perf_counter() - start) < self.timeConst:
            #     pass
            
            


        except KeyboardInterrupt:
            self.reset()

    def driveStriaghtDistNoGyro(self, speed, dist):
        degrees = round((360 * dist) / (math.pi * self.wheelDia))
        
        try:
            
            BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
            BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))

            gain = 10
            gain2 = 15
            average = 0
            offset = 0
            
            start = time.perf_counter()

            while average < degrees - 3:
                if time.perf_counter() - start < 2:
                    dpsb = 100 * ((time.perf_counter() - start) / 2)
                    dpsc = 93 * ((time.perf_counter() - start) / 2)
                else:
                    dpsb, dpsc = 100, 100
                BP.set_motor_dps(BP.PORT_B, dpsb + (gain * offset))
                BP.set_motor_dps(BP.PORT_C, dpsc + (gain * offset))

                average = (abs(BP.get_motor_encoder(BP.PORT_B)) + abs(BP.get_motor_encoder(BP.PORT_C))) / 2
                offset = BP.get_motor_encoder(BP.PORT_B) - BP.get_motor_encoder(BP.PORT_C)
                

            BP.set_motor_dps(BP.PORT_B, 0)
            BP.set_motor_dps(BP.PORT_C, 0)
            # time.sleep(self.timeConst) # for reasons unknow to me this MUST be > 1. <= 1 stops folowing actions from executing? 

           
                
        
        except KeyboardInterrupt:
            self.reset()

    def driveStraightDist(self, speed, dist):

        degrees = round((360 * dist) / (math.pi * self.wheelDia))
        self.gyro.reset()
        

        try:
            
            # print("heading at begining of drive is", self.gyro.heading())
            start = time.perf_counter()
            while (time.perf_counter() - start) < self.timeConst:
                pass
            BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
            BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))

            gain = 10
            gain2 = 15
            average = 0
            

            while average < degrees - 3:
                
                
                currentOffset = self.gyro.heading()
                # self.gyro.printHeading()

                BP.set_motor_dps(BP.PORT_B, speed - gain * currentOffset)
                BP.set_motor_dps(BP.PORT_C, speed + gain * currentOffset)

                average = (BP.get_motor_encoder(BP.PORT_B) + BP.get_motor_encoder(BP.PORT_C)) / 2
                

            start = time.perf_counter()
            while (time.perf_counter() - start) < 2:
                # self.gyro.printHeading()
                currentOffset = degrees - average
                BP.set_motor_dps(BP.PORT_B, gain2 * currentOffset)
                BP.set_motor_dps(BP.PORT_C, gain2 * currentOffset)
                average = (BP.get_motor_encoder(BP.PORT_B) + BP.get_motor_encoder(BP.PORT_C)) / 2
                

            BP.set_motor_dps(BP.PORT_B, 0)
            BP.set_motor_dps(BP.PORT_C, 0)
            start = time.perf_counter()
            
            # while (time.perf_counter() - start) < self.timeConst:
            #     pass
            # # print("heading at end of drive is", self.gyro.heading())
        
            
            
           
                
        
        except KeyboardInterrupt:
            self.reset()

    def driveStraightUntil(self, speed, groundDist, wallDist):
        degrees = round((360 * groundDist) / (math.pi * self.wheelDia))
        
        try:
            
            self.gyro.reset()
            time.sleep(self.timeConst)
            BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
            BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))

            gain = 10
            gain2 = 15
            gain3 = 50
            average = 0
            flagGround = False
            flagWall = False

            while (not flagGround) &  (not flagWall):

                currentOffset = self.gyro.heading()
                

                BP.set_motor_dps(BP.PORT_B, speed - gain * currentOffset)
                BP.set_motor_dps(BP.PORT_C, speed + gain * currentOffset)

                average = (BP.get_motor_encoder(BP.PORT_B) + BP.get_motor_encoder(BP.PORT_C)) / 2
                # print(average, " ", degrees - 3)
                if average > degrees - 3:
                    flagGround = True
                    # print("1")
                elif self.frontUltra.getDistance() < wallDist + 5:
                    flagWall = True
                    # print("2")
                
            if flagGround:
                start = time.perf_counter()
                while (time.perf_counter() - start) < 3:
                    currentOffset = degrees - average
                    BP.set_motor_dps(BP.PORT_B, gain2 * currentOffset)
                    BP.set_motor_dps(BP.PORT_C, gain2 * currentOffset)
                    average = (BP.get_motor_encoder(BP.PORT_B) + BP.get_motor_encoder(BP.PORT_C)) / 2

            if flagWall:
                start = time.perf_counter()
                while (time.perf_counter() - start) < 5:
                    currentOffset = wallDist - self.frontUltra.getDistance()
                    # print(currentOffset)
                    if abs(currentOffset) > 2:
                        currentOffset = 0
                    BP.set_motor_dps(BP.PORT_B, gain3 * -currentOffset)
                    BP.set_motor_dps(BP.PORT_C, gain3 * -currentOffset)  

            BP.set_motor_dps(BP.PORT_B, 0)
            BP.set_motor_dps(BP.PORT_C, 0)
            time.sleep(self.timeConst) # for reasons unknow to me this MUST be > 1. <= 1 stops folowing actions from executing? 

           
                
        
        except KeyboardInterrupt:
            self.reset()

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
            self.reset()

    def getHeading(self):

        try:
            while True:
                
                self.gyro.printHeading()
        except KeyboardInterrupt:
            self.reset()
    
    def getFrontUltraDist(self):

        try:
            while True:

                self.frontUltra.printDistance()
        except KeyboardInterrupt:
            self.reset()
            
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

            BP.set_motor_dps(BP.PORT_B, 0)
            BP.set_motor_dps(BP.PORT_C, 0)
            
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

            

            # dist = 0.5 * (self.frontLeftUltra.getDistance() + self.backLeftUltra.getDistance())
            # print("dist is", dist)

            # if (dist < 6):
                
            #     self.gyroTurn(100, -90)
            #     self.driveStraightDist(100, abs(12 - dist))
            #     self.gyroTurn(100, 90)

            #     BP.set_motor_dps(BP.PORT_B, 0)
            #     BP.set_motor_dps(BP.PORT_C, 0)

            #     dist = 0.5 * (self.frontLeftUltra.getDistance() + self.backLeftUltra.getDistance())
            #     print("dist is", dist)

            # while True:
            #     if abs(self.frontLeftUltra.getDistance() - self.backLeftUltra.getDistance()) < 2:
            #         break
            #     left = self.frontLeftUltra.getDistance()
            #     right = self.backLeftUltra.getDistance()
                
            #     currentOffset = left - right
            #     BP.set_motor_dps(BP.PORT_B, speed * (currentOffset / abs(currentOffset)))
            #     BP.set_motor_dps(BP.PORT_C, speed * (-currentOffset / abs(currentOffset)))

            # start = time.perf_counter()
            # while (time.perf_counter() - start) < 4:
                
            #     left = self.frontLeftUltra.getDistance()
            #     right = self.backLeftUltra.getDistance()
                
            #     currentOffset = left - right
                
            #     BP.set_motor_dps(BP.PORT_B, gain * currentOffset * 1)
            #     BP.set_motor_dps(BP.PORT_C, gain * currentOffset * -1)
             
            # BP.set_motor_dps(BP.PORT_B, 0)
            # BP.set_motor_dps(BP.PORT_C, 0)


        
        except KeyboardInterrupt:
            self.reset()

        
    def explore(self):
        # returns distances of surrounding walls

        walls = []
        walls.append(0.5 * (self.frontLeftUltra.getDistance() + self.backLeftUltra.getDistance()))
        walls.append(self.frontUltra.getDistance())
        walls.append(self.rightUltra.getDistance())
        walls.append(0) # we just came from this direction
        for i in range(0, len(walls)):
            if (walls[i] < 20) & (walls[i] != 0):
                walls[i] = 1
            else:
                walls[i] = 0

        print("walls i see", walls)
        
        return walls
    
    def reset(self):
        print("Robot shutting down... :(")
        BP.reset_all()
        sys.exit(1)





