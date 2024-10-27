# 🧱 LEGO Mosaic Creator

Transform your photos into LEGO brick mosaics with this interactive web application! Upload any image and convert it into a detailed LEGO mosaic with customizable patterns, colors, and styles.

## ✨ Features

- **Image Upload**: Support for JPG, JPEG, and PNG formats
- **Real-time Conversion**: Instantly see your image transformed into LEGO bricks
- **Customization Options**:
  - Adjustable canvas size (width × height in bricks)
  - Variable number of LEGO colors (5-20 colors)
  - Two brick patterns: Classic Studs and Smooth Tile
  - Multiple mosaic styles: Standard, Circular, and Diamond
- **Brick Count Estimation**: Get detailed counts of required bricks by color
- **Export Options**:
  - Download the mosaic as a PNG image
  - Generate PDF building instructions with color reference guide

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Required Python packages:
  - streamlit
  - opencv-python (cv2)
  - numpy
  - Pillow (PIL)
  - reportlab

### Installation

1. Clone the repository or download the source code
2. Install the required packages:
```bash
pip install streamlit opencv-python numpy pillow reportlab
```
3. Run the application:
```bash
streamlit run main.py
```

## 💡 Usage Guide

1. **Upload an Image**:
   - Click the "Choose an image..." button
   - Select a JPG, JPEG, or PNG file from your computer

2. **Customize Your Mosaic**:
   - Adjust the canvas size using the width and height inputs
   - Select the number of LEGO colors using the slider
   - Toggle between Classic Studs and Smooth Tile patterns
   - Choose a mosaic style (Standard, Circular, or Diamond)

3. **Export Your Creation**:
   - Download the mosaic as a PNG image
   - Generate PDF building instructions with:
     - Grid-based assembly guide
     - Color reference chart
     - Brick count statistics

## 🎨 Customization Options

### Canvas Size
- Width: 10-100 bricks
- Height: 10-100 bricks
- Automatic brick size calculation based on input image

### Color Selection
- Minimum: 5 colors
- Maximum: 20 colors
- Uses official LEGO color palette

### Brick Patterns
- **Classic Studs**: Traditional LEGO brick appearance with circular studs
- **Smooth Tile**: Clean, flat surface without studs

### Mosaic Styles
- **Standard**: Regular rectangular mosaic
- **Circular**: Circular-shaped mosaic
- **Diamond**: Diamond-shaped mosaic

## 📁 Project Structure

```
.
├── main.py                 # Main application file
├── lego_utils.py          # Core LEGO conversion utilities
├── instruction_generator.py # PDF instruction generation
├── assets/
│   ├── brick_patterns.py  # Brick pattern definitions
│   └── lego_colors.py     # LEGO color definitions
├── styles/
│   └── style.css         # Custom styling
└── .streamlit/
    └── config.toml       # Streamlit configuration
```

## 🔧 Dependencies

- **Core Libraries**:
  - `streamlit`: Web application framework
  - `opencv-python`: Image processing
  - `numpy`: Numerical computations
  - `Pillow`: Image handling
  - `reportlab`: PDF generation

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## 📝 License

This project is open-source and available under the MIT License.
