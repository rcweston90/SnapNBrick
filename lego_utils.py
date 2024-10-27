import cv2
import numpy as np
from assets.lego_colors import LEGO_COLORS

def get_lego_palette(n_colors):
    """Convert LEGO_COLORS to numpy array and return n_colors samples"""
    colors = np.array([color for color in LEGO_COLORS])
    if len(colors) > n_colors:
        indices = np.linspace(0, len(colors)-1, n_colors, dtype=int)
        return colors[indices]
    return colors

def find_nearest_color(pixel, palette):
    """Find the nearest LEGO color for a given pixel"""
    distances = np.sqrt(np.sum((palette - pixel) ** 2, axis=1))
    return palette[np.argmin(distances)]

def convert_to_lego_mosaic(image, brick_size, color_count):
    """Convert image to LEGO mosaic"""
    # Resize image to fit brick size
    h, w = image.shape[:2]
    new_h = (h // brick_size) * brick_size
    new_w = (w // brick_size) * brick_size
    image = cv2.resize(image, (new_w, new_h))
    
    # Get LEGO color palette
    palette = get_lego_palette(color_count)
    
    # Create mosaic
    mosaic = np.zeros_like(image)
    for i in range(0, new_h, brick_size):
        for j in range(0, new_w, brick_size):
            block = image[i:i+brick_size, j:j+brick_size]
            avg_color = np.mean(block, axis=(0, 1))
            lego_color = find_nearest_color(avg_color, palette)
            mosaic[i:i+brick_size, j:j+brick_size] = lego_color
            
            # Add brick effect
            cv2.rectangle(
                mosaic,
                (j, i),
                (j+brick_size-1, i+brick_size-1),
                lego_color.tolist(),
                1
            )
    
    return mosaic
