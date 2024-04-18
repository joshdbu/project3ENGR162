from __future__ import print_function # use python 3 syntax but make it compatible with python 2
import brickpi3 # type: ignore
from RobotGyro import Gyro
from GroveUltrasonic import GroveUltra
from EV3Ultrasonic import EV3Ultra
from IRClass import IRSensor
import math
import sys
import time

BP = brickpi3.BrickPi3()
print("\nCurrent battery voltage:", BP.get_voltage_battery(), "volts \nProgram will begin in T - 5 seconds")
BP.reset_all()
startTime = time.perf_counter()


class Robot:
    def __init__(self):
        
        self.frontUltraPort = 7
        self.leftFrontUP = 6
        self.leftBackUP = 5
        self.numMeasure = 2

        self.gyro = Gyro()
        self.frontUltra = GroveUltra(self.frontUltraPort, self.numMeasure)
        self.frontLeftUltra = GroveUltra(self.leftFrontUP, self.numMeasure)
        self.backLeftUltra = GroveUltra(self.leftBackUP, self.numMeasure)
        self.rightUltra = EV3Ultra(self.numMeasure)
        self.frontIR = IRSensor()

        self.heading = self.gyro.heading()
        self.wheelDia = 4.07 
        self.timeConst = 0.01
    
    def gyroTurn(self, speed, degrees): # this function usless now?
        print("starting turn")
        dia = 2.35
        motorDeg = dia * degrees
        direction = motorDeg / abs(motorDeg)
        gain = 15
        try:

            BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
            BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))
            temp = 0
            while temp < abs(motorDeg):
                BP.set_motor_dps(BP.PORT_B, speed * direction)
                BP.set_motor_dps(BP.PORT_C, speed * -direction)
                temp = 0.5 * (abs(BP.get_motor_encoder(BP.PORT_B)) + abs(BP.get_motor_encoder(BP.PORT_C)))

            start = time.perf_counter()
            while (time.perf_counter() - start) < 3:
                
                currentOffset = abs(motorDeg) - abs(temp)
                BP.set_motor_dps(BP.PORT_B, gain * currentOffset * direction)
                BP.set_motor_dps(BP.PORT_C, gain * -currentOffset * direction)
                temp = 0.5 * (abs(BP.get_motor_encoder(BP.PORT_B)) + abs(BP.get_motor_encoder(BP.PORT_C)))
                

            BP.set_motor_dps(BP.PORT_B, 0)
            BP.set_motor_dps(BP.PORT_C, 0)

            print("turn done")

        except KeyboardInterrupt:
            self.reset()

    def turnDeg(self, speed, degrees):

        direction = -1
        if degrees > 0:
            direction = 1

        gain = 15
        
        try:
            
            self.gyro.reset()
    
            while abs(self.gyro.heading())  + 5 < abs(degrees) :
                # print("og loop: ", self.gyro.heading())
                self.gyro.printHeading()
                BP.set_motor_dps(BP.PORT_B, speed * direction)
                BP.set_motor_dps(BP.PORT_C, speed * -direction)
            
            start = time.perf_counter()
            
            
            while (time.perf_counter() - start) < 2:
                currentOffset = degrees - self.gyro.heading()
                # print("p loop: ", self.gyro.heading())
                self.gyro.printHeading()
                BP.set_motor_dps(BP.PORT_B, gain * currentOffset * 1)
                BP.set_motor_dps(BP.PORT_C, gain * currentOffset * -1)

            BP.set_motor_dps(BP.PORT_B, 0)
            BP.set_motor_dps(BP.PORT_C, 0)
        
            self.gyro.reset()
            
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
            start = time.perf_counter()
            while (time.perf_counter() - start) < self.timeConst:
                pass
            BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
            BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))

            gain = 10
            gain2 = 15
            average = 0
            
            while abs(average) < abs(degrees - 3):    
                currentOffset = self.gyro.heading()

                BP.set_motor_dps(BP.PORT_B, speed - gain * currentOffset)
                BP.set_motor_dps(BP.PORT_C, speed + gain * currentOffset)

                average = (BP.get_motor_encoder(BP.PORT_B) + BP.get_motor_encoder(BP.PORT_C)) / 2
                

            start = time.perf_counter()
            while (time.perf_counter() - start) < 2:
                currentOffset = degrees - average
                BP.set_motor_dps(BP.PORT_B, gain2 * currentOffset)
                BP.set_motor_dps(BP.PORT_C, gain2 * currentOffset)
                average = (BP.get_motor_encoder(BP.PORT_B) + BP.get_motor_encoder(BP.PORT_C)) / 2
                

            BP.set_motor_dps(BP.PORT_B, 0)
            BP.set_motor_dps(BP.PORT_C, 0)
            start = time.perf_counter()

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
            self.ultraWarmUp()
            while (not flagGround) &  (not flagWall):

                currentOffset = self.gyro.heading()
                

                BP.set_motor_dps(BP.PORT_B, speed - gain * currentOffset)
                BP.set_motor_dps(BP.PORT_C, speed + gain * currentOffset)

                average = (BP.get_motor_encoder(BP.PORT_B) + BP.get_motor_encoder(BP.PORT_C)) / 2
                temp = self.frontUltra.getDistance()
                # print(temp)

                if (abs(average) > abs(degrees - 15)) & (temp > 20): #added stuff jb 4/18
                    flagGround = True
                    print("fg")
                elif  temp < wallDist:
                    print("wall dist", temp)
                    flagWall = True
                    print("fw")
                
            if flagGround:
                start = time.perf_counter()
                while (time.perf_counter() - start) < 3:
                    currentOffset = degrees - average
                    # print(currentOffset)
                    BP.set_motor_dps(BP.PORT_B, gain2 * currentOffset)
                    BP.set_motor_dps(BP.PORT_C, gain2 * currentOffset)
                    average = (BP.get_motor_encoder(BP.PORT_B) + BP.get_motor_encoder(BP.PORT_C)) / 2

            if flagWall:
                start = time.perf_counter()
                while (time.perf_counter() - start) < 5:
                    currentOffset = wallDist - self.frontUltra.getDistance()
                    # print("current off:", currentOffset)
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
                if self.frontUltra.getDistance() < dist + 1:
                    break    
                currentOffset = self.gyro.heading()
                
                BP.set_motor_dps(BP.PORT_B, speed - gain * currentOffset)
                BP.set_motor_dps(BP.PORT_C, speed + gain * currentOffset)


            start = time.perf_counter()
            while (time.perf_counter() - start) < 3:
                raw = dist - self.frontUltra.getDistance()
                if abs(raw) < 10:
                    currentOffset = raw
                BP.set_motor_dps(BP.PORT_B, gain2 * -currentOffset)
                BP.set_motor_dps(BP.PORT_C, gain2 * -currentOffset)
                

            BP.set_motor_dps(BP.PORT_B, 0)
            BP.set_motor_dps(BP.PORT_C, 0)
            time.sleep(3)

        except KeyboardInterrupt:
            self.reset()

    def getFrontUltraDist(self):

        try:
            while True:

                self.frontUltra.printDistance()
        except KeyboardInterrupt:
            self.reset()
            
    def squareUp(self):
        # squares up robot on left wall and resets gyro
        try:
            gain = 15
            while True:

                left = self.frontLeftUltra.getDistance()
                right = self.backLeftUltra.getDistance()
                
                if abs(left - right) < 1.5:
                    break
                
                
                currentOffset = left - right
                
                # print("left:", left, "right:", right, "offset:", currentOffset)
                BP.set_motor_dps(BP.PORT_B, 100 * (currentOffset / abs(currentOffset))) # add python even odd function instead of math, div by zero error could happen if offset is rounded to zero
                BP.set_motor_dps(BP.PORT_C, 100 * (-currentOffset / abs(currentOffset)))

            BP.set_motor_dps(BP.PORT_B, 0)
            BP.set_motor_dps(BP.PORT_C, 0)
            left = self.frontLeftUltra.getDistance()
            right = self.backLeftUltra.getDistance()
            currentOffset = left - right
            
            if abs(currentOffset) < 1:
                timeConst = 2
            else:
                timeConst = 5
            
            start = time.perf_counter()
            while (time.perf_counter() - start) < timeConst:
                
                left = self.frontLeftUltra.getDistance()
                right = self.backLeftUltra.getDistance()
                
                currentOffset = left - right
                # print("left:", left, "right:", right, "offset:", currentOffset)
                if abs(currentOffset) > 10:
                    pass
                    print("error caught. current offset is:", currentOffset)
                else:
                    BP.set_motor_dps(BP.PORT_B, gain * currentOffset * 1)
                    BP.set_motor_dps(BP.PORT_C, gain * currentOffset * -1)
                
            BP.set_motor_dps(BP.PORT_B, 0)
            BP.set_motor_dps(BP.PORT_C, 0)
            
            self.gyro.reset()
        
        except KeyboardInterrupt:
            self.reset()

    def strafe(self, direction, wallDist, wheelDist):
        factor = 1
        if direction == 0:
            factor = -1
            
        self.gyroTurn(150, -90 * factor)
        self.driveStraightUntil(150, wheelDist, wallDist)
        self.gyroTurn(150, 90 * factor)

        self.squareUp()

    def celebrate(self):
        try:

            start = time.perf_counter()
            while (time.perf_counter() - start) <0.5:
                
                BP.set_motor_dps(BP.PORT_A, -120)
            while (time.perf_counter() - start) < 1:
                
                BP.set_motor_dps(BP.PORT_A, 120)
            BP.set_motor_dps(BP.PORT_A, 0)

        except KeyboardInterrupt:
            self.reset()
    
    def explore(self):
        # returns distances of surrounding walls
        for i in range(5):
            self.ultraWarmUp()
        walls = []
        walls.append(0.5 * (self.frontLeftUltra.getDistance() + self.backLeftUltra.getDistance()))
        walls.append(self.frontUltra.getDistance())
        walls.append(0.5 * (self.rightUltra.getDistance() + self.rightUltra.getDistance()))
        walls.append(0) # we just came from this direction
        print("\nwalls are", walls)
        for i in range(0, len(walls)):
            if (walls[i] < 30) & (walls[i] != 0):
                walls[i] = 1
            else:
                walls[i] = 0

        print("walls i see", walls)
        
        return walls
    
    def reset(self):
        print("\n\n\nRobot shutting down... :(\nStats:", round(time.perf_counter() - startTime, 2), "seconds of run time\n\n\n")
        BP.set_motor_dps(BP.PORT_B, 0)
        BP.set_motor_dps(BP.PORT_C, 0)
        self.celebrate()
        BP.reset_all()
        sys.exit(1)

    def ultraWarmUp(self):
        a = self.frontLeftUltra.getDistance()
        b = self.backLeftUltra.getDistance()
        c = self.frontUltra.getDistance()
        d = self.rightUltra.getDistance()
        time.sleep(0.05)
