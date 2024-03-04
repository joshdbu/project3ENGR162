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
        self.heading = 3 # heading of 0 is left, 1 is up, 2 is right, 3 is down
        self.mouseMap = np.zeros((self.height, self.width, self.depth))
        self.favorList = [3, 0, 2, 1] # ranked list of favorite paths, rn down, right, left, up
        self.unit = 5 # grid unit distance in centimeters

        self.careBot = Robot()
        
        
    def move(self):
        
        self.mapUpdate()
        data = self.mouseMap[self.yPos, self.xPos, 0:4]
        path = self.decidePath(data)
        # print("path is", path)
        # print("heading is", self.heading)
        if len(path) > 1:
            for i in range(len(self.favorList) - 1, -1, -1): # reverse indexes path through favorlist
                if self.favorList[i] in path:
                    choice = self.favorList[i]
        else:
            choice = path[0]
        
        if self.heading == choice:
            self.drive()
            self.careBot.driveStraightUntil(100, self.unit, 1)
            # print("going straight")
        elif (self.heading - 1 == choice) | (self.heading + 3 == choice):
            self.heading = choice
            # print("turning left")
            self.careBot.gyroTurn(100, 90)
            # print("going straight")
            self.careBot.driveStraightUntil(100, self.unit, 1)
            
            # robot turn left 90
            self.drive()
        elif (self.heading + 1 == choice) | (self.heading - 3 == choice):
            self.heading = choice
            self.careBot.gyroTurn(100, -90)
            # print("turning right")
            self.careBot.driveStraightUntil(100, self.unit, 1)
            # print("going straight")
            # robot turn right 90
            self.drive()
        else:
            self.heading = choice
            self.careBot.gyroTurn(100, 180)
            # print("turning aorund")
            self.careBot.driveStraightUntil(100, self.unit, 1)
            # print("turning right")
            # robot turn 180
            self.drive()
        
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
        
        # junction sensing
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

    def solveMaze(self):
        move = 1
        self.mouseMap[self.yPos, self.xPos, 4] += 1 # increments visits to this cell
        self.drive() # moves into maze
        self.careBot.driveStraightUntil(100, 10, 1)
        while self.yPos < self.height - 1:
            
            self.move()
            print("at", self.oldX, " ", self.oldY)
            move += 1
        path = [[row[4] for row in column] for column in self.mouseMap]
        path = [[' X ' if element != 0 else '   ' for element in row] for row in path]
        
        return move, path
    
    
    def mapUpdate(self):
        walls = self.careBot.explore()
        out = [0, 0, 0, 0]
        if self.heading == 0:
            out = [walls[1], walls[2], walls[3], walls[0]]
        elif self.heading == 2:
            out = [walls[3], walls[0], walls[1], walls[2]]
        elif self.heading ==3:
            out = [walls[2], walls[3], walls[0], walls[1]]
        else:
            out = walls

        for i in range(0,4):
            self.mouseMap[self.yPos, self.xPos, i] = out[i] # had walls instead of out cost me hours

    def reset(self):
        self.xPos, self.oldX = self.startX, self.startX
        self.yPos, self.oldY = self.startY, self.startY
        self.mouseMap = np.zeros((self.height, self.width, self.depth))
