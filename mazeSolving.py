from MapClass import Map
from DumbMouseClass import DumbMouse


testMap = Map(2,0) 
tom = DumbMouse(testMap)
#jerry = 


numMove = 0
while tom.yPos < 5:
    
    tom.move(testMap)
    numMove += 1
    tom.printChar()
print('Tom completed the maze in ', numMove, ' moves. His final yPos is ', tom.yPos, ' and his final x position is ', tom.xPos)