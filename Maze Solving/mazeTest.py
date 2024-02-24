from MapClass import Map
from SmartMouseClass import SmartMouse
import matplotlib.pyplot as plt

testMap = Map(2,0) 



numMoveData = []

for i in range (0,1000):
    jerry =  SmartMouse(testMap)
    numMove = 0
    while jerry.yPos < 5:
        
        jerry.move(testMap)
        numMove += 1
    
    numMoveData.append(numMove)
    


plt.hist(numMoveData)
plt.show()