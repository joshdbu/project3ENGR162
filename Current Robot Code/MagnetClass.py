from __future__ import print_function 
from MPU9250 import MPU9250
import math
from statistics import mean

mpu9250 = MPU9250()

class Magnet_Sensor:
    def __init__(self): 
        self.baseline = [0,0]
        self.baseline = self.calibrate()
        
    # print function
    def Mag_PrintValues(self):
        [xMag, yMag, zMag, magnitude] = self.Mag_Read()
        print ("X = " + xMag + "\tY = " + yMag + "\tZ = " + zMag);

    #Read Function		
    def Mag_Read(self):
        xList = []
        yList = []
        zList = []
        for i in range(10):
            mag = mpu9250.readMagnet() # magnet sensor values
            xMag = mag['x']
            yMag = mag['y']
            zMag = mag['z']
            xList.append(xMag - self.baseline[0])
            yList.append(yMag - self.baseline[1])
            zList.append(zMag)
        xAvg = mean(xList)
        yAvg = mean(yList)
        zAvg = mean(zList)
        magnitude = math.sqrt(xAvg ** 2 + yAvg ** 2)
        return [xAvg, yAvg, zAvg, magnitude]

    def calibrate(self):
        [xMag, yMag, zMag, magnitude] = self.Mag_Read()
        return[xMag, yMag]