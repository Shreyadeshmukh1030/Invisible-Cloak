import time
import cv2

class BackgroundManager:
    def __init__(self, countdown_seconds=5):
        self.background = None
        self.countdown_seconds = countdown_seconds
        self.is_capturing = False
        self.capture_start_time = 0
        self.capture_completed = False
        self.countdown_val = countdown_seconds

    def start_capture(self):
        """Initiates the background capture process."""
        self.is_capturing = True
        self.capture_completed = False
        self.capture_start_time = time.time()
        self.countdown_val = self.countdown_seconds
        self.background = None

    def update(self, frame):
        """
        Updates the background capture state based on elapsed time.
        Returns the modified frame with countdown text, or the original frame if not capturing.
        """
        if not self.is_capturing:
            return frame

        elapsed_time = time.time() - self.capture_start_time
        remaining_time = max(0, self.countdown_seconds - int(elapsed_time))
        self.countdown_val = remaining_time

        display_frame = frame.copy()
        
        # Add overlay text
        cv2.putText(display_frame, "Capturing Background...", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(display_frame, "Please move out of the camera.", (50, 100), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
        
        # Huge countdown number
        cv2.putText(display_frame, str(remaining_time), (frame.shape[1]//2 - 50, frame.shape[0]//2 + 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 10, cv2.LINE_AA)

        if elapsed_time >= self.countdown_seconds:
            # Capture the background
            self.background = frame.copy()
            self.is_capturing = False
            self.capture_completed = True
            
        return display_frame

    def get_background(self):
        return self.background
    
    def has_background(self):
        return self.background is not None

    def reset(self):
        self.background = None
        self.is_capturing = False
        self.capture_completed = False
