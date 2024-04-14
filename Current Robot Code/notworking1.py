
import grovepi # type: ignore
import time

# set I2C to use the hardware bus
# grovepi.set_bus("RPI_1")
time.sleep(2)

# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND
ultrasonic_ranger = 6
print("Starting on port", ultrasonic_ranger)
while True:
    try:
        # Read distance value from Ultrasonic
        backLeft5 = grovepi.ultrasonicRead(5)
        frontLeft6 = grovepi.ultrasonicRead(6)
        front7 = grovepi.ultrasonicRead(7)
        print("bl:", backLeft5, "fl:", frontLeft6, "f:", front7)

    except Exception as e:
        print("here error!!")
        print ("Error:{}".format(e))
    
    time.sleep(0.1) # don't overload the i2c bus
