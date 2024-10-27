import cv2
import numpy as np
from assets.lego_colors import LEGO_COLORS
from assets.brick_patterns import BRICK_PATTERNS, MOSAIC_STYLES
from collections import defaultdict

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
    pattern_mask = pattern.astype(np.uint8)
    colored_block = np.full_like(block, color, dtype=np.uint8)
    overlay = (pattern_mask * color).astype(np.uint8)
    result = cv2.addWeighted(colored_block, 0.8, overlay, 0.2, 0)
    return result

def get_color_name(color):
    """Get a human-readable name for a LEGO color"""
    color_names = {
        str([244, 244, 244]): "White",
        str([27, 42, 52]): "Black",
        str([187, 0, 0]): "Red",
        str([228, 205, 158]): "Tan",
        str([0, 109, 182]): "Blue",
        str([40, 127, 70]): "Green",
        str([255, 213, 0]): "Yellow",
        str([160, 95, 52]): "Brown",
        str([108, 110, 104]): "Dark Gray",
        str([199, 193, 183]): "Light Gray",
        str([255, 128, 0]): "Orange",
        str([154, 78, 174]): "Purple",
        str([18, 238, 212]): "Teal",
        str([255, 167, 167]): "Pink",
        str([52, 43, 117]): "Dark Blue",
        str([88, 42, 18]): "Dark Brown",
        str([0, 143, 155]): "Cyan",
        str([144, 194, 58]): "Lime"
    }
    return color_names.get(str(color.tolist()), "Unknown")

def convert_to_lego_mosaic(image, brick_size, color_count, pattern_style="Classic Studs", mosaic_style="Standard"):
    """Convert image to LEGO mosaic with specified pattern and style"""
    print(f"Processing image shape: {image.shape}")
    
    # Resize image to fit brick size
    h, w = image.shape[:2]
    new_h = (h // brick_size) * brick_size
    new_w = (w // brick_size) * brick_size
    image = cv2.resize(image, (new_w, new_h))
    print(f"Resized image shape: {image.shape}")
    
    # Convert style mask to proper format
    style_mask = MOSAIC_STYLES[mosaic_style](np.ones_like(image))
    style_mask = style_mask.astype(np.uint8)
    print(f"Style mask unique values: {np.unique(style_mask)}")
    
    # Apply style mask
    if mosaic_style != "Standard":
        image = cv2.bitwise_and(image, style_mask)
    print(f"After style mask application - image unique values: {np.unique(image)}")
    
    # Get LEGO color palette and brick pattern
    palette = get_lego_palette(color_count)
    pattern = BRICK_PATTERNS[pattern_style](brick_size)
    print(f"Pattern shape: {pattern.shape}, unique values: {np.unique(pattern)}")
    
    # Initialize brick counter
    brick_counts = defaultdict(int)
    
    # Create mosaic
    mosaic = np.zeros_like(image)
    for i in range(0, new_h, brick_size):
        for j in range(0, new_w, brick_size):
            block = image[i:i+brick_size, j:j+brick_size]
            if mosaic_style == "Standard" or np.any(style_mask[i:i+brick_size, j:j+brick_size]):
                avg_color = np.mean(block, axis=(0, 1))
                lego_color = find_nearest_color(avg_color, palette)
                
                # Count bricks
                brick_counts[tuple(lego_color)] += 1
                
                # Apply brick pattern
                patterned_block = apply_brick_pattern(
                    block, 
                    lego_color,
                    pattern
                )
                mosaic[i:i+brick_size, j:j+brick_size] = patterned_block
    
    # Convert brick counts to named dictionary
    named_brick_counts = {get_color_name(np.array(color)): count 
                         for color, count in brick_counts.items()}
    
    print(f"Final mosaic shape: {mosaic.shape}, unique values: {np.unique(mosaic)}")
    return mosaic, named_brick_counts
