#Entry point to run main loop 
#test
from time import sleep
from sensor import UltrasonicSensor
from cam import CameraDisplay
from alert import AlertSystem 

def main():
    sensor = UltrasonicSensor()
    camera = CameraDisplay()  # no alert system passed here
    alert_system = AlertSystem()  # alert system is separate

    camera.start()  # Start the camera

    try:
        while True:
            distance = sensor.get_distance_cm()  # Get distance from sensor
            camera.update_overlay(distance)  # Update camera overlay
            camera.show()  # Show the camera feed

            print(f"Distance: {distance:.2f} cm")  # Print to terminal
            alert_system.play_alert(distance)  # Play an alert based on distance
            sleep(0.3)
    except KeyboardInterrupt:
        print("Exiting...")
        camera.cleanup()  # Clean up camera resources

if __name__ == "__main__":
    main()