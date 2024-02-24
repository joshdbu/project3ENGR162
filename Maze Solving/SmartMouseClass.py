import math as m
import numpy as np
import random as r
from MapClass import Map

# smartMouse can only make surround function calls to map class

class SmartMouse:
    def __init__(x, j):
        
        x.xPos = j.startX
        x.yPos = j.startY
        x.oldX = j.startX
        x.oldY = j.startY
        x.height = j.h
        x.width = j.w
        x.depth = j.x
        x.mouseMap = np.zeros((x.height, x.width, x.depth))
        
        
    def moveUp(x):
        x.oldY = x.yPos
        x.oldX = x.xPos
        x.yPos -= 1
        
    def moveDown(x):
        x.oldY = x.yPos
        x.oldX = x.xPos
        x.yPos += 1
        
    def moveLeft(x):
        x.oldY = x.yPos
        x.oldX = x.xPos
        x.xPos -= 1
        
    def moveRight(x):
        x.oldY = x.yPos
        x.oldX = x.xPos
        x.xPos += 1
        
    def move(x,j):
        
        data = Map.surround(j, x.yPos, x.xPos) #pulls surrounding data from map example, replace with robot function in future
        x.mouseMap[x.yPos, x.xPos, 4] += 1 # increments visits to this cell

        path = x.decidePath(data)

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
        moves = [] # stores final list of potential moves
        semiSafeList = [] # stores directions that have been visited but good to go to from junction
        back = 3 # direction we came from

        if x.xPos - x.oldX == 1:
            back = 0
        elif x.xPos - x.oldX == -1:
            back = 2
        elif x.yPos - x.oldY == 1:
            back = 1
        elif x.yPos - x.oldY == -1:
            back = 3


        # new junction sensing

        if sum(data) == 2: 
            for i in range(0,4):
                if data[i] == 0:
                    if i != back:
                        moves.append(i) # when in a hallway, this will give direction of next move
                        #print("do we ever get here?")
                    # print("what about here")

        elif sum(data) == 3:
            moves.append(back) # when in a dead end, this will give direction of next move
        else:
           # print("wheee whoooo junction reached!!")

            # junction reached
            
            if x.xPos != 0: # scores left option
                options[0] -= x.mouseMap[x.yPos, x.xPos - 1, 4] # subtracts if left has been visited
                options[0] -= data[0] * 2 # eliminates if left has wall
            else:
                options[0] -= 2 # eliminates if mouse on left side
            
            if x.yPos != 0: # scores top option
                options[1] -= x.mouseMap[x.yPos - 1, x.xPos, 4] 
                options[1] -= data[1] * 2
            else:
                options[1] -= 2
            
            if x.xPos != 4: # scores right option
                options[2] -= x.mouseMap[x.yPos, x.xPos + 1, 4] 
                options[2] -= data[2] * 2
            else: 
                options[2] -= 2
           
            if x.yPos != 4: # scores bottom option
                options[3] -= x.mouseMap[x.yPos + 1, x.xPos, 4] 
                options[3] -= data[3] * 2
            else:
                options[3] -= 2

            

            for i in range(0,4):
                if options[i] == 2:
                    moves.append(i) # adds unvisited options into moves
                elif options[i] == 1:
                    semiSafeList.append(i) # adds visited once paths into semiSafelist
            

        if len(moves) == 0:
            if x.mouseMap[x.oldY, x.oldX, 4] < 2:
                moves.append(back)
            else:
                moves = semiSafeList
            
        
        return moves   
