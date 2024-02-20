import math as m
import numpy as np
import random as r
from MapClass import Map

class DumbMouse:
    def __init__(x, j):
        
        x.xPos = j.startX
        x.yPos = j.startY
        x.height = j.h
        x.width = j.w
        x.depth = j.x
        x.mouseMap = np.zeros((x.height, x.width, x.depth))
        
        
    def moveUp(x):
        x.yPos -= 1
    def moveDown(x):
        x.yPos += 1
    def moveLeft(x):
        x.xPos -= 1
    def moveRight(x):
        x.xPos += 1
    def move(x,j):
        flag = True
        data = Map.surround(j, x.yPos, x.xPos)
        #print(data)
        #j.mazeMap[x.yPos, x.xPos] = data
        while flag:
            num = r.randint(0,3)
            if data[num] == 0:
                
                flag = False
                if num == 0:
                    x.moveLeft()
                elif num == 1:
                    x.moveUp()
                elif num == 2:
                    x.moveRight()
                elif num == 3:
                    x.moveDown()
                
        
    
    def printChar(x):
        x=0
        
        
    def solveMaze(x):
        
        x.moveLeft()
        x.moveUp()
