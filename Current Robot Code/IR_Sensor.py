# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 15:25:13 2024

@author: Elizabeth
"""
from __future__ import print_function 
import grovepi

class IRSensor:
    def __init__(self): 
       sensor1= 8		# Pin 8 is A8 Port
       sensor2 = 9		# Pin 9 is A8 Port 
       grovepi.pinMode(sensor1,"INPUT")
       grovepi.pinMode(sensor2,"INPUT")

    # print function
    def IR_PrintValues(self):
       [x, y] =  self.IR_Read()
       print ("One = " + x + "\tTwo = " + y)

    #Read Function		
    def IR_Read(self):
           
        sensor1= 8		
        sensor2 = 9	             
        sensor1_value = grovepi.analogRead(sensor1)
        sensor2_value = grovepi.analogRead(sensor2)
                    
        return [sensor1_value, sensor2_value]
        