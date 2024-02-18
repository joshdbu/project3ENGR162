from math import remainder
from brickpi3 import BrickPi3, SensorError
from __future__ import print_function # use python 3 syntax but make it compatible with python 2
import time

bp = BrickPi3()


class Gyro:
    def __init__(self, port: int):
        self.port = port
        bp.set_sensor_type(self.port, bp.SENSOR_TYPE.EV3_GYRO_ABS_DPS)  # type: ignore

        self._heading = 0
        self._offset = 0

    def heading(self):
        try:
            raw = bp.get_sensor(self.port)[0]
        except SensorError:
            pass
        else:
            self._heading = int(remainder(raw, 360)) + self._offset

        return self._heading
    
    def offset(self, value: int):
        self._offset = value

    def reset(self):
        self.offset(-self.heading())

    def printHeading(self):
        print(self.heading())
        time.sleep(0.02)
