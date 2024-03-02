from MapClass import Map
from DumbMouseClass import DumbMouse
from SmartMouseClass import SmartMouse
from RobotClass import Robot
import time
from MazeRobotClass import MazeRobot

# testMap = Map(2,0) 
# tom = DumbMouse(testMap)
# jerry =  SmartMouse(testMap)
careBot = MazeRobot(2, 0, 7, 5, 6)

start = time.perf_counter()
while (time.perf_counter() - start) < 1:
    pass      # gives time for gyro to calibrate

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
move, path = careBot.solveMaze()

# try:
#     for i in range(0,10):
#         careBot.turnDeg(100, -90)
#         careBot.driveStriaghtDistNoGyro(200, 15)
#         careBot.turnDeg(100, 90)
# except KeyboardInterrupt:
#             careBot.reset()
# careBot.driveStriaghtDistNoGyro(100, 100)

# careBot.driveStraightDist(200, 15)
