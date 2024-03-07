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
size = 40 # in cm



[a,b] = pointOne
[c,d] = pointTwo
[e,f] = pointThree
[g,h] = pointFour
[i,j] = pointFive
[k,l] = pointSix



# To point two
if(b != d):
    careBot.driveStriaghtDistNoGyro(200, size * (d - b))

careBot.turnDeg(100, -90)

if(c != a):
    careBot.driveStriaghtDistNoGyro(200, size * (c - a))

careBot.turnDeg(100, 90)

time.sleep(sleepTime)

# To point three
if(f != d):
    careBot.driveStriaghtDistNoGyro(200, size * (f - d))

careBot.turnDeg(100, -90)

if(e != c):
    careBot.driveStriaghtDistNoGyro(200, size * (e - c))

careBot.turnDeg(100, 90)

time.sleep(sleepTime)


# To point four
if(h != f):
    careBot.driveStriaghtDistNoGyro(200, size * (h - f))

careBot.turnDeg(100, -90)

if(g != e):
    careBot.driveStriaghtDistNoGyro(200, size * (g - e))

careBot.turnDeg(100, 90)

time.sleep(sleepTime)


# To point five
if(j != h):
    careBot.driveStriaghtDistNoGyro(200, size * (j - h))

careBot.turnDeg(100, -90)

if(i != g):
    careBot.driveStriaghtDistNoGyro(200, size * (i - g))

careBot.turnDeg(100, 90)

time.sleep(sleepTime)

# to point six
if(l != j):
    careBot.driveStriaghtDistNoGyro(200, size * (l - j))

careBot.turnDeg(100, -90)

if(k != i):
    careBot.driveStriaghtDistNoGyro(200, size * (k - i))

careBot.turnDeg(100, 90)
