# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 13:48:07 2024

@author: 13017
"""
import math
import time
from RobotClass import Robot
careBot = Robot()

pointOne = [0, 2]
pointTwo = [2, 2]
pointThree = [2, 0]
pointFour = [0, 0]
sleepTime = 100
sizeOfGridSqu = 40 # in cm


while True:
    [a,b] = pointOne
    [c,d] = pointTwo
    [e,f] = pointThree
    [g,h] = pointFour
    
    
    #calculates degrees and distance from previous point to the next point
    degreeOne = math.degrees(math.tan(a/b))
    distOne = math.sqrt((a*a) + (b*b))
    
    degreeTwo = math.degrees(math.tan((c-a)/(d-b)))
    distTwo = math.dist(pointTwo, pointOne)
    
    degreeThree = math.degrees(math.tan((e-c)/(f-d)))
    distThree = math.dist(pointThree, pointTwo)
    
    degreeFour = math.degrees(math.tan((g-e)/(h-f)))
    distFour = math.dist(pointFour, pointThree)
    
    
    # To point one
    careBot.gyroTurn(100, degreeOne)
    careBot.driveStraightDist(50, sizeOfGridSqu * distOne)
    time.sleep(sleepTime)  # waits to allow for distance checking in POC
    
    
    # to point two
    careBot.gyroTurn(100, degreeTwo)
    careBot.driveStraightDist(50, sizeOfGridSqu * distTwo)
    time.sleep(sleepTime)  # waits to allow for distance checking in POC
    
    # to point three
    careBot.gyroTurn(100, degreeThree)
    careBot.driveStraightDist(50, sizeOfGridSqu * distThree)
    time.sleep(sleepTime)  # waits to allow for distance checking in POC
    
    # to point four
    careBot.gyroTurn(100, degreeFour)
    careBot.driveStraightDist(50, sizeOfGridSqu * distFour)
    time.sleep(sleepTime)  # waits to allow for distance checking in POC
    
