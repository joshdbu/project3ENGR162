import time
from MazeRobotClass import MazeRobot

# self, x, y, h, w, d
print("Data entry:\n*Don't forget to start at zero and include bounderies :)*")
xVal = int(input("Please enter maximum X value of maze: "))
yVal = int(input("Please enter maximum Y value of maze: "))
startXPos = int(input("Please enter Start X Pos of robot: "))
careBot = MazeRobot(startXPos, 0, yVal, xVal, 7)

time.sleep(5)

# hi Josh

careBotMoves = []
careBotPaths = []

careBotMove, careBotPath = careBot.solveMaze()
careBotMoves.append(careBotMove)
careBotPaths.append(careBotPath)
    
careBot.reset()

minIndex = careBotMoves.index(min(careBotMoves))

for row in careBotPaths[0]:  # Iterate over each row in the first scenario
    for i in range(len(row)):  # Iterate over each index in the row
        print(int(row[i]), end='')  # Print the integer value without newline
        if i < len(row) - 1:  # Check if it's not the last value in the row
            print(',')  # Add comma and space
    print()  # Move to the next line after printing each row

print("careBot took", careBotMoves[0], "turns")  # Print the number of turns for the first scenario

