import numpy as np
from RobotClass import Robot
from MagnetClass import Magnet_Sensor
from IRClass import IRSensor

class MazeRobot:
    def __init__(self, x, y, h, w, d):
        
        self.xPos, self.startX, self.oldX = x, x, x
        self.yPos, self.startY, self.oldY = y, y, y
        self.height = h
        self.width = w
        self.depth = d
        self.heading = 3 # heading of 0 is left, 1 is up, 2 is right, 3 is down
        self.mouseMap = np.zeros((self.height, self.width, self.depth))
        self.favorList = [2, 3, 0, 1] # ranked list of favorite paths, rn down, left, right, up
        # self.favorList = [3, 2, 0, 1] # ranked list of favorite paths
        self.unit = 40 # grid unit distance in centimeters
        self.wallDist = 12 # distance to stop from forward wall

        self.careBot = Robot()
        self.mag = Magnet_Sensor()
        self.IR = IRSensor()
        
        
    def move(self):
        
        self.mapUpdate()
        data = self.mouseMap[self.yPos, self.xPos, 0:4]
        path = self.decidePath(data)
        # print("path is", path)
        # print("heading is", self.heading)
        # self.updateFavor()
        print("path is 0 is left, 1 is up, 2 is right, 3 is down\n", path)
        if len(path) > 1:
            for i in range(len(self.favorList) - 1, -1, -1): # reverse indexes path through favorlist
                if self.favorList[i] in path:
                    choice = self.favorList[i]
        else:
            choice = path[0]
        
        if self.heading == choice:
            self.drive()
            self.careBot.driveStraightUntil(200, self.unit, self.wallDist)
            # print("going straight")
        elif (self.heading - 1 == choice) | (self.heading + 3 == choice):
            self.heading = choice
            # print("turning left")
            self.careBot.gyroTurn(150, 90)
            # print("going straight")
            self.careBot.driveStraightUntil(200, self.unit, self.wallDist)
            
            # robot turn left 90
            self.drive()
        elif (self.heading + 1 == choice) | (self.heading - 3 == choice):
            self.heading = choice
            self.careBot.gyroTurn(150, -90)
            # print("turning right")
            self.careBot.driveStraightUntil(200, self.unit, self.wallDist)
            # print("going straight")
            # robot turn right 90
            self.drive()
        else:
            self.heading = choice
            self.careBot.gyroTurn(150, 180)
            # print("turning aorund")
            self.careBot.driveStraightUntil(200, self.unit, self.wallDist)
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
                self.mouseMap[self.yPos, self.xPos, 4] += 1 # added 4/17 to stop double cycling in single dead ends
        
        else:
            # junction reached
            
            if self.xPos != 0: # scores left option
                options[0] -= self.mouseMap[self.yPos, self.xPos - 1, 4] # subtracts if left has been visited
                options[0] -= data[0] * 2 # eliminates if left has wall
            else:
                options[0] -= 2 # eliminates if mouse on left side
            
            if self.yPos != 0: # scores top option
                print(options[1], "pre mm sub")
                options[1] -= self.mouseMap[self.yPos - 1, self.xPos, 4] 
                print(options[1], "pre wall subtraction")
                options[1] -= data[1] * 2
                print(options[1], "post wall subtraction")
            else:
                options[1] -= 2
                print("is this killing us? if print then yes", self.xPos, self.yPos)
            
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
        self.careBot.driveStraightUntil(200, self.unit, self.wallDist)
        while self.yPos < self.height - 1:
            
            print("at", self.oldX, " ", self.oldY)
            self.move()
            print("")
            move += 1
        path = [[row[4] for row in column] for column in self.mouseMap]
        # path = [[' X ' if element != 0 else '   ' for element in row] for row in path]
        
        self.reset()
        print("do we get here?")
        return move, path
    
    
    def mapUpdate(self):
        walls = self.careBot.explore()
        # print
        if walls[0] == 1:
            # pass
            self.careBot.squareUp()

            # leftWallDist = 0.5 * (self.careBot.backLeftUltra.getDistance() + self.careBot.frontLeftUltra.getDistance())
            # print("leftwall dist is:", leftWallDist)
            # if leftWallDist < 7:
            #     temp = self.wallDist - leftWallDist
            #     self.careBot.strafe(1, 999, temp)
            # elif leftWallDist > 17.5:
            #     self.careBot.strafe(0, self.wallDist, 999)
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

    def updateFavor(self):
        update = False
        points = [[3,2],[2,0]] # enter dangerous points here. dangerous points are the path to obstacle, not necasarily obstacle itself

        for i in range(len(points) - 1):
            if (self.xPos + 1 == points[i, 0]) & (self.yPos == points[i, 1]): # if obstacle is to right
                self.favorList = [3, 2, 1]
                update = True
            elif (self.xPos - 1 == points[i, 0]) & (self.yPos == points[i, 1]): # if obstacle is to left
                self.favorList = [3, 0, 1]
                update = True
            elif (self.xPos == points[i, 0]) & (self.yPos + 1 == points[i, 1]): # if below
                self.favorList = [2, 0, 1]
                update = True
            elif (self.xPos == points[i, 0]) & (self.yPos - 1 == points[i, 1]): # if above
                self.favorList = [3, 2, 0]
                update = True
            
        if not update:
            self.favorList = [3, 2, 0, 1] # confirms favorlist is reset if not at point

    def reset(self):
        self.xPos, self.oldX = self.startX, self.startX
        self.yPos, self.oldY = self.startY, self.startY
        self.mouseMap = np.zeros((self.height, self.width, self.depth))

    def avoidThings(self):
        IRReading = self.IR.IR_Read()
        magReading = self.mag.Mag_Read()
        
        if IRReading > 60: #IR sensor reading from 20 cm away
            print(f"IR: {IRReading}")
            if self.heading == 0:
                self.mouseMap[self.yPos, self.xPos - 1, 5] = IRReading
            elif self.heading == 1:
                self.mouseMap[self.yPos - 1, self.xPos, 5] = IRReading
            elif self.heading == 2:
                self.mouseMap[self.yPos, self.xPos + 1, 5] = IRReading
            elif self.heading == 3:
                self.mouseMap[self.yPos + 1, self.xPos, 5] = IRReading
                
        elif magReading[0] > 4 and magReading[1] > 10: #this needs to be confirmed
            print(f"Mag: {magReading}")
            if self.heading == 0:
                self.mouseMap[self.yPos, self.xPos - 1, 6] = magReading
            elif self.heading == 1:
                self.mouseMap[self.yPas - 1, self.xPos, 6] = magReading
            elif self.heading == 2:
                self.mouseMap[self.yPos, self.xPos + 1, 6] = magReading
            elif self.heading == 3:
                self.mouseMap[self.yPos + 1, self.xPos, 6] = magReading
