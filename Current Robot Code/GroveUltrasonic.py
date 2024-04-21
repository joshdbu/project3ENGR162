from __future__ import print_function # use python 3 syntax but make it compatible with python 2
import grovepi # type: ignore
import time
from statistics import median


class GroveUltra:
    def __init__(self, port, measure):
        # set I2C to use the hardware bus
        grovepi.set_bus("RPI_1")
        # Connect the Grove Ultrasonic Ranger to digital port D4
        self.ultrasonic_ranger = port
        self._dist = 0
        self.numMeasure = measure

    def GetDistFast(self):
        print("here1")
        raw = grovepi.ultrasonicRead(self.ultrasonic_ranger)
        print("here2")
        time.sleep(0.02) # don't overload the i2c bus            


        return raw
    
    def getDistance(self):
        vals = []

        # print("get here1")
        measure = 0
        for i in range(0,self.numMeasure): # halved from 10 to 5 to shorten cycle time
            try:
                raw = grovepi.ultrasonicRead(self.ultrasonic_ranger)
                # print("raw is:", raw)
                count = 0
                while ((raw > 400) | (raw < 5)) & (count < 10):
                    # print("bad reading")
                    raw = grovepi.ultrasonicRead(self.ultrasonic_ranger)
                    count = count + 1
                measure += count        
            except Exception:
                pass
            else:
                vals.append(raw)
            time.sleep(0.02) # don't overload the i2c bus
            
        self._dist = median(vals)
        # print(self._dist, "count was:", measure)
        # if self._dist < 10:
        #     print("less than 10!--- ", vals)

        return self._dist
    
    def printDistance(self):
        # print(self.getDistance())
        print(self.GetDistFast())
        # print('{: <10}'.format(self.getDistance()), end="\r")
        time.sleep(0.02)
    