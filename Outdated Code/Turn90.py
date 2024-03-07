import brickpi3

BP = brickpi3.BrickPi3()

speed = 50
degrees = 2.4 * 90

BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
BP.set_motor_limits(BP.PORT_B, 90, speed)
BP.set_motor_position(BP.PORT_B, degrees)
    
BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))
BP.set_motor_limits(BP.PORT_C, 90, speed) 
BP.set_motor_position(BP.PORT_C, -degrees)
