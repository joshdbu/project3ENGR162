from MapClass import Map
from DumbMouseClass import DumbMouse
from SmartMouseClass import SmartMouse
from RobotClass import Robot
import time
from MazeRobotClass import MazeRobot

# testMap = Map(2,0) 
# tom = DumbMouse(testMap)
# careBot =  SmartMouse(testMap)
careBot = MazeRobot(1, 0, 7, 2, 6)

time.sleep(5)

# hi Josh
# while True:
#     print(careBot.explore())
#     time.sleep(0.02)

#careBot.squareUp(50)
# while True:
#     print(careBot.backLeftUltra.getDistance(), " | ", careBot.frontLeftUltra.getDistance())
#careBot.getFrontUltraDist()
# careBot.driveStraightUltra(200, 15)
#careBot.gyroTurn(100,90)
#careBot.driveStraightUntil(200, 20, 20)


careBotMoves = []
careBotPaths = []

for i in range(0,1):
    careBotMove, careBotPath = careBot.solveMaze()
    careBotMoves.append(careBotMove)
    careBotPaths.append(careBotPath)
    careBot.reset()

minIndex = careBotMoves.index(min(careBotMoves))

for row in careBotPaths[0]:
    for value in row:
        print(value, end=' ')
    print()  # Add a newline after each row
print("careBot took", careBotMoves[0], "turns")

# try:
#     for i in range(0,10):
#         careBot.turnDeg(100, -90)
#         careBot.driveStriaghtDistNoGyro(200, 15)
#         careBot.turnDeg(100, 90)
# except KeyboardInterrupt:
#             careBot.reset()
# careBot.driveStriaghtDistNoGyro(100, 100)

# careBot.driveStraightDist(200, 15)
