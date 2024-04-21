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
# while True:
#     careBot.frontUltra.printDistance()


# careBot.driveStraightUntil(200, 40, 1)
# careBot.gyroTurn(150,-90)
# careBot.driveStraightUntil(200,40,1)
# careBot.gyroTurn(150,90)
# careBot.driveStraightUntil(200,40,1)
# careBot.gyroTurn(150,-90)
# careBot.driveStraightUntil(200,40,1)
# careBot.driveStraightUntil(200,40,1)
# careBot.gyroTurn(150,-90)
# careBot.driveStraightUntil(200,40,1)
# careBot.driveStraightUntil(200,4000,12)
# careBot.driveStraightDist(-200, -40)
# while True:
#     careBot.explore()
while True:
    careBot.turnUltra(-98)
    time.sleep(0.25)
    careBot.turnUltra(98)


# careBot.dropCargo(2000, 700)
# careBot.driveStraightUntil(-200,-40,0.0001)
# careBot.gyroTurn(150, 900)
# while True:
#     print(careBot.rightUltra.distance())
#     time.sleep(2)

# while True:
#     x = careBot.explore()
#     # print("right", careBot.rightUltra.getDistance(), "front", careBot.frontUltra.getDistance(), "fl", careBot.frontLeftUltra.getDistance(), "bl", careBot.backLeftUltra.getDistance())
#     # print("front", careBot.frontUltra.getDistance())
#     # print("fl", careBot.frontLeftUltra.getDistance())
#     # print("bl", careBot.backLeftUltra.getDistance())
#     time.sleep(5)









careBot.reset()