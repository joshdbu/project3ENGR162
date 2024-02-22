import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import math

from MapClass import Map
from RobotClass import Robot

careBot = Robot()

radius = 10
reading = 821 * exp(-0.215 * radius)

careBot.gyroTurn(180, -90)
# move(radius)
careBot.gyroTurn(180, 90)
# move(radius * 2.5)
careBot.gyroTurn(180, 90)
# move(radius)
careBot.gyroTurn(180, -90)




