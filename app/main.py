#Entry point to run main loop 
from time import sleep
from sensor import UltrasonicSensor

def main():
    sensor = UltrasonicSensor()

    try:
        while True:
            distance = sensor.get_distance_cm()
            print(f"Distance: {distance:.2f} cm")
            sleep(0.3)
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()