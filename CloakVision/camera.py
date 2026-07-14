import cv2
import time

class Camera:
    def __init__(self, camera_index=0, resolution=(640, 480)):
        self.camera_index = camera_index
        self.resolution = resolution
        self.cap = None
        self.fps = 0
        self.prev_frame_time = 0
        
    def start(self):
        """Initializes the webcam."""
        if self.cap is None or not self.cap.isOpened():
            # In Windows, sometimes cv2.CAP_DSHOW provides faster startup
            self.cap = cv2.VideoCapture(self.camera_index)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            return self.cap.isOpened()
        return True

    def stop(self):
        """Releases the webcam."""
        if self.cap and self.cap.isOpened():
            self.cap.release()
            self.cap = None

    def get_frame(self):
        """Reads a frame from the webcam and calculates FPS."""
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1) # Flip horizontally for mirror effect
                self._calculate_fps()
                return True, frame
        return False, None

    def _calculate_fps(self):
        """Calculates frames per second."""
        new_frame_time = time.time()
        if self.prev_frame_time != 0:
            self.fps = 1 / (new_frame_time - self.prev_frame_time)
        self.prev_frame_time = new_frame_time

    def get_fps(self):
        return round(self.fps, 1)
    
    def get_resolution(self):
        if self.cap and self.cap.isOpened():
            w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            return f"{w}x{h}"
        return "Unknown"

    @staticmethod
    def get_available_cameras(max_tested=5):
        """Returns a list of available camera indices."""
        available_cameras = []
        for i in range(max_tested):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()
        return available_cameras
