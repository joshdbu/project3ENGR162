from IRClass import IRSensor
from MagnetClass import Magnet_Sensor

magnet = Magnet_Sensor()
ir = IRSensor()

temp = ir.IR_Read()
temp = magnet.Mag_Read()

temp = input("Press enter to take IR reading.")
irRead = ir.IR_Read()
temp = input("Press enter to take magnet reading.")
magRead = magnet.Mag_Read()

irThresh = irRead * 0.8
magThresh = round(magRead[3] * 0.8, 1)

print(f"IR raw: {irRead}   Suggested threshold: {irThresh}")
print(f"Magnet raw: {round(magRead[3], 1)}   Suggested threshold: {magThresh}")