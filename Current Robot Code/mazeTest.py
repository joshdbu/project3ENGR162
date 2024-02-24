from MapClass import Map
from SmartMouseClass import SmartMouse
import matplotlib.pyplot as plt

testMap = Map(2,0) 



numMoveData = []

for i in range (0,100000):
    jerry =  SmartMouse(testMap)
    numMove = 0
    while jerry.yPos < 5:
        
        jerry.move(testMap)
        numMove += 1
    
    numMoveData.append(numMove)
    


plt.hist(numMoveData, bins=20)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.title("100,000 Iterations of Maze Algorithm on Test Map")
plt.xlabel("Number of Turns for Iteration to Complete Maze")
plt.ylabel("Number of Iterations Completing Maze")
plt.show()

