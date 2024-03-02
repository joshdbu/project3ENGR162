import numpy as np

class DemoMap:
    def __init__(self):
        self.h = 7 # height of map
        self.w = 5 # width of map
    
    def getHeight(self):
        return self.h
    def getWidth(self):
        return self.w


class Map:
    def __init__(self, intX, intY):
        self.h = 7 # height of map
        self.w = 5 # width of map
        self.x = 6 # depth of map
        #self.mazeMap = np.zeros((self.h, self.w, self.x))
        self.startX = intX
        self.startY = intY
        #self.mazeMap[self.startX][self.startY] = [1,1,1,0,0,0]
        
        self.practiceMap = [
                    [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                    [[1, 1, 0, 0], [0, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [0, 1, 1, 0]],
                    [[1, 0, 0, 0], [0, 1, 0, 1], [0, 0, 0, 0], [0, 1, 0, 1], [0, 0, 1, 0]],
                    [[1, 0, 1, 0], [1, 1, 1, 0], [1, 0, 1, 1], [1, 1, 1, 0], [1, 0, 1, 0]],
                    [[1, 0, 0, 0], [0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1], [1, 0, 1, 0]],
                    [[1, 0, 0, 1], [0, 0, 1, 1], [1, 0, 1, 0], [1, 1, 0, 1], [0, 0, 1, 1]],
                    [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
                    ]
        
    def surround(self, yCord, xCord, heading):
        
        walls = self.practiceMap[yCord][xCord]

        out = [0, 0, 0, 0]
        if heading == 0:
            out = [walls[3], walls[0], walls[1], walls[2]]
        elif heading == 2:
            out = [walls[1], walls[2], walls[3], walls[0]]
        elif heading == 3:
            out = [walls[2], walls[3], walls[0], walls[1]]
        else:
            out = walls


        return out
    def testExplore(self, yCord, xCord):
        
        out = self.practiceMap[yCord][xCord]

        return out
    