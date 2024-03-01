import numpy as np
import random as r
from MapClass import Map
from RobotClass import Robot

class MazeRobot:
    def __init__(self, x, y, h, w, d):
        
        self.xPos, self.startX, self.oldX = x, x, x
        self.yPos, self.startY, self.oldY = y, y, y
        self.height = h
        self.width = w
        self.depth = d
        
        
        self.moveDist = 40 # cell distance
        self.heading = 3 # heading of 0 is left, 1 is up, 2 is right, 3 is down
        self.mouseMap = np.zeros((self.height, self.width, self.depth))
        self.robot = Robot()
        
            

    def move(self, j):
        data = Map.surround(j, self.yPos, self.xPos)

        path = self.decidePath(data)

        if len(path) > 1:
            choice = path[r.randint(0,len(path) - 1)]
        else:
            choice = path[0]
        
        if self.heading == choice:
            self.drive()
            # self.robot.driveStraightUntil()
        elif self.heading - 1 == choice:
            self.heading = choice
            # robot turn left 90
            self.drive()
        elif self.heading + 1 == choice:
            self.heading = choice
            # robot turn right 90
            self.drive()
        else:
            self.heading = choice
            # robot turn 180
            self.drive()
        


    
    def drive(self):
        self.oldY = self.yPos
        self.oldX = self.xPos
        
        if self.heading == 0:    
            self.xPos -= 1
        elif self.heading == 1:
            self.yPos -= 1
        elif self.heading == 2:
            self.xPos += 1
        elif self.heading == 3:
            self.yPos += 1

        self.mouseMap[self.yPos, self.xPos, 4] += 1 # increments visits to this cell

            

    
            
        

    def decidePath(self, data):
        options = [ 2, 2, 2, 2 ] # start at 2, decrease depending on criteria, if reaches zero its a no go
        moves = [] # stores final list of potential moves
        semiSafeList = [] # stores directions that have been visited but good to go to from junction
        back = 3 # direction we came from

        if self.xPos - self.oldX == 1:
            back = 0
        elif self.xPos - self.oldX == -1:
            back = 2
        elif self.yPos - self.oldY == 1:
            back = 1
        elif self.yPos - self.oldY == -1:
            back = 3


        # new junction sensing

        if sum(data) == 2: 
            for i in range(0,4):
                if data[i] == 0:
                    if i != back:
                        moves.append(i) # when in a hallway, this will give direction of next move


        elif sum(data) == 3:
            if (self.xPos == self.startX) & (self.yPos == self.startY + 1):
                moves.append(3) # hard code to not make robot leave maze when it gets in
            else:
                moves.append(back) # when in a dead end, this will give direction of next move
        else:

            # junction reached
            
            if self.xPos != 0: # scores left option
                options[0] -= self.mouseMap[self.yPos, self.xPos - 1, 4] # subtracts if left has been visited
                options[0] -= data[0] * 2 # eliminates if left has wall
            else:
                options[0] -= 2 # eliminates if mouse on left side
            
            if self.yPos != 0: # scores top option
                options[1] -= self.mouseMap[self.yPos - 1, self.xPos, 4] 
                options[1] -= data[1] * 2
            else:
                options[1] -= 2
            
            if self.xPos != self.width - 1: # scores right option
                options[2] -= self.mouseMap[self.yPos, self.xPos + 1, 4] 
                options[2] -= data[2] * 2
            else: 
                options[2] -= 2
           
            if self.yPos != self.height - 1: # scores bottom option
                options[3] -= self.mouseMap[self.yPos + 1, self.xPos, 4] 
                options[3] -= data[3] * 2
            else:
                options[3] -= 2

            for i in range(0,4):
                if options[i] == 2:
                    moves.append(i) # adds unvisited options into moves
                elif options[i] == 1:
                    semiSafeList.append(i) # adds visited once paths into semiSafelist
            

        if len(moves) == 0:
            if self.mouseMap[self.oldY, self.oldX, 4] < 2:
                moves.append(back)
            else:
                moves = semiSafeList
        return moves   
    
    def solveMaze(self, j):
        move = 1
        
        self.mouseMap[self.yPos, self.xPos, 4] += 1 # increments visits to this cell
        self.drive() # moves into maze
        while self.yPos < self.height - 1:
            self.move(j)
            move += 1
            print("x Pos:", self.xPos, "Y Pos:", self.yPos)
        path = [[row[4] for row in column] for column in self.mouseMap]
        path = [[' X ' if element != 0 else '   ' for element in row] for row in path]
        
        return move, path
    
    def reset(self):
        self.xPos, self.oldX = self.startX, self.startX
        self.yPos, self.oldY = self.startY, self.startY
        self.mouseMap = np.zeros((self.height, self.width, self.depth))