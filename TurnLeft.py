import brickpi3

BP = brickpi3.BrickPi3()
speed = 50

try:
    while True:
        BP.set_motor_dps(BP.PORT_B, speed)
        BP.set_motor_dps(BP.PORT_C, -speed)
except KeyboardInterrupt:
    BP.reset_all()
