#wraps sensor in a thread for continuous background polling
import threading
from sensor import UltrasonicSensor
from time import sleep

class SensorThread(threading.Thread):
    def __init__(self, shared_state, trigger_pin=23, echo_pin=24):
        super().__init__()
        self.sensor = UltrasonicSensor(trigger_pin, echo_pin)
        self.shared_state = shared_state
        self.running = True  # Allows controlled shutdown
        self.daemon = True   # Thread exits when main program exits

    def run(self):
        while self.running:
            distance = self.sensor.get_distance_cm()

            # Thread-safe update of shared distance
            with self.shared_state.lock:
                self.shared_state.distance = distance

            sleep(0.1)  # Poll every 100 ms