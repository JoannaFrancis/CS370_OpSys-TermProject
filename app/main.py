#Entry point to run main loop 
import threading
import time
from sensor import UltrasonicSensor
from sensor_thread import SensorThread
from cam_thread  import CameraThread
from alert_thread import AlertThread

class SharedState:
    def __init__(self):
        self.distance = 100.0 #Dummy Value needed to avoid attributeError on start up 
        self.lock = threading.Lock()
def main():
    shared_state = SharedState()

    sensor_thread = SensorThread(shared_state)
    camera_thread = CameraThread(shared_state)
    alert_thread = AlertThread(shared_state)

    sensor_thread.start()
    camera_thread.start()
    alert_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down threads...")
        sensor_thread.running = False
        camera_thread.running = False
        alert_thread.running = False
        sensor_thread.join()
        camera_thread.join()
        alert_thread.join()
        print("Exited cleanly.")
if __name__ == "__main__":
    main()