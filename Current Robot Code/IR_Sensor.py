# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 15:25:13 2024

@author: Elizabeth
"""
from __future__ import print_function 
import grovepi
from statistics import mean

class IRSensor:
    def __init__(self): 
       self.sensor1 = 8		# Pin 8 is A8 Port
       self.sensor2 = 9		# Pin 9 is A8 Port 
       grovepi.pinMode(sensor1,"INPUT")
       grovepi.pinMode(sensor2,"INPUT")

    # print function
    def IR_PrintValues(self):
       reading = self.IR_Read()
       print ("IR reading: " + reading)

    #Read Function		
    def IR_Read(self): 
        readList = []
        for i in range(10):
            sensor1_value = grovepi.analogRead(self.sensor1)
            sensor2_value = grovepi.analogRead(self.sensor2)
            avgValue = (sensor1_value + sensor2_value) / 2   
            readList.append(avgValue)
        meanValue = mean(readList)
        return meanValue
        
