#code to control back up camera logic
import threading
import cv2
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

    def run(self):
        while self.running:
            frame = self.picam2.capture_array()

            # Convert frame to RGB (needed by OpenCV)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_YUV2RGB_I420)

            # Access the shared distance and overlay it on the camera feed
            with self.shared_state.lock:
                distance = self.shared_state.distance

            # Overlay the distance text on the frame
            cv2.putText(rgb_frame, f"Distance: {distance:.2f} cm", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Draw a red box if distance is within a certain range (e.g., 20 cm)
            if distance <= 20.0:
                cv2.rectangle(rgb_frame, (50, 50), (250, 250), (0, 0, 255), 2)

            # Display the updated frame
            cv2.imshow("Camera Feed", rgb_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def cleanup(self):
        # Stop the camera and close OpenCV windows
        self.picam2.stop()
        cv2.destroyAllWindows()