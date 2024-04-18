import numpy as np
from RobotClass import Robot

speed = 200


class MazeRobot:
    def __init__(self, x, y, h, w, d):
        
        self.xPos, self.startX, self.oldX = x, x, x
        self.yPos, self.startY, self.oldY = y, y, y
        self.height = h
        self.width = w
        self.depth = d
        self.heading = 3 # heading of 0 is left, 1 is up, 2 is right, 3 is down
        self.mouseMap = np.zeros((self.height, self.width, self.depth))
        self.favorList = [3, 2, 0, 1] # ranked list of favorite paths, rn down, left, right, up
        # self.favorList = [3, 2, 0, 1] # ranked list of favorite paths
        self.unit = 40 # grid unit distance in centimeters
        self.wallDist = 12 # distance to stop from forward wall

        self.obRX = 3
        self.obRY = 2

        self.careBot = Robot()
        
        
    def move(self):
        
        self.mapUpdate()
        self.updateFavor()
        if (self.xPos == self.obRX) & (self.yPos == self.obRY):
            self.avoidThings()
        data = self.mouseMap[self.yPos, self.xPos, 0:4]
        path = self.decidePath(data)
        # print("path is", path)
        # print("heading is", self.heading)
        
        # print("path is 0 is left, 1 is up, 2 is right, 3 is down\n", path)
        if len(path) > 1:
            for i in range(len(self.favorList) - 1, -1, -1): # reverse indexes path through favorlist
                if self.favorList[i] in path:
                    choice = self.favorList[i]
        else:
            choice = path[0]
        
        if self.heading == choice:
            self.drive(False)
            self.careBot.driveStraightUntil(speed, self.unit, self.wallDist)
            # print("going straight")
        elif (self.heading - 1 == choice) | (self.heading + 3 == choice):
            self.heading = choice
            # print("turning left")
            self.careBot.gyroTurn(150, 90)
            # print("going straight")
            self.careBot.driveStraightUntil(speed, self.unit, self.wallDist)
            
            # robot turn left 90
            self.drive(False)
        elif (self.heading + 1 == choice) | (self.heading - 3 == choice):
            self.heading = choice
            self.careBot.gyroTurn(150, -90)
            # print("turning right")
            self.careBot.driveStraightUntil(speed, self.unit, self.wallDist)
            # print("going straight")
            # robot turn right 90
            self.drive(False)
        else:
            # self.heading = choice
            # self.careBot.gyroTurn(150, 180)
            # print("turning aorund")
            # self.careBot.driveStraightUntil(speed, self.unit, self.wallDist)
            # # print("turning right")
            # # robot turn 180
            self.careBot.driveStraightDist(-speed, -self.unit)
            self.drive(True)
        
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
                # print(options[1], "pre mm sub")
                options[1] -= self.mouseMap[self.yPos - 1, self.xPos, 4] 
                # print(options[1], "pre wall subtraction")
                options[1] -= data[1] * 2
                # print(options[1], "post wall subtraction")
            else:
                options[1] -= 2
                # print("is this killing us? if print then yes", self.xPos, self.yPos)
            
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

    
    def drive(self, flag):
        self.oldY = self.yPos
        self.oldX = self.xPos
        
        if self.heading == 0:    
            if not flag:
                self.xPos -= 1
            else:
                self.xPos += 1
        elif self.heading == 1:
            if not flag:  
                self.yPos -= 1
            else:
                self.yPos += 1
        elif self.heading == 2:
            if not flag:
                self.xPos += 1
            else:
                self.xPos -= 1
        elif self.heading == 3:
            if not flag:
                self.yPos += 1
            else:
                self.yPos -= 1

        self.mouseMap[self.yPos, self.xPos, 4] += 1 # increments visits to this cell

    def solveMaze(self):
        for i in range(25):
            self.careBot.ultraWarmUp()
        move = 1
        print("is this updated?")
        self.mouseMap[self.yPos, self.xPos, 4] += 1 # increments visits to this cell
        self.drive(False) # moves into maze
        self.careBot.driveStraightUntil(speed, self.unit, self.wallDist)
        while not ((self.xPos == 5) & (self.yPos == 5)):
        # while self.yPos < self.height - 1:
            
            print("at", self.oldX, " ", self.oldY)
            self.move()
            print("")
            move += 1
        path = [[row[4] for row in column] for column in self.mouseMap]
        path = [['1' if element != 0 else '0' for element in row] for row in path]
        path[self.startY][self.startX] = 5
        path[self.yPos][self.xPos] = 4
        obstacles = []
        for i in range(self.height):
            for j in range(self.width):
                if self.mouseMap[i, j, 5] != 0:
                    obstacles.append(["High Temperature Heat Source", "Radiated Power (W)", self.mouseMap[i, j, 6], j + 1, i + 1])
                elif self.mouseMap[i, j, 6] != 0:
                    obstacles.append(["Electrical/Magnetic Activity Source", "Field Strength (uT)", self.mouseMap[i, j, 5], j + 1, i + 1])


        for row in obstacles:
            if row[0] == "High Temperature Heat Source":
                path[row[3] - 1][row[4] - 1] = 2
            else:
                path[row[3] - 1][row[4] - 1] = 3

        print(obstacles)

        self.reset()
        # print("do we get here?")
        return move, path, obstacles
    
    
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
        pass
        # update = False
        # points = [[3,2],[2,0]] # enter dangerous points here. dangerous points are the path to obstacle, not necasarily obstacle itself

        # if (self.xPos == 3) & (self.yPos == 2):
        #     self.favorList = [2, 0, 1]
        #     print("we're cheating")
        # else:
        #     self.favorList = [3, 2, 0, 1]


        # for i in range(len(points) - 1):
        #     if (self.xPos + 1 == points[i, 0]) & (self.yPos == points[i, 1]): # if obstacle is to right
        #         self.favorList = [3, 2, 1]
        #         update = True
        #     elif (self.xPos - 1 == points[i, 0]) & (self.yPos == points[i, 1]): # if obstacle is to left
        #         self.favorList = [3, 0, 1]
        #         update = True
        #     elif (self.xPos == points[i, 0]) & (self.yPos + 1 == points[i, 1]): # if below
        #         self.favorList = [2, 0, 1]
        #         update = True
        #     elif (self.xPos == points[i, 0]) & (self.yPos - 1 == points[i, 1]): # if above
        #         self.favorList = [3, 2, 0]
        #         update = True
            
        # if not update:
        #     self.favorList = [3, 2, 0, 1] # confirms favorlist is reset if not at point

    def reset(self):
        self.careBot.reset()
        self.xPos, self.oldX = self.startX, self.startX
        self.yPos, self.oldY = self.startY, self.startY
        self.mouseMap = np.zeros((self.height, self.width, self.depth))

    def avoidThings(self):
        IRReading = self.careBot.frontIR.IR_Read()
        # magReading = self.mag.Mag_Read()
        print(f"IR: {IRReading}")
        if IRReading > 55: #IR sensor reading from 20 cm away
            # print(f"IR: {IRReading}")
            if self.heading == 0:
                self.mouseMap[self.yPos, self.xPos - 1, 5] = IRReading
            elif self.heading == 1:
                self.mouseMap[self.yPos - 1, self.xPos, 5] = IRReading
            elif self.heading == 2:
                self.mouseMap[self.yPos, self.xPos + 1, 5] = IRReading
            elif self.heading == 3:
                self.mouseMap[self.yPos + 1, self.xPos, 5] = IRReading
            return(IRReading)
                
        # elif magReading[3] > 2: #this needs to be confirmed
        #     magnitude = magReading[3]
        #     print(f"Mag: {magnitude}")
        #     if self.heading == 0:
        #         self.mouseMap[self.yPos, self.xPos - 1, 6] = magnitude
        #     elif self.heading == 1:
        #         self.mouseMap[self.yPas - 1, self.xPos, 6] = magnitude
        #     elif self.heading == 2:
        #         self.mouseMap[self.yPos, self.xPos + 1, 6] = magnitude
        #     elif self.heading == 3:
        #         self.mouseMap[self.yPos + 1, self.xPos, 6] = magnitude
        #     return(magnitude)

        else:
            return(0)
