import brickpi3

try:
    while True:
        BP = brickpi3.BrickPi3()
        BP.set_motor_dps(BP.PORT_B, 30)
        BP.set_motor_dps(BP.PORT_C, 30)
except KeyboardInterrupt:
    BP.set_motor_dps(BP.PORT_B, 0)
    BP.reset_all()
