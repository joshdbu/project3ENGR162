import math
import time
from RobotClass import Robot

careBot = Robot()
time.sleep(5) #need this everywhere!!!!

pointOne = [0, 0]
pointTwo = [2, 2]
pointThree = [2, 0]
pointFour = [0, 0]
pointFive = [1,1]
pointSix = [0,0]
sleepTime = 5
size = 10 # in cm



[a,b] = pointOne
[c,d] = pointTwo
[e,f] = pointThree
[g,h] = pointFour
[i,j] = pointFive
[k,l] = pointSix



# To point two
if(b != d):
    careBot.driveStraightDist(200, size * (d - b))

careBot.gyroTurn(100, -90)

if(c != a):
    careBot.driveStraightDist(200, size * (c - a))

careBot.gyroTurn(100, 90)

time.sleep(sleepTime)

# To point three
if(f != d):
    careBot.driveStraightDist(200, size * (f - d))

careBot.gyroTurn(100, -90)

if(e != c):
    careBot.driveStraightDist(200, size * (e - c))

careBot.gyroTurn(100, 90)

time.sleep(sleepTime)


# To point four
if(h != f):
    careBot.driveStraightDist(200, size * (h - f))

careBot.gyroTurn(100, -90)

if(g != e):
    careBot.driveStraightDist(200, size * (g - e))

careBot.gyroTurn(100, 90)

time.sleep(sleepTime)


# To point five
if(j != h):
    careBot.driveStraightDist(200, size * (j - h))

careBot.gyroTurn(100, -90)

if(i != g):
    careBot.driveStraightDist(200, size * (i - g))

careBot.gyroTurn(100, 90)

time.sleep(sleepTime)

# to point six
if(l != j):
    careBot.driveStraightDist(200, size * (l - j))

careBot.gyroTurn(100, -90)

if(k != i):
    careBot.driveStraightDist(200, size * (k - i))

careBot.gyroTurn(100, 90)