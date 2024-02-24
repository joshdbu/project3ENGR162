from __future__ import print_function # use python 3 syntax but make it compatible with python 2
import grovepi # type: ignore
import time
from statistics import mean


class GroveUltra:
    def __init__(self, port):
        # set I2C to use the hardware bus
        grovepi.set_bus("RPI_1")
        # Connect the Grove Ultrasonic Ranger to digital port D4
        self.ultrasonic_ranger = port
        self._dist = 0

    def getDistance(self):
        vals = []
        for i in range(0,10):
            try:
                raw = grovepi.ultrasonicRead(self.ultrasonic_ranger)
            except Exception:
                pass
            else:
                vals.append(raw)
            time.sleep(0.01) # don't overload the i2c bus
        
        self._dist = mean(vals)

        return self._dist
    
    def printDistance(self):
        print('{: <10}'.format(self.getDistance()), end="\r")
        time.sleep(0.02)
    
    