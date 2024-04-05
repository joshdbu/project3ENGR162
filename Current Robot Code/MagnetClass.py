from __future__ import print_function 
import grovepi
from MPU9250 import MPU9250
import math
import time
from statistics import mean

class Magnet_Sensor:
    def __init__(self): 
        mpu9250 = MPU9250()
    
    # print function
    def Mag_PrintValues(self):
        [xMag, yMag, zMag] = self.Mag_Read()
        print ("X = " + x + "\tY = " + yMag + "\tZ = " + zMag);

    #Read Function		
    def Mag_Read(self):
        xList = []
        yList = []
        zList = []
        for i in range(10):
            [xMag, yMag, zMag] = mpu9250.readMagnet() # magnet sensor values
            xList.append(xMag)
            yList.append(yMag)
            zList.append(zMag)
        xAvg = mean(xList)
        yAvg = mean(yList)
        zAvg = mean(zList)
        return [xAvg, yAvg, zAvg]
        
