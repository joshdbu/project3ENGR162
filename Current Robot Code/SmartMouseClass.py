import math as m
import numpy as np
import random as r
from MapClass import Map

# smartMouse can only make surround function calls to map class
# theoreticly surround function could be replaced with robot function and code would sill run
class SmartMouse:
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
        data = Map.surround(j, x.yPos, x.xPos) #pulls surrounding data from map example, replace with robot function in future
        x.mouseMap[x.yPos, x.xPos, 4] += 1 # increments visits to this cell

        path = x.decidePath(data)
        print(path)

        if len(path) > 1:
            choice = path[r.randint(0,len(path) - 1)]
        else:
            choice = path[0]
        
        if choice == 0:
            x.moveLeft()
        elif choice == 1:
            x.moveUp()
        elif choice == 2:
            x.moveRight()
        elif choice == 3:
            x.moveDown()        

    def decidePath(x, data):
        options = [ 2, 2, 2, 2 ] # start at 2, decrease depending on criteria, if reaches zero its a no go
        
        if x.xPos != 0: # confirms mouse is not on left side
            options[0] -= x.mouseMap[x.yPos, x.xPos - 1, 4] # subtracts if left has been visited
            options[0] -= data[0] * 2 # eliminates if left has wall
        else:
            options[0] -= 2
        if x.yPos != 0:
            options[1] -= x.mouseMap[x.yPos - 1, x.xPos, 4] 
            options[1] -= data[1] * 2
        else:
            options[1] -= 2
        if x.xPos != 4:
            options[2] -= x.mouseMap[x.yPos, x.xPos + 1, 4] 
            options[2] -= data[2] * 2
        else: 
            options[2] -= 2
        if x.yPos != 4:
            options[3] -= x.mouseMap[x.yPos + 1, x.xPos, 4] 
            options[3] -= data[3] * 2
        else:
            options[3] -= 2

        safeList = []
        semiSafeList = []
        maxIndex = 4
        maxNum = 1
        for i in range(0,4):
            if options[i] == 2:
                safeList.append(i)
            elif options[i] == 1:
                semiSafeList.append(i)
        if len(safeList) == 0:
            safeList = semiSafeList
                
            

        
        print(options,' x: ', x.xPos, ' y: ', x.yPos)
        return safeList
        

        
    def solveMaze(x):
        
        x.moveLeft()
        x.moveUp()
