class Map:
    def __init__(j, intX, intY):
        j.h = 5 # height of map
        j.w = 5 # width of map
        j.x = 6 # depth of map
        #j.mazeMap = np.zeros((j.h, j.w, j.x))
        j.startX = intX
        j.startY = intY
        #j.mazeMap[j.startX][j.startY] = [1,1,1,0,0,0]
        
        j.practiceMap = [
                    [[1, 1, 0, 0], [0, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [0, 1, 1, 0]],
                    [[1, 0, 0, 0], [0, 1, 0, 1], [0, 0, 0, 0], [0, 1, 0, 1], [0, 0, 1, 0]],
                    [[1, 0, 1, 0], [1, 1, 1, 0], [1, 0, 1, 1], [1, 1, 1, 0], [1, 0, 1, 0]],
                    [[1, 0, 0, 0], [0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1], [1, 0, 1, 0]],
                    [[1, 0, 0, 1], [0, 0, 1, 1], [1, 0, 1, 0], [1, 1, 0, 1], [0, 0, 1, 1]],
                    [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
                    ]
        
    def surround(j, xCord, yCord):
        out = j.practiceMap[xCord][yCord]
        return out
    def explore(j, xCord, yCord):
        
        out = j.practiceMap[xCord][yCord]
        out.append(0)
        out.append(0)
        return out