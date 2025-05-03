#Entry point to run main loop 
from time import sleep
from sensor import UltrasonicSensor
from app.cam import CameraDisplay

def main():
    sensor = UltrasonicSensor()
    camera = CameraDisplay()

    try:
        while True:
            distance = sensor.get_distance_cm()
            camera.update_overlay(distance)
            camera.show()
            print(f"Distance: {distance:.2f} cm")
            sleep(0.3)
    except KeyboardInterrupt:
        print("Exiting...")
        camera.cleanup()

if __name__ == "__main__":
    main()