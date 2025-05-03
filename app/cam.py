#code to control back up camera logic
import cv2

class CameraDisplay:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def update_overlay(self, distance):
        self.overlay_distance = distance

    def show(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        if self.overlay_distance < 50:
            color = (0, 0, 255)  # Red
            cv2.putText(frame, f"WARNING: {self.overlay_distance:.1f} cm", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.rectangle(frame, (100, 100), (540, 380), color, 3)
        else:
            cv2.putText(frame, f"Distance: {self.overlay_distance:.1f} cm", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Backup Camera", frame)
        cv2.waitKey(1)

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()