#code to control back up camera logic
#test

from picamera2 import Picamera2
import cv2
from time import sleep

class CameraDisplay:
    def __init__(self):
        # Initialize camera
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_video_configuration())

    def start(self):
        # Start the camera
        self.picam2.start()

    def update_overlay(self, distance):
        # Convert the image to RGB (required by OpenCV)
        frame = self.picam2.capture_array()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_YUV2RGB_I420)

        # Overlay text on the frame (distance in cm)
        cv2.putText(rgb_frame, f"Distance: {distance:.2f} cm", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Draw a box if within range
        if distance <= 20.0:  # You can adjust the range
            cv2.rectangle(rgb_frame, (50, 50), (250, 250), (0, 0, 255), 2)

        # Display the camera feed
        cv2.imshow("Camera Feed", rgb_frame)

    def show(self):
        # Keep the camera feed running
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False
        return True

    def cleanup(self):
        self.picam2.stop()
        cv2.destroyAllWindows()