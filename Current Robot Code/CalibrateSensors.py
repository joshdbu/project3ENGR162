from IRClass import IRSensor
from MagnetClass import Magnet_Sensor

magnet = Magnet_Sensor()
ir = IRSensor()

temp = ir.IR_Read()
temp = magnet.Mag_Read()

irRead = ir.IR_Read()
magRead = magnet.Mag_Read()

irThresh = irRead * 0.8
magThresh = irRead * 0.8

print(f"IR raw: {irRead}   Suggested threshold: {irThresh}")
print(f"Magnet raw: {magRead}   Suggested threshold: {magThresh}")