# HIT137 Image Editor

A feature-rich desktop image editing application built with Python, Tkinter, and OpenCV. This project demonstrates object-oriented programming principles, GUI development, and advanced image processing techniques.

## Features

### Core Image Operations
- **Open & Save Images** - Support for JPG, PNG, BMP formats
- **Undo/Redo** - Full history management for all operations
- **Reset All** - Quickly reset all filters and adjustments

### Filters & Effects
- **Grayscale** - Convert images to grayscale with adjustable intensity
- **Blur** - Apply Gaussian blur with customizable strength
- **Edge Detection** - Canny edge detection with intensity control
- **Background Removal** - Automatic background removal using GrabCut algorithm

### Transform Operations
- **Rotate** - 90°, 180°, and 270° rotation
- **Flip** - Horizontal and vertical flipping
- **Resize** - Scale images from 20% to 200%

### Adjustments
- **Brightness** - Adjust from -100 to +100
- **Contrast** - Adjust from 0.5x to 2.0x
- **Live Preview** - Real-time preview for all slider-based adjustments

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Required Libraries

Install the required dependencies using pip:

```bash
pip install opencv-python
pip install pillow
pip install numpy
```

Or install from a requirements file:

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
opencv-python>=4.5.0
Pillow>=8.0.0
numpy>=1.19.0
```

### For Anaconda Users

If you're using Anaconda, you can also install using conda:

```bash
conda install -c conda-forge opencv
conda install pillow
conda install numpy
```

## Project Structure

```
image_editor_app/
│
├── main.py                 # Entry point of the application
├── gui.py                  # GUI implementation (ImageEditorApp class)
├── image_model.py          # Data model for image management
├── image_processor.py      # Image processing operations
└── README.md              # This file
```

### File Descriptions

- **main.py** - Initializes and runs the application
- **gui.py** - Contains the main GUI class with all UI components and event handlers
- **image_model.py** - Manages image data, file operations, and undo/redo history
- **image_processor.py** - Implements all image processing algorithms using OpenCV

## Usage

### Running the Application

1. Navigate to the project directory:
```bash
cd image_editor_app
```

2. Run the application:
```bash
python main.py
```

### Basic Workflow

1. **Open an Image**
   - Click `File > Open` or use the Open button
   - Select an image file (JPG, PNG, or BMP)

2. **Apply Edits**
   - Use sliders for real-time adjustments
   - Click buttons to apply filters and transformations
   - Use +/- buttons for fine-tuned control

3. **Save Your Work**
   - Click `File > Save` to overwrite the original
   - Click `File > Save As` to save with a new name
   - **Important**: Save as PNG to preserve transparency after background removal

### Tips for Best Results

- **Background Removal**: Works best when the subject is centered and clearly distinct from the background
- **Undo/Redo**: Use `Edit > Undo` or `Edit > Redo` to navigate through your editing history
- **Live Preview**: Sliders show live previews - click "Apply" buttons to commit changes
- **Transparency**: Always save as PNG format after using BG Remover to preserve transparency

## Key Components

### ImageEditorApp (gui.py)
Main GUI class that handles:
- User interface creation
- Event handling
- Display updates
- Interaction with ImageModel and ImageProcessor

### ImageModel (image_model.py)
Data model that manages:
- Current and original image storage
- Undo/redo stack implementation
- File I/O operations
- Image state management

### ImageProcessor (image_processor.py)
Processing engine that provides:
- Grayscale conversion
- Gaussian blur
- Edge detection (Canny)
- Background removal (GrabCut)
- Rotation and flipping
- Brightness/contrast adjustment
- Image resizing

## Technical Details

### Image Processing Algorithms

- **Grayscale**: Uses weighted color channel conversion
- **Blur**: Gaussian blur with adjustable kernel size
- **Edge Detection**: Canny algorithm with dual thresholds
- **Background Removal**: GrabCut iterative segmentation algorithm
- **Brightness/Contrast**: Linear transformation with clipping

### Design Patterns

- **Model-View-Controller (MVC)**: Separation of data, UI, and processing logic
- **Encapsulation**: Private attributes with public getter methods
- **Command Pattern**: Undo/redo implementation using stack-based history

## Troubleshooting

### Common Issues

**Problem**: `ModuleNotFoundError: No module named 'PIL'`
```bash
# Solution:
pip install Pillow
```

**Problem**: `ModuleNotFoundError: No module named 'cv2'`
```bash
# Solution:
pip install opencv-python
```

**Problem**: Background removal doesn't work well
- Ensure the subject is roughly centered in the image
- Try images with clear foreground/background separation
- Avoid images with complex or cluttered backgrounds

**Problem**: Saved image loses transparency
- Make sure to save as PNG format (not JPG)
- JPG doesn't support transparency - use PNG instead

## System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: 3.7 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Display**: 1024x768 minimum resolution

## Future Enhancements

Potential features for future versions:
- Additional filters (sepia, vintage, etc.)
- Drawing tools (brush, shapes, text)
- Batch processing
- Advanced background removal with AI models
- Layer support
- Image enhancement (sharpen, denoise)

## Credits

Developed as part of HIT137 Assignment 3
- **Framework**: Tkinter (Python standard library)
- **Image Processing**: OpenCV
- **Image Display**: Pillow (PIL)

## License

This project is developed for educational purposes as part of the HIT137 course assignment.

## Support

For issues, questions, or contributions:
1. Check the troubleshooting section
2. Review the code comments for implementation details
3. Consult OpenCV and Tkinter documentation

---

**Version**: 1.0  
**Last Updated**: February 2026