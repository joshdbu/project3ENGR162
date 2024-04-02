from __future__ import print_function 
import grovepi
from MPU9250 import MPU9250
import math
import time

class MagSensor:
    def __init__(self): 
        mpu9250 = MPU9250()
    
    # print function
    def Mag_PrintValues(self):
        [xMag, yMag, zMag] = mpu9250.readMagnet() # magnet sensor values
        print ("X = " + x + "\tY = " + yMag + "\tZ = " + zMag);

    #Read Function		
    def Mag_Read(self):
        [xMag, yMag, zMag] = mpu9250.readMagnet() # magnet sensor values
        return [xMag, yMag, zMag]
        
