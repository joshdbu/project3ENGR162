# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 14:37:51 2024

@author: 13017
"""

def IR_setup(grovepi):
        sensor1= 8		# Pin 8 is A8 Port
        sensor2 = 9		# Pin 9 is A8 Port 
        grovepi.pinMode(sensor1,"INPUT")
        grovepi.pinMode(sensor2,"INPUT")

# Output function
def IR_PrintValues(grovepi):
        try:
                sensor1= 8		
                sensor2 = 9		         
                sensor1_value = grovepi.analogRead(sensor1)
                sensor2_value = grovepi.analogRead(sensor2)
                
                print ("One = " + str(sensor1_value) + "\tTwo = " + str(sensor2_value))


        except IOError:
                print ("Error")

#Read Function		
def IR_Read(grovepi):
        try:
                sensor1= 8		
                sensor2 = 9	             
                sensor1_value = grovepi.analogRead(sensor1)
                sensor2_value = grovepi.analogRead(sensor2)
                
                return [sensor1_value, sensor2_value]

        except IOError:
                print ("Error")
