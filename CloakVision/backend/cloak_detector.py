import cv2
import numpy as np

class CloakDetector:
    def __init__(self):
        self.lower_hsv = np.array([0, 0, 180])
        self.upper_hsv = np.array([180, 40, 255])
        self.opening_kernel_size = 3
        self.closing_kernel_size = 3
        self.blur_ksize = 5
        self.white_pixels_percent = 0
        self.mask_pixels = 0
        
        self.use_mediapipe = False
        self.mp_pose = None
        self.pose = None
        try:
            import mediapipe as mp
            self.mp_pose = mp.solutions.pose
            self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
            self.mp_available = True
        except Exception as e:
            print(f"MediaPipe Pose not available: {e}")
            self.mp_available = False

    def update_hsv_thresholds(self, lower, upper):
        self.lower_hsv = np.array(lower)
        self.upper_hsv = np.array(upper)

    def update_filter_params(self, open_k, close_k, blur_k):
        self.opening_kernel_size = max(1, open_k | 1)
        self.closing_kernel_size = max(1, close_k | 1)
        self.blur_ksize = max(1, blur_k | 1)

    def toggle_mediapipe(self, state):
        if self.mp_available:
            self.use_mediapipe = state

    def get_pose_mask(self, frame, shape):
        mask = np.zeros(shape[:2], dtype=np.uint8)
        if not self.use_mediapipe or not self.pose:
            mask.fill(255)
            return mask

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)

        if results.pose_landmarks:
            h, w = shape[:2]
            points = []
            for landmark in results.pose_landmarks.landmark:
                if landmark.visibility > 0.3:
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    points.append([cx, cy])
            if points:
                points = np.array(points, np.int32)
                hull = cv2.convexHull(points)
                cv2.drawContours(mask, [hull], 0, 255, -1)
                kernel = np.ones((50, 50), np.uint8)
                mask = cv2.dilate(mask, kernel, iterations=2)
                return mask
                
        mask.fill(255)
        return mask

    def apply_cloak(self, frame, background):
        if background is None:
            return frame

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask_white = cv2.inRange(hsv, self.lower_hsv, self.upper_hsv)
        
        if self.use_mediapipe:
            pose_mask = self.get_pose_mask(frame, frame.shape)
            mask_white = cv2.bitwise_and(mask_white, pose_mask)
        
        kernel_open = np.ones((self.opening_kernel_size, self.opening_kernel_size), np.uint8)
        mask_white = cv2.morphologyEx(mask_white, cv2.MORPH_OPEN, kernel_open)
        
        kernel_close = np.ones((self.closing_kernel_size, self.closing_kernel_size), np.uint8)
        mask_white = cv2.morphologyEx(mask_white, cv2.MORPH_CLOSE, kernel_close)
        
        mask_white = cv2.GaussianBlur(mask_white, (self.blur_ksize, self.blur_ksize), 0)
        mask_white = cv2.medianBlur(mask_white, self.blur_ksize)
        
        self.mask_pixels = cv2.countNonZero(mask_white)
        total_pixels = mask_white.shape[0] * mask_white.shape[1]
        self.white_pixels_percent = (self.mask_pixels / total_pixels) * 100

        mask_inv = cv2.bitwise_not(mask_white)
        res1 = cv2.bitwise_and(background, background, mask=mask_white)
        res2 = cv2.bitwise_and(frame, frame, mask=mask_inv)
        
        output = cv2.addWeighted(res1, 1, res2, 1, 0)
        return output
