from MazeRobotClass import MazeRobot
import time

carebot = MazeRobot()

try:    
    while True:
        val = carebot.avoidThings(0,0,3,3,7)
        if val == 0:
            print("Nothing found.")
        time.sleep(1)
        
except KeyboardInterrupt:
    pass