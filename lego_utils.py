import cv2
import numpy as np
from assets.lego_colors import LEGO_COLORS
from assets.brick_patterns import BRICK_PATTERNS, MOSAIC_STYLES

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

def apply_brick_pattern(block, color, pattern):
    """Apply the selected brick pattern to a block"""
    pattern_mask = pattern.astype(float)
    colored_block = np.full_like(block, color)
    return (colored_block * pattern_mask).astype(np.uint8)

def convert_to_lego_mosaic(image, brick_size, color_count, pattern_style="Classic Studs", mosaic_style="Standard"):
    """Convert image to LEGO mosaic with specified pattern and style"""
    # Resize image to fit brick size
    h, w = image.shape[:2]
    new_h = (h // brick_size) * brick_size
    new_w = (w // brick_size) * brick_size
    image = cv2.resize(image, (new_w, new_h))
    
    # Apply mosaic style mask
    style_mask = MOSAIC_STYLES[mosaic_style](np.ones_like(image))
    image = cv2.bitwise_and(image, style_mask)
    
    # Get LEGO color palette and brick pattern
    palette = get_lego_palette(color_count)
    pattern = BRICK_PATTERNS[pattern_style](brick_size)
    
    # Create mosaic
    mosaic = np.zeros_like(image)
    for i in range(0, new_h, brick_size):
        for j in range(0, new_w, brick_size):
            block = image[i:i+brick_size, j:j+brick_size]
            if np.any(style_mask[i:i+brick_size, j:j+brick_size]):
                avg_color = np.mean(block, axis=(0, 1))
                lego_color = find_nearest_color(avg_color, palette)
                
                # Apply brick pattern
                patterned_block = apply_brick_pattern(
                    block, 
                    lego_color,
                    pattern
                )
                mosaic[i:i+brick_size, j:j+brick_size] = patterned_block
    
    return mosaic
