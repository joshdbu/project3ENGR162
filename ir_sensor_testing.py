# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 14:14:41 2024

@author: Elizabeth
"""

import time
import grovepi
from IR_Functions import *

IR_setup(grovepi)

while True:
    try:
        [sensor1_value, sensor2_value]=IR_Read(grovepi)
        
        print ("One = " + str(sensor1_value) + "\tTwo = " + str(sensor2_value))
        time.sleep(.1)

    except IOError:
        print ("Error")
