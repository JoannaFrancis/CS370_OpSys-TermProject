#code to run the sensor
from gpiozero import DistanceSensor
from time import sleep
import RPi.GPIO as GPIO
import time

TRIG = 23
ECHO = 24

def setup_sensor():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)
    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    while GPIO.input(ECHO) == 0:
        pass
    time1 = time.time()
    while GPIO.input(ECHO) == 1:
        pass
    time2 = time.time()

    duration = time2 - time1
    distance_cm = duration * 340 / 2 * 100
    return round(distance_cm, 2)