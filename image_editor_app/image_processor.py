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
       
        return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
