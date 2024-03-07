import time
from RobotClass import Robot


degrees = 90 # change to degrees of turn, positive is counterclockwise and negative is clockwise
careBot = Robot()
time.sleep(5) #need this everywhere!!!!

careBot.gyroTurn(100,degrees)
