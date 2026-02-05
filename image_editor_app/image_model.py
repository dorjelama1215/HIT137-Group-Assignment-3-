# image_model.py

import cv2
import numpy as np

class ImageModel:
    """
    Holds the current image, original image, file name, and undo/redo stacks.
    Demonstrates encapsulation and class interaction with ImageProcessor.
    """

    def __init__(self):
        self._original_image = None
        self._current_image = None
        self._file_path = None
        self._undo_stack = []
        self._redo_stack = []

    # Encapsulated getters
    def get_image(self):
        return self._current_image

    def get_filename(self):
        return self._file_path

    def get_dimensions(self):
        if self._current_image is None:
            return None
        h, w = self._current_image.shape[:2]
        return w, h

    # Core methods
    def load_image(self, file_path):
        image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        if image is None:
            raise ValueError("Could not load image.")
        self._file_path = file_path
        self._original_image = image.copy()
        self._current_image = image
        self._undo_stack.clear()
        self._redo_stack.clear()

    def save_image(self, file_path=None):
        if self._current_image is None:
            raise ValueError("No image to save.")
        
        path = file_path if file_path else self._file_path
        if not path:
            raise ValueError("No file path specified.")
        
        # Save with appropriate format
        cv2.imwrite(path, self._current_image)
        
        if file_path:
            self._file_path = file_path

    def apply_change(self, new_image):
        """Push current image to undo stack and set new image.
        Clears the redo stack to maintain correct history behaviour"""
        if self._current_image is not None:
            self._undo_stack.append(self._current_image.copy())
            self._redo_stack.clear()
        self._current_image = new_image

    def undo(self):
        if not self._undo_stack:
            return
        self._redo_stack.append(self._current_image.copy())
        self._current_image = self._undo_stack.pop()

    def redo(self):
        if not self._redo_stack:
            return
        self._undo_stack.append(self._current_image.copy())
        self._current_image = self._redo_stack.pop()
