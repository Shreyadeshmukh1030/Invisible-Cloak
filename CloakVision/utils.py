import cv2
from PIL import Image, ImageTk
import os
from datetime import datetime

def cv2_to_photoimage(cv2_image):
    """Converts an OpenCV image (BGR or grayscale) to a Tkinter PhotoImage."""
    if len(cv2_image.shape) == 2: # Grayscale
        img_rgb = cv2.cvtColor(cv2_image, cv2.COLOR_GRAY2RGB)
    else:
        img_rgb = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    
    img_pil = Image.fromarray(img_rgb)
    return ImageTk.PhotoImage(image=img_pil)

def save_screenshot(frame, directory="screenshots"):
    """Saves the given frame as an image file."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(directory, f"cloak_{timestamp}.png")
    cv2.imwrite(filename, frame)
    return filename

def get_lighting_status(frame):
    """Estimates lighting status based on frame brightness."""
    # Convert to grayscale to evaluate brightness
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mean_brightness = cv2.mean(gray)[0]
    
    if mean_brightness < 40:
        return "Low Light"
    elif mean_brightness > 220:
        return "Very Bright"
    elif 100 <= mean_brightness <= 180:
        return "Excellent"
    else:
        return "Good"
