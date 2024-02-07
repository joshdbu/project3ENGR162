from MapClass import Map
from DumbMouseClass import DumbMouse
from SmartMouseClass import SmartMouse


testMap = Map(2,0) 
tom = DumbMouse(testMap)
jerry =  SmartMouse(testMap)


numMove = 0
while tom.yPos < 5:
    
    tom.move(testMap)
    numMove += 1
    tom.printChar()
print('Tom completed the maze in ', numMove, ' moves. His final yPos is ', tom.yPos, ' and his final x position is ', tom.xPos)
numMove = 0

while jerry.yPos < 5:
    
    jerry.move(testMap)
    numMove += 1
print('Jerry completed the maze in ', numMove, ' moves. His final yPos is ', tom.yPos, ' and his final x position is ', tom.xPos)