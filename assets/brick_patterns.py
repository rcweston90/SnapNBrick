import numpy as np
import cv2

def create_stud_pattern(brick_size):
    """Create a classic LEGO stud pattern"""
    pattern = np.ones((brick_size, brick_size, 3), dtype=np.uint8)
    stud_radius = int(brick_size * 0.2)
    center = (brick_size // 2, brick_size // 2)
    
    # Create circular stud with proper values
    cv2.circle(pattern, center, stud_radius, (0.2, 0.2, 0.2), -1)
    cv2.circle(pattern, center, stud_radius, (0.3, 0.3, 0.3), 1)
    
    return pattern

def create_smooth_pattern(brick_size):
    """Create a smooth tile pattern"""
    pattern = np.ones((brick_size, brick_size, 3), dtype=np.uint8)
    cv2.rectangle(pattern, (1, 1), (brick_size-2, brick_size-2), (0.2, 0.2, 0.2), 1)
    return pattern

BRICK_PATTERNS = {
    "Classic Studs": create_stud_pattern,
    "Smooth Tile": create_smooth_pattern
}

# Update mosaic styles to use proper mask values
MOSAIC_STYLES = {
    "Standard": lambda x: x,
    "Circular": lambda x: cv2.circle(
        np.ones_like(x),
        (x.shape[1]//2, x.shape[0]//2),
        min(x.shape[0], x.shape[1])//2,
        (1, 1, 1),
        -1
    ),
    "Diamond": lambda x: cv2.rectangle(
        np.ones_like(x),
        (x.shape[1]//4, x.shape[0]//4),
        (3*x.shape[1]//4, 3*x.shape[0]//4),
        (1, 1, 1),
        -1
    )
}
