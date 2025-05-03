# Alert system class for the buzzer
#test
from gpiozero import buzzer
from time import sleep 

class AlertSystem:
    def __init__(self, trigger_pin=18):
        self.buzzer = Buzzer(trigger_pin)

    def play_alert(self, distance_measured):
        try:
            if distance_measured <= 10.0:
                self.buzzer.on()
                sleep(0.05)
                self.buzzer.off()
            elif distance_measured <= 20.0:
                self.buzzer.on()
                sleep(0.1)
                self.buzzer.off()
            elif distance_measured <= 50.0:
                self.buzzer.on()
                sleep(0.2)
                self.buzzer.off()
            else:
                self.buzzer.off()
        except KeyboardInterrupt:
            print("Closing buzzer...")