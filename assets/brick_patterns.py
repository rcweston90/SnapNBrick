import numpy as np
import cv2

def create_stud_pattern(brick_size):
    """Create a classic LEGO stud pattern"""
    pattern = np.ones((brick_size, brick_size, 3), dtype=np.uint8)
    stud_radius = int(brick_size * 0.2)
    center = (brick_size // 2, brick_size // 2)
    
    # Create circular stud
    cv2.circle(pattern, center, stud_radius, (0.9, 0.9, 0.9), -1)
    cv2.circle(pattern, center, stud_radius, (0.8, 0.8, 0.8), 1)
    
    return pattern

def create_smooth_pattern(brick_size):
    """Create a smooth tile pattern"""
    pattern = np.ones((brick_size, brick_size, 3), dtype=np.uint8)
    cv2.rectangle(pattern, (1, 1), (brick_size-2, brick_size-2), (0.95, 0.95, 0.95), 1)
    return pattern

def create_diagonal_pattern(brick_size):
    """Create a diagonal striped pattern"""
    pattern = np.ones((brick_size, brick_size, 3), dtype=np.uint8)
    for i in range(-brick_size, brick_size*2, 4):
        cv2.line(pattern, (i, 0), (i+brick_size, brick_size), (0.9, 0.9, 0.9), 1)
    return pattern

BRICK_PATTERNS = {
    "Classic Studs": create_stud_pattern,
    "Smooth Tile": create_smooth_pattern,
    "Diagonal": create_diagonal_pattern
}

MOSAIC_STYLES = {
    "Standard": lambda x: x,
    "Circular": lambda x: cv2.circle(x.copy(), (x.shape[1]//2, x.shape[0]//2), 
                                   min(x.shape[0], x.shape[1])//2, (255, 255, 255), -1),
    "Diamond": lambda x: cv2.rectangle(x.copy(), 
                                     (x.shape[1]//4, x.shape[0]//4),
                                     (3*x.shape[1]//4, 3*x.shape[0]//4),
                                     (255, 255, 255), -1)
}
