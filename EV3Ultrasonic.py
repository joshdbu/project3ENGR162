from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from math import remainder
from brickpi3 import BrickPi3, SensorError # type: ignore
from statistics import mean
import time

bp = BrickPi3()


class EV3Ultra:
    def __init__(self):
        
        bp.set_sensor_type(bp.PORT_3, bp.SENSOR_TYPE.EV3_ULTRASONIC_CM)  # type: ignore

        self._distance = 0
        self._offset = 0

    def distance(self):
        try:
            raw = bp.get_sensor(bp.PORT_1)[0]
        except SensorError:
            pass
        else:
            self._heading = int(remainder(raw, 360)) + self._offset

        return self._heading

    def avgDist(self):
        sum = []
        for i in range(1,6):
            sum.append(self.distance())
        avg = mean(sum)

        return avg
        

    def offset(self, value: int):
        self._offset = value


    def printDistance(self):
        print('{: <4}'.format(self.distance()), end="\r")
        time.sleep(0.02)
