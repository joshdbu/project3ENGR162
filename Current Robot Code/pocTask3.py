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
sleepTime = 0.1
size = 5 # in cm



[a,b] = pointOne
[c,d] = pointTwo
[e,f] = pointThree
[g,h] = pointFour
[i,j] = pointFive
[k,l] = pointSix



# To point two
if(b != d):
    careBot.driveStraightUntil(200, size * (d - b), 10000)

careBot.gyroTurn(100, -90)

if(c != a):
    careBot.driveStraightUntil(200, size * (c - a), 10000)

careBot.gyroTurn(100, 90)

time.sleep(sleepTime)

# To point three
if(f != d):
    careBot.driveStraightUntil(200, size * (f - d), 10000)

careBot.gyroTurn(100, -90)

if(e != c):
    careBot.driveStraightUntil(200, size * (e - c), 10000)

careBot.gyroTurn(100, 90)

time.sleep(sleepTime)


# To point four
if(h != f):
    careBot.driveStraightUntil(200, size * (h - f), 10000)

careBot.gyroTurn(100, -90)

if(g != e):
    careBot.driveStraightUntil(200, size * (g - e), 10000)

careBot.gyroTurn(100, 90)

time.sleep(sleepTime)


# To point five
if(j != h):
    careBot.driveStraightUntil(200, size * (j - h), 10000)

careBot.gyroTurn(100, -90)

if(i != g):
    careBot.driveStraightUntil(200, size * (i - g), 10000)

careBot.gyroTurn(100, 90)

time.sleep(sleepTime)

# to point six
if(l != j):
    careBot.driveStraightUntil(200, size * (l - j), 10000)

careBot.gyroTurn(100, -90)

if(k != i):
    careBot.driveStraightUntil(200, size * (k - i), 10000)

careBot.gyroTurn(100, 90)