import time
from MazeRobotClass import MazeRobot
import csv

# self, x, y, h, w, d
print("Data entry:\n*Don't forget to start at zero and include bounderies :)*")
# xVal = int(input("Please enter maximum X value of maze: "))
# yVal = int(input("Please enter maximum Y value of maze: "))
# startXPos = int(input("Please enter Start X Pos of robot: "))
# startYPos = int(input("Please enter Start Y Pos of robot: "))
# endX = int(input("Please enter end X value of maze: "))
# endY = int(input("Please enter end Y value of maze: "))

xVal = 7
yVal = 9
startXPos = 5
startYPos = 0
endX = 0
endY = 7

careBot = MazeRobot(startXPos, startYPos, yVal, xVal, 7, endX, endY)

time.sleep(5)

# hi Josh

careBotMoves = []
careBotPaths = []
careBotObstacles = []

careBotMove, careBotPath, careBotObstacle = careBot.solveMaze()
careBotMoves.append(careBotMove)
careBotPaths.append(careBotPath)
careBotObstacles.append(careBotObstacle)
    


minIndex = careBotMoves.index(min(careBotMoves))

print("paths v2", careBotMoves[0])

for row in careBotPaths[0]:  # Iterate over each row in the first scenario
    for i in range(len(row)):  # Iterate over each index in the row
        print(int(row[i]), end='')  # Print the integer value without newline
        if i < len(row) - 1:  # Check if it's not the last value in the row
            print(',', end = '')  # Add comma and space
    print()  # Move to the next line after printing each row

with open('careBotPaths.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    
    # Writing metadata
    csvwriter.writerow(["Team: 39"])
    csvwriter.writerow(["Map: Demo"])
    csvwriter.writerow(["Unit Length: 40"])
    csvwriter.writerow(["Unit: cm"])
    csvwriter.writerow(['Origin: (2', '0)'])
    csvwriter.writerow(["Notes: This is the demo"])
    
    # Iterate over each row in the 2D list and write it to the CSV file
    # for row in careBotPaths[0][1:]:  # Exclude the first row
    #     csvwriter.writerow(row[1:-1])  # Exclude the first and last columns

    for row in careBotPaths[0]:
        csvwriter.writerow(row)

with open('team39_hazards.csv', 'w', newline='') as csvfile:
    # print("here1")
    csvwriter = csv.writer(csvfile)
    # print("here2")
    csvwriter.writerow(["Team: 39"])
    csvwriter.writerow(["Map: Demo"])
    csvwriter.writerow(["Origin: (2, 0)"])
    csvwriter.writerow(["Notes: This is the demo hazard info"])
    csvwriter.writerow([])
    csvwriter.writerow(["Hazard Type", "Parameter of Interest", "Parameter Value", "Hazard X Coordinate", "Hazard Y Coordinate"])
    
    # Iterate over each row in the 2D list and write it to the CSV file
    for row in careBotObstacles[0]:
        csvwriter.writerow(row)
    # print("here3")
# print("careBot took", careBotMoves[0], "turns")  # Print the number of turns for the first scenario

careBot.reset()
