from __future__ import print_function 
import grovepi # type: ignore
from statistics import mean

class IRSensor:
    def __init__(self): 
       self.sensor1 = 8		# Pin 8 is A0 Port
       self.sensor2 = 9		# Pin 9 is A0 Port 
       grovepi.pinMode(self.sensor1,"INPUT")
       grovepi.pinMode(self.sensor2,"INPUT")

    # print function
    def IR_PrintValues(self):
       reading = self.IR_Read()
       print ("IR reading: " + str(reading))

    #Read Function		
    def IR_Read(self): 
        print("Reading IR Now")
        readList = []
        for j in range(10):
            temp = grovepi.analogRead(self.sensor1)
            temp = grovepi.analogRead(self.sensor2)
        for i in range(10):
            sensor1_value = grovepi.analogRead(self.sensor1)
            sensor2_value = grovepi.analogRead(self.sensor2)
            avgValue = (sensor1_value + sensor2_value) / 2   
            readList.append(avgValue)
        meanValue = mean(readList)
        return meanValue