import numpy as np
from RobotClass import Robot

speed = 250


class MazeRobot:
    def __init__(self, x, y, h, w, d, ex, ey):
        
        self.xPos, self.startX, self.oldX = x, x, x
        self.yPos, self.startY, self.oldY = y, y, y
        self.height = h
        self.width = w
        self.depth = d
        self.endX = ex
        self.endY = ey
        self.heading = 3 # heading of 0 is left, 1 is up, 2 is right, 3 is down
        self.mouseMap = np.zeros((self.height, self.width, self.depth))
        self.favorList = [3, 2, 0, 1] # ranked list of favorite paths, rn down, left, right, up
        # self.favorList = [2, 3, 0, 1] # ranked list of favorite paths
        self.unit = 40 # grid unit distance in centimeters
        self.wallDist = 15 # distance to stop from forward wall

        self.obRX = 2
        self.obRY = 5

        self.careBot = Robot()
        
        
    def move(self):
        
        self.mapUpdate()
        self.updateFavor()
        if (self.xPos == self.obRX) & (self.yPos == self.obRY):
            self.avoidThings()
        data = self.mouseMap[self.yPos, self.xPos, 0:4]
        path = self.decidePath(data)

        if len(path) > 1:
            for i in range(len(self.favorList) - 1, -1, -1): # reverse indexes path through favorlist
                if self.favorList[i] in path:
                    choice = self.favorList[i]
        else:
            choice = path[0]
        
        if self.heading == choice: # straight
            self.careBot.driveStraightUntil(speed, self.unit, self.wallDist)
            self.drive()

        elif (self.heading - 1 == choice) | (self.heading + 3 == choice): #left
            self.heading = choice
            self.careBot.gyroTurn(150, 90)
            if self.careBot.frontLeftUltra.getDistance() < 25: # added in 4/18, should square up post turns 
                self.careBot.squareUp()
            
            self.careBot.driveStraightUntil(speed, self.unit, self.wallDist)
            self.drive()

        elif (self.heading + 1 == choice) | (self.heading - 3 == choice): #right
            self.heading = choice
            self.careBot.gyroTurn(150, -90)
            if self.careBot.frontLeftUltra.getDistance() < 25: # added in 4/18, should square up post turns 
                self.careBot.squareUp()
            
            self.careBot.driveStraightUntil(speed, self.unit, self.wallDist)
            self.drive()
        
        else: #back up
            self.heading = choice
            self.careBot.gyroTurn(150, -180)
            if self.careBot.frontLeftUltra.getDistance() < 25: # added in 4/18, should square up post turns 
                self.careBot.squareUp()
            
            self.careBot.driveStraightUntil(speed, self.unit, self.wallDist)
            
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
        
        else: # junction reached
            
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


    # def drive(self, flag):
    #     self.oldY = self.yPos
    #     self.oldX = self.xPos
        
    #     # flagging stuff is for backwards driving
    #     if self.heading == 0:    
    #         if not flag:
    #             self.xPos -= 1
    #         else:
    #             self.xPos += 1
    #     elif self.heading == 1:
    #         if not flag:  
    #             self.yPos -= 1
    #         else:
    #             self.yPos += 1
    #     elif self.heading == 2:
    #         if not flag:
    #             self.xPos += 1
    #         else:
    #             self.xPos -= 1
    #     elif self.heading == 3:
    #         if not flag:
    #             self.yPos += 1
    #         else:
    #             self.yPos -= 1

        self.mouseMap[self.yPos, self.xPos, 4] += 1 # increments visits to this cell

    def solveMaze(self):
        for i in range(10):
            self.careBot.ultraWarmUp()
        move = 1
        print("is this updated?")
        self.mouseMap[self.yPos, self.xPos, 4] += 1 # increments visits to this cell
        self.drive() # moves into maze
        self.careBot.driveStraightUntil(speed, self.unit, self.wallDist)
        while not ((self.xPos == self.endX) & (self.yPos == self.endY)):
            print("at", self.xPos, " ", self.yPos)
            self.move()
            print("")
            move += 1
        self.careBot.dropCargo(-1000, 800, True)
        path = [[row[4] for row in column] for column in self.mouseMap]
        path = [['1' if element != 0 else '0' for element in row] for row in path]
        # print("path is", path)
        path[self.startY][self.startX] = 5
        path[self.yPos][self.xPos] = 4
        obstacles = []
        # hardcoded hazards
        # self.mouseMap[4, 1, 6] = 150.23
        # self.mouseMap[4, 1, 5] = 70.2
        for i in range(self.height):
            for j in range(self.width):
                if self.mouseMap[i, j, 5] != 0:
                    obstacles.append(["High Temperature Heat Source", "Radiated Power (W)", self.mouseMap[i, j, 5], j, i])
                    self.mouseMap[i, j, 4] = 2                
                elif self.mouseMap[i, j, 6] != 0:
                    obstacles.append(["Electrical/Magnetic Activity Source", "Field Strength (uT)", self.mouseMap[i, j, 6], j, i])
                    self.mouseMap[i, j, 4] = 3

        for row in obstacles:
            if row[0] == "High Temperature Heat Source":
                path[row[3]][row[4]] = 2
            else:
                path[row[3]][row[4]] = 3

        # print(obstacles)

        self.reset()
        return move, path, obstacles
    
    
    def mapUpdate(self):
        walls = self.careBot.explore()
        if walls[0] == 1:
            self.careBot.squareUp()

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

        if (self.xPos == -1) & (self.yPos == -1):
            self.favorList = [1]
            print("we're cheating")
        else:
            self.favorList = [3, 2, 0, 1]

    def reset(self):
        # self.careBot.reset()
        self.xPos, self.oldX = self.startX, self.startX
        self.yPos, self.oldY = self.startY, self.startY
        self.mouseMap = np.zeros((self.height, self.width, self.depth))

    def avoidThings(self):
        IRReading = self.careBot.frontIR.IR_Read()
        magReading = self.careBot.magnet.Mag_Read()
        # print(f"IR: {IRReading}")
        if IRReading > 25: #IR sensor reading from 20 cm away
            print(f"IR: {IRReading}")
            if self.heading == 0:
                self.mouseMap[self.yPos, self.xPos - 1, 5] = IRReading
            elif self.heading == 1:
                self.mouseMap[self.yPos - 1, self.xPos, 5] = IRReading
            elif self.heading == 2:
                self.mouseMap[self.yPos, self.xPos + 1, 5] = IRReading
            elif self.heading == 3:
                self.mouseMap[self.yPos + 1, self.xPos, 5] = IRReading
            return(IRReading)
                
        elif magReading[3]:
        # elif magReading[3] > 1.5: 
            magnitude = magReading[3]
            print(f"Mag: {magnitude}")
            if self.heading == 0:
                self.mouseMap[self.yPos, self.xPos - 1, 6] = magnitude
            elif self.heading == 1:
                self.mouseMap[self.yPas - 1, self.xPos, 6] = magnitude
            elif self.heading == 2:
                self.mouseMap[self.yPos, self.xPos + 1, 6] = magnitude
            elif self.heading == 3:
                self.mouseMap[self.yPos + 1, self.xPos, 6] = magnitude

            return(magnitude)

        else:
            return(0)