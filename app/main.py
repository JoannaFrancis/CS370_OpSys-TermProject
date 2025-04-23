#Entry point to run main loop 
import time
import RPi.GPIO as GPIO
from sensor import setup_sensor, get_distance

def main():
    try:
        setup_sensor()
        print("Ultrasonic sensor is running...")

        while True:
            distance = get_distance()
            print(f"Distance: {distance:.2f} cm")
            time.sleep(0.3)

    except KeyboardInterrupt:
        print("Stopping sensor...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()