from MapClass import Map
from DumbMouseClass import DumbMouse
from SmartMouseClass import SmartMouse
from RobotClass import Robot
import time

# testMap = Map(2,0) 
# tom = DumbMouse(testMap)
# jerry =  SmartMouse(testMap)
careBot = Robot()
time.sleep(4) # gives time for gyro to calibrate


# while True:
#     print(careBot.explore())
#     time.sleep(0.02)

#careBot.squareUp(50)
# while True:
#     print(careBot.backLeftUltra.getDistance(), " | ", careBot.frontLeftUltra.getDistance())
#careBot.getFrontUltraDist()
# careBot.driveStraightUltra(200, 15)
careBot.gyroTurn(100,90)
careBot.driveStraightDist(200, 20)
careBot.gyroTurn(100, -90)
# careBot.driveStraightDist(200, 10)
# careBot.gyroTurn(100, 90)
# careBot.driveStraightDist(200, 15)


