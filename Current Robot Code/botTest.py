from RobotClass import Robot
import time



careBot = Robot()
time.sleep(5)

# for i in range(0,10):
#     careBot.gyroTurn(100, -90)
#     careBot.driveStraightDist(100, 15)
#     careBot.gyroTurn(100, 90)
# while True:
#     careBot.gyro.printHeading()

careBot.strafe(1, 999, 14)











careBot.reset()