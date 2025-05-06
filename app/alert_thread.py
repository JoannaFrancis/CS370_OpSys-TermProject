# Alert system class for the buzzer
#test
import threading
from gpiozero import Buzzer
from time import sleep

class AlertThread(threading.Thread):
    def __init__(self, shared_data, buzzer_pin=17):
        super().__init__()
        self.buzzer = Buzzer(buzzer_pin)
        self.shared_data = shared_data
        self.daemon = True

    def run(self):
        self.buzzer.on()
        while True:
            distance = self.shared_data.distance  # default to 100cm
            if distance <= 10:
                self.buzzer.on()
                sleep(0.05)
                self.buzzer.off()
            elif distance <= 20:
                self.buzzer.on()
                sleep(0.1)
                self.buzzer.off()
            elif distance <= 50:
                self.buzzer.on()
                sleep(0.2)
                self.buzzer.off()    
            else:
                self.buzzer.off()
                sleep(0.2)
