__all__ = ['IMU']

from MPU9250 import MPU9250


class IMU:
    def __init__(self):
        self.mpu = MPU9250()

        self._accel = {'x': 0, 'y': 0, 'z': 0}
        self._gyro = {'x': 0, 'y': 0, 'z': 0}
        self._mag = {'x': 0, 'y': 0, 'z': 0}

    def accel(self):
        try:
            a = self.mpu.readAccel()
        except Exception:
            pass
        else:
            if a != self._accel:
                self._accel = a

        return self._accel

    def gyro(self):
        try:
            g = self.mpu.readGyro()
        except Exception:
            pass
        else:
            if g != self._gyro:
                self._gyro = g

        return self._gyro

    def mag(self):
        try:
            m = self.mpu.readMagnet()
        except Exception:
            pass
        else:
            if m != self._mag:
                self._mag = m

        return self._mag
