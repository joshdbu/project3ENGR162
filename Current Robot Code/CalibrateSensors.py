from IRClass import IRSensor
from MagnetClass import Magnet_Sensor

magnet = Magnet_Sensor()
ir = IRSensor()

ir.IR_PrintValues()
magnet.Mag_PrintValues()