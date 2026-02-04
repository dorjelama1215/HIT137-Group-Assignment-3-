# image_processor.py

import cv2
import numpy as np

class ImageProcessor:
    """
    Performs OpenCV image processing operations on numpy arrays.
    """

    def to_grayscale(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    def blur(self, image, ksize=5):
        if ksize % 2 == 0:
            ksize += 1
        return cv2.GaussianBlur(image, (ksize, ksize), 0)

    def edges(self, image, low_threshold=100, high_threshold=200):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, low_threshold, high_threshold)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    def adjust_brightness_contrast(self, image, brightness=0, contrast=1.0):
        """
        brightness: -100 to 100
        contrast: 0.5 to 2.0
        """
        img = image.astype("float32")
        img = img * contrast + brightness
        img = np.clip(img, 0, 255)
        return img.astype("uint8")

    def rotate(self, image, angle):
        if angle == 90:
            return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        elif angle == 180:
            return cv2.rotate(image, cv2.ROTATE_180)
        elif angle == 270:
            return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            return image

    def flip(self, image, mode="horizontal"):
        if mode == "horizontal":
            return cv2.flip(image, 1)
        elif mode == "vertical":
            return cv2.flip(image, 0)
        else:
            return image

    def resize(self, image, scale=1.0):
        if scale <= 0:
            return image
        h, w = image.shape[:2]
        new_w = int(w * scale)
        new_h = int(h * scale)
        return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    def remove_background(self, image):
        """
        Remove background using GrabCut algorithm.
        Returns image with transparent background (BGRA format).
        """
        # Create a copy to work with
        img = image.copy()
        
        # Create mask for GrabCut
        mask = np.zeros(img.shape[:2], np.uint8)
        
        # Create background and foreground models (required by GrabCut)
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)
        
        # Define rectangle around the foreground (assume center region)
        h, w = img.shape[:2]
        rect = (10, 10, w - 20, h - 20)
        
        # Apply GrabCut algorithm
        cv2.grabCut(img, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
        
        # Modify mask: set definite background and probable background to 0
        # definite foreground and probable foreground to 1
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        
        # Create alpha channel from mask
        alpha = mask2 * 255
        
        # Convert BGR to BGRA
        bgra = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        
        # Apply alpha channel
        bgra[:, :, 3] = alpha
        
        return bgra