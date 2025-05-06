# Alert system class for the buzzer
#test
import threading
from gpiozero import Buzzer
from time import sleep

class AlertThread(threading.Thread):
    def __init__(self, shared_data, buzzer_pin=18):
        super().__init__()
        self.buzzer = Buzzer(buzzer_pin)
        self.shared_data = shared_data
        self.daemon = True

    def run(self):
        self.buzzer.on()
        while True:
            distance = self.shared_data.distance  # default to 100cm
            if distance <= 10:
                self.buzzer.beep(0.2, 0.2, None, False)
            elif distance <= 20:
                self.buzzer.beep(0.2, 0.1, None, False)
            elif distance <= 50:
                self.buzzer.beep(0.1, 0.05, None, False)       
            else:
                self.buzzer.off()
                sleep(0.2)
