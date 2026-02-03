"""This section contains the image processing class
which is responsible for all image processing operations using openCV"""
import cv2
import numpy as np
class ImageProcessor:
    """Image processor class performs manipulation of images
    also shoes encapsulation by binding differnt methods"""
    
    def __init__(self):
        """Initializes the Imageprocessor object 
        Arg:
        img=current working image 
        orignal=Copy of original image""" 
        self.image=None
        self.original=None

    def load_image(self):
        """Responsible for loading the image
        Takes argument as path to the image file and returns the loaded image"""
        self.image=cv.imread(path)
        self.original=self.image.copy()
        return self.image
    
    def grayscale(self):
        """Converts the image into grayscale"""
        gray=cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        self=cv2.cvtColor(self.image,cv2.COLOR_GRAY2BGR)
        returns self.image
    
    def blur(self,value):
        """Applies Gaussan Blur to the image
        Takes argument as blur intensity level and returns the blur image"""
        kernel_size=value*2+1
        self.image=cv2.GaussianBlur(self.image,(kernel_size,kernel_size),0)
        return self.image 

    def edge_detection(self):
        """Applies canny edge detection
        returns the edged image"""
        edges=cv2.canny(self.image,100,200)
        self.image=cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)
        return self.image

    def 

        
    

    