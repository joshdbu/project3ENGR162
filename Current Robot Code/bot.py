from MapClass import Map
from DumbMouseClass import DumbMouse
from SmartMouseClass import SmartMouse
from RobotClass import Robot
import time

testMap = Map(2,0) 
tom = DumbMouse(testMap)
jerry =  SmartMouse(testMap)
careBot = Robot()
time.sleep(5) # gives time for gyro to calibrate

#careBot.drive()
#careBot.turnDeg(250, 90)
careBot.gyroTurn(150, -45)
#careBot.driveStraightDist(100, 15)
#careBot.getHeading()
# careBot.moveForward(100)
#careBot.getHeading()



# numMove = 0
# while tom.yPos < 5:
    
#     tom.move(testMap)
#     numMove += 1
    
# print('Tom completed the maze in ', numMove, ' moves. His final yPos is ', tom.yPos, ' and his final x position is ', tom.xPos)
# numMove = 0

# while jerry.yPos < 5:
# #while numMove <= 10:
    
#     jerry.move(testMap)
#     numMove += 1
# print('Jerry completed the maze in ', numMove, ' moves. His final yPos is ', jerry.yPos, ' and his final x position is ', jerry.xPos)
# #print(jerry.mouseMap)

