import grovepi
import time

ultrasonic1 = 5
ultrasonic2 = 6
ultrasonic3 = 7

grovepi.pinMode(ultrasonic1, "INPUT")
grovepi.pinMode(ultrasonic2, "INPUT")

while True:
    print("Sensor 1: ")
    print(grovepi.ultrasonicRead(ultrasonic1))
    print("Sensor 2: ")
    print(grovepi.ultrasonicRead(ultrasonic2))
    print("Sensor 3: ")
    print(grovepi.ultrasonicRead(ultrasonic3))
    time.sleep(0.1)