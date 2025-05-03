#Entry point to run main loop 
#test
from time import sleep
from sensor import UltrasonicSensor
from cam import CameraDisplay
from alert import AlertSystem 

def main():
    sensor = UltrasonicSensor()
    camera = CameraDisplay()
    alert_system = AlertSystem()

    try:
        while True:
            distance = sensor.get_distance_cm()
            camera.update_overlay(distance)
            camera.show()
            print(f"Distance: {distance:.2f} cm")
            alert_system.play_alert(distance)
            sleep(0.3)
    except KeyboardInterrupt:
        print("Exiting...")
        camera.cleanup()

if __name__ == "__main__":
    main()