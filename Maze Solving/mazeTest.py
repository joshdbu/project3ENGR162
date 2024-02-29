from MapClass import Map
from SmartMouseClass import SmartMouse
import matplotlib.pyplot as plt
from MapClass import DemoMap
demoMap = DemoMap()
testMap = Map(2,0) 


jerry =  SmartMouse(2, 0, 7, 5, 6)
jerryMoves = []
jerryPaths = []

for i in range(0,1):
    jerryMove, jerryPath = jerry.solveMaze(testMap)
    jerryMoves.append(jerryMove)
    jerryPaths.append(jerryPath)
    jerry.reset()

minIndex = jerryMoves.index(min(jerryMoves))

for row in jerryPaths[0]:
    for value in row:
        print(value, end=' ')
    print()  # Add a newline after each row
print("jerry took", jerryMoves[0], "turns")

for row in jerryPaths[minIndex]:
    for value in row:
        print(value, end=' ')
    print()  # Add a newline after each row
print("jerry took", jerryMoves[minIndex], "turns")


# numMoveData = []

# for i in range (0,100):
#     jerry =  SmartMouse(testMap)
#     numMove = 0
#     while jerry.yPos < 5:
        
#         jerry.move(testMap)
#         numMove += 1
    
#     numMoveData.append(numMove)
    


# plt.hist(numMoveData, bins=20)
# plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
# plt.title("100 Iterations of Maze Algorithm on Test Map")
# plt.xlabel("Number of Turns for Iteration to Complete Maze")
# plt.ylabel("Number of Iterations Completing Maze")
# plt.show()

