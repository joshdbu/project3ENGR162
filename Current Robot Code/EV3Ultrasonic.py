from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from math import remainder
from brickpi3 import BrickPi3, SensorError # type: ignore
from statistics import median
import time

bp = BrickPi3()


class EV3Ultra:
    def __init__(self, measure):
        
        bp.set_sensor_type(bp.PORT_1, bp.SENSOR_TYPE.EV3_ULTRASONIC_CM)  # type: ignore

        self._distance = 0
        self._offset = 0
        self.numMeasure = 10

    def distance(self):
        try:
            temp = 255
            while(temp > 250) & (temp < 260):
                temp = bp.get_sensor(bp.PORT_1)
            
        except SensorError:
            pass

        return temp

    def getDistance(self):
        sum = []
        for i in range(1, self.numMeasure):
            
            sum.append(self.distance())
            time.sleep(0.02)
        avg = median(sum)

        return avg
        

    def offset(self, value: int):
        self._offset = value


    def printDistance(self):
        print('{: <4}'.format(self.distance()), end="\r")
        time.sleep(0.02)
