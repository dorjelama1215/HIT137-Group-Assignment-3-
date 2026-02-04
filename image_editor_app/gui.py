# gui.py

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os

from image_model import ImageModel
from image_processor import ImageProcessor

class ImageEditorApp(tk.Tk):
    """
    Main GUI class. Interacts with ImageModel and ImageProcessor.
    Demonstrates class interaction and Tkinter GUI elements.
    """

    def __init__(self):
        super().__init__()
        self.title("HIT137 Image Editor")
        self.geometry("1000x700")

        self.model = ImageModel()
        self.processor = ImageProcessor()

        self._original_for_sliders = None  # for brightness/contrast reference
        self.tk_image = None               # keep reference to avoid GC

        self._create_menu()
        self._create_widgets()
        self._create_status_bar()

    # ---------- GUI setup ----------

    def _create_menu(self):
        menubar = tk.Menu(self)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_image)
        file_menu.add_command(label="Save", command=self.save_image)
        file_menu.add_command(label="Save As", command=self.save_image_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_exit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        self.config(menu=menubar)

    def _create_widgets(self):
        # Left: image display area (canvas)
        self.canvas = tk.Canvas(self, bg="gray")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right: control panel
        control_frame = tk.Frame(self, width=250)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons for basic operations
        tk.Label(control_frame, text="Operations", font=("Arial", 12, "bold")).pack(pady=10)

        tk.Button(control_frame, text="Grayscale", command=self.apply_grayscale).pack(fill=tk.X, padx=10, pady=2)
        tk.Button(control_frame, text="Blur", command=self.apply_blur).pack(fill=tk.X, padx=10, pady=2)
        tk.Button(control_frame, text="Edge Detection", command=self.apply_edges).pack(fill=tk.X, padx=10, pady=2)

        # Rotation
        tk.Label(control_frame, text="Rotate", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        rot_frame = tk.Frame(control_frame)
        rot_frame.pack(pady=2)
        tk.Button(rot_frame, text="90°", command=lambda: self.apply_rotate(90)).pack(side=tk.LEFT, padx=2)
        tk.Button(rot_frame, text="180°", command=lambda: self.apply_rotate(180)).pack(side=tk.LEFT, padx=2)
        tk.Button(rot_frame, text="270°", command=lambda: self.apply_rotate(270)).pack(side=tk.LEFT, padx=2)

        # Flip
        tk.Label(control_frame, text="Flip", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        flip_frame = tk.Frame(control_frame)
        flip_frame.pack(pady=2)
        tk.Button(flip_frame, text="Horizontal", command=lambda: self.apply_flip("horizontal")).pack(side=tk.LEFT, padx=2)
        tk.Button(flip_frame, text="Vertical", command=lambda: self.apply_flip("vertical")).pack(side=tk.LEFT, padx=2)

        # Resize/scale slider
        tk.Label(control_frame, text="Resize (Scale)", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        self.scale_var = tk.DoubleVar(value=1.0)
        scale_slider = ttk.Scale(
            control_frame,
            from_=0.2,
            to=2.0,
            orient=tk.HORIZONTAL,
            variable=self.scale_var,
            command=self.on_scale_change
        )
        scale_slider.pack(fill=tk.X, padx=10, pady=2)
        tk.Label(control_frame, text="0.2x - 2.0x").pack(pady=(0, 5))

        # Brightness slider
        tk.Label(control_frame, text="Brightness", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        self.brightness_var = tk.IntVar(value=0)
        self.brightness_slider = ttk.Scale(
            control_frame,
            from_=-100,
            to=100,
            orient=tk.HORIZONTAL,
            command=self.on_brightness_contrast_change
        )
        self.brightness_slider.set(0)
        self.brightness_slider.pack(fill=tk.X, padx=10, pady=2)

        # Contrast slider
        tk.Label(control_frame, text="Contrast", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        self.contrast_var = tk.DoubleVar(value=1.0)
        self.contrast_slider = ttk.Scale(
            control_frame,
            from_=0.5,
            to=2.0,
            orient=tk.HORIZONTAL,
            command=self.on_brightness_contrast_change
        )
        self.contrast_slider.set(1.0)
        self.contrast_slider.pack(fill=tk.X, padx=10, pady=2)

    def _create_status_bar(self):
        self.status_var = tk.StringVar(value="No image loaded.")
        status_bar = tk.Label(self, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # ---------- File operations ----------

    def open_image(self):
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp"),
            ("All files", "*.*"),
        ]
        path = filedialog.askopenfilename(title="Open Image", filetypes=filetypes)
        if not path:
            return
        try:
            self.model.load_image(path)
            self._original_for_sliders = self.model.get_image().copy()
            self._reset_sliders()
            self._update_display()
            self._update_status_bar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_image(self):
        try:
            self.model.save_image()
            messagebox.showinfo("Saved", "Image saved successfully.")
            self._update_status_bar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_image_as(self):
        if self.model.get_image() is None:
            messagebox.showwarning("Warning", "No image to save.")
            return
        filetypes = [
            ("JPEG", "*.jpg"),
            ("PNG", "*.png"),
            ("Bitmap", "*.bmp"),
            ("All files", "*.*"),
        ]
        path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=filetypes,
            title="Save Image As"
        )
        if not path:
            return
        try:
            self.model.save_image(path)
            messagebox.showinfo("Saved", "Image saved successfully.")
            self._update_status_bar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_exit(self):
        if messagebox.askokcancel("Exit", "Do you really want to exit?"):
            self.destroy()

    # ---------- Edit operations (undo/redo) ----------

    def undo(self):
        self.model.undo()
        self._original_for_sliders = self.model.get_image().copy() if self.model.get_image() is not None else None
        self._reset_sliders()
        self._update_display()
        self._update_status_bar()

    def redo(self):
        self.model.redo()
        self._original_for_sliders = self.model.get_image().copy() if self.model.get_image() is not None else None
        self._reset_sliders()
        self._update_display()
        self._update_status_bar()

    # ---------- Image processing actions ----------

    def _ensure_image_loaded(self):
        if self.model.get_image() is None:
            messagebox.showwarning("Warning", "Please open an image first.")
            return False
        return True

    def apply_grayscale(self):
        if not self._ensure_image_loaded():
            return
        img = self.model.get_image()
        new_img = self.processor.to_grayscale(img)
        self.model.apply_change(new_img)
        self._original_for_sliders = self.model.get_image().copy()
        self._reset_sliders()
        self._update_display()
        self._update_status_bar()

    def apply_blur(self):
        if not self._ensure_image_loaded():
            return
        img = self.model.get_image()
        new_img = self.processor.blur(img, ksize=7)
        self.model.apply_change(new_img)
        self._original_for_sliders = self.model.get_image().copy()
        self._reset_sliders()
        self._update_display()
        self._update_status_bar()

    def apply_edges(self):
        if not self._ensure_image_loaded():
            return
        img = self.model.get_image()
        new_img = self.processor.edges(img, 100, 200)
        self.model.apply_change(new_img)
        self._original_for_sliders = self.model.get_image().copy()
        self._reset_sliders()
        self._update_display()
        self._update_status_bar()

    def apply_rotate(self, angle):
        if not self._ensure_image_loaded():
            return
        img = self.model.get_image()
        new_img = self.processor.rotate(img, angle)
        self.model.apply_change(new_img)
        self._original_for_sliders = self.model.get_image().copy()
        self._reset_sliders()
        self._update_display()
        self._update_status_bar()

    def apply_flip(self, mode):
        if not self._ensure_image_loaded():
            return
        img = self.model.get_image()
        new_img = self.processor.flip(img, mode)
        self.model.apply_change(new_img)
        self._original_for_sliders = self.model.get_image().copy()
        self._reset_sliders()
        self._update_display()
        self._update_status_bar()

    # ---------- Sliders: resize, brightness, contrast ----------

    def on_scale_change(self, event=None):
        if not self._ensure_image_loaded():
            return
        img = self.model.get_image()
        scale = self.scale_var.get()
        new_img = self.processor.resize(img, scale=scale)
        # Do NOT push to undo stack on every slider move; just update view
        self._display_image(new_img)
        self._update_status_bar(temp_image=new_img)

    def on_brightness_contrast_change(self, event=None):
        if self._original_for_sliders is None:
            if not self._ensure_image_loaded():
                return
            self._original_for_sliders = self.model.get_image().copy()

        b = float(self.brightness_slider.get())
        c = float(self.contrast_slider.get())
        new_img = self.processor.adjust_brightness_contrast(
            self._original_for_sliders, brightness=b, contrast=c
        )
        # Only preview; not committed to undo/redo until user clicks 'Apply' if you add such button.
        self._display_image(new_img)
        self._update_status_bar(temp_image=new_img)

    def _reset_sliders(self):
        self.scale_var.set(1.0)
        self.brightness_slider.set(0)
        self.contrast_slider.set(1.0)

    # ---------- Display helpers ----------

    def _display_image(self, image):
        # Convert BGR (OpenCV) to RGB for Tkinter
        rgb_image = image[:, :, ::-1]
        pil_image = Image.fromarray(rgb_image)

        # Fit to canvas while keeping aspect ratio
        canvas_w = self.canvas.winfo_width() or 800
        canvas_h = self.canvas.winfo_height() or 600
        pil_image.thumbnail((canvas_w, canvas_h))

        self.tk_image = ImageTk.PhotoImage(pil_image)
        self.canvas.delete("all")
        self.canvas.create_image(canvas_w // 2, canvas_h // 2, image=self.tk_image)

    def _update_display(self):
        img = self.model.get_image()
        if img is not None:
            self._display_image(img)

    def _update_status_bar(self, temp_image=None):
        img = temp_image if temp_image is not None else self.model.get_image()
        if img is None:
            self.status_var.set("No image loaded.")
            return

        h, w = img.shape[:2]
        filename = self.model.get_filename()
        name_only = os.path.basename(filename) if filename else "Unsaved image"
        self.status_var.set(f"{name_only} - {w}x{h}px")
