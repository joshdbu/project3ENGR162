from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from math import remainder
from brickpi3 import BrickPi3, SensorError # type: ignore

import time

bp = BrickPi3()


class Gyro:
    def __init__(self):
        
        bp.set_sensor_type(bp.PORT_3, bp.SENSOR_TYPE.EV3_GYRO_ABS)  # type: ignore

        self._heading = 0
        self._pureHeading = 0
        self._offset = 0

    def heading(self):
        try:
            raw = bp.get_sensor(bp.PORT_3)
        except SensorError:
            pass
        else:
            self._heading = int((abs(int(raw / 360)) * raw + raw)) - self._offset

        return self._heading
    
    def rawHeading(self):
        try:
            raw = bp.get_sensor(bp.PORT_3)
        except SensorError:
            pass
        else:
            self._pureHeading = int((abs(int(raw / 360)) * raw + raw))
        
        return self._pureHeading
    
    def offset(self, value: int):
        self._offset = value

    def reset(self):
        self.offset(self.rawHeading())

    def printHeading(self):
        print('{: <4}'.format(self.heading()), end="\r")
        time.sleep(0.02)
