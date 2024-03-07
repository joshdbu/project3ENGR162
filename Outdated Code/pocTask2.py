import time
from RobotClass import Robot

careBot = Robot()
time.sleep(5) #need this everywhere!!!!


# hallway thing
careBot.driveStraightUltra(200, 20)

# change to -90 if right turn, keep at 90 if left turn
careBot.gyroTurn(100,-90)

# drive straight for 200 cm
careBot.driveStraightDist(200, 200)
