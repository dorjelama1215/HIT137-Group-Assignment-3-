"""This section contains the file handling class which manages the opening and closing of
the files in the file dialog box"""

from tkinter import filedialog,messagebox
import cv2
import os 

class FileHandler:
    """This class is responsible for managing image file input and output operation
    Demonstrates encapsulation by isolating all file handling topics"""

    def __init__(self):
        """Initializes the FileHandler objects
        Attributes current_file_path(str):Stores the path of the currently opened file"""

        self.current_file_path=None

    def openfile(self):
        """Opens a file dialog to open a file selected by the user
        Returns str if a file is selected and none is no file is selected"""
        filepath= filedialog.askopenfilename(
        title="Open Image",
        filetypes=[
            ("Image Files","*.jpeg *.jpg *.png *.bmp")
        ]
    )
        if not filepath:
            return None
        self.current_file_path=filepath
        return filepath

    def savefile(self,image):
        """Saves the image to the current file path
        If no file path exists the method redirects to save as file operation""" 

        if self.current_file_path is None:
            self.savefileas(image)
        else:
            cv2.imwrite(self.current_file_path,image)
            messagebox.showinfo("Saved","Image saved successfully")
            
        
    
    def savefileas(self,image):
        """Opens a save as dialog to save the image with a new name"""
        filepath=filedialog.asksaveasfilename(
        title="Save image as",
        defaultextension=".jpg",
        filetypes=[
            ("JPEG","*.jpeg"),
            ("PNG", "*.png"),
            ("Bitmap","*.bmp")

        ]
    )
        if not filepath:
            return

        cv2.imwrite(filepath,image)
        self.current_file_path=filepath
        messagebox.showinfo(
        "Saved",
        f"Image saved as {os.path.basename(filepath)}"
    )

     
