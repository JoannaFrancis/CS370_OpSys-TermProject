#code to run the sensor
#test
from gpiozero import DistanceSensor
from time import sleep

class UltrasonicSensor:
    def __init__(self, trigger_pin=23, echo_pin=24):
        self.sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin)

    def get_distance_cm(self):
        return self.sensor.distance * 100