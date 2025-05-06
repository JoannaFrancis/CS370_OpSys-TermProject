#code to control back up camera logic
import threading
import cv2
import numpy as np
from picamera2 import Picamera2
from time import sleep

class CameraThread(threading.Thread):
    def __init__(self, shared_state):
        super().__init__()
        self.shared_state = shared_state
        self.running = True  # Allows controlled shutdown
        self.daemon = True   # Thread exits when main program exits
        self.picam2 = Picamera2()  # Initialize the camera
        self.picam2.configure(self.picam2.create_video_configuration())
        self.picam2.start()
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2()

    def run(self):
        while self.running:
            frame = self.picam2.capture_array()
            # Resize the frame to fit the screen resolution (native resolution 800x480)(max resolution 1920x1080)
            frame_resized = cv2.resize(frame, (800, 480))

            # Access the shared distance and overlay it on the camera feed
            with self.shared_state.lock:
                distance = self.shared_state.distance

            # Overlay the distance text on the frame
            cv2.putText(frame_resized, f"Distance: {distance:.2f} cm", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Draw a red bounding box if distance is within a certain range (e.g., 20 cm)
            if distance <= 20.0:
               # Convert to greyscale to reduce image noise
                gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)

                # Apply Gaussian blur to reduce high-frequency noise/reflections
                blurred = cv2.GaussianBlur(gray, (5, 5), 0)

                #Seperate foreground from background in variable light
                thresh = cv2.adaptiveThreshold(
                    blurred,                
                    255,                    
                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  # Gaussian weight of neighborhood
                    cv2.THRESH_BINARY_INV,  # Invert the output (objects = white, background = black)
                    11,                     # Block size 
                    2                       # Tunes sensitivity
                )

                # Find external contours from the binary image (white objects on black background)
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Loop through each contour found
                for contour in contours:
                    area = cv2.contourArea(contour)  # Calculate the contour area in pixels

                    # Filter out too-small or too-large contours to eliminate noise and large reflections
                    if 800 < area < 5000:  # ajust lower bounds to filter small reflections or upper bound to exclude large background regions
                        x, y, w, h = cv2.boundingRect(contour)  # Get the bounding box coordinates
                        cv2.rectangle(frame_resized, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Draw red rectangle
                 # Display the updated frame
                cv2.imshow("Camera Feed", frame_resized)

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    def cleanup(self):
        # Stop the camera and close OpenCV windows
        self.picam2.stop()
        cv2.destroyAllWindows()