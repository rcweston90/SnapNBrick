from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
import numpy as np
import io

def create_building_instructions(mosaic, brick_size, brick_counts, filename=None):
    """Generate PDF building instructions for the LEGO mosaic"""
    # Calculate grid dimensions
    height, width = mosaic.shape[:2]
    grid_h, grid_w = height // brick_size, width // brick_size
    
    # Create PDF buffer if no filename provided
    if filename is None:
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=landscape(letter))
    else:
        c = canvas.Canvas(filename, pagesize=landscape(letter))
    
    # PDF dimensions
    pdf_w, pdf_h = landscape(letter)
    margin = 50
    available_w = pdf_w - 2 * margin
    available_h = pdf_h - 2 * margin
    
    # Calculate grid cell size
    cell_size = min(available_w / grid_w, available_h / grid_h)
    
    # Start position
    start_x = margin + (available_w - cell_size * grid_w) / 2
    start_y = pdf_h - margin - (available_h - cell_size * grid_h) / 2
    
    # Draw title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, pdf_h - margin/2, "LEGO Mosaic Building Instructions")
    
    # Draw grid
    c.setFont("Helvetica", 8)
    for i in range(grid_h):
        for j in range(grid_w):
            x = start_x + j * cell_size
            y = start_y - (i + 1) * cell_size
            
            # Get color of current brick
            brick_color = mosaic[i*brick_size:(i+1)*brick_size, j*brick_size:(j+1)*brick_size].mean(axis=(0, 1))
            
            # Draw colored rectangle
            c.setFillColorRGB(brick_color[2]/255, brick_color[1]/255, brick_color[0]/255)
            c.rect(x, y, cell_size, cell_size, fill=1)
            
            # Draw grid lines
            c.setStrokeColorRGB(0.7, 0.7, 0.7)
            c.rect(x, y, cell_size, cell_size)
            
            # Add coordinates
            c.setFillColorRGB(0, 0, 0)
            c.drawString(x + 2, y + 2, f"{i+1},{j+1}")
    
    # Add color reference guide
    c.showPage()
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, pdf_h - margin/2, "Color Reference Guide")
    
    # Draw color swatches with counts
    c.setFont("Helvetica", 12)
    y_pos = pdf_h - margin - 40
    x_pos = margin
    
    for color_name, count in brick_counts.items():
        # Find color RGB values from the mosaic
        color_sample = None
        for i in range(0, height, brick_size):
            for j in range(0, width, brick_size):
                block = mosaic[i:i+brick_size, j:j+brick_size]
                avg_color = np.mean(block, axis=(0, 1))
                if color_name in str(avg_color):
                    color_sample = avg_color
                    break
            if color_sample is not None:
                break
        
        if color_sample is not None:
            # Draw color swatch
            c.setFillColorRGB(color_sample[2]/255, color_sample[1]/255, color_sample[0]/255)
            c.rect(x_pos, y_pos, 20, 20, fill=1)
            c.setStrokeColorRGB(0, 0, 0)
            c.rect(x_pos, y_pos, 20, 20)
            
            # Add color name and count
            c.setFillColorRGB(0, 0, 0)
            c.drawString(x_pos + 30, y_pos + 5, f"{color_name}: {count} bricks")
            
            # Update position
            y_pos -= 30
            if y_pos < margin:
                y_pos = pdf_h - margin - 40
                x_pos += 200
    
    c.save()
    
    if filename is None:
        return buffer.getvalue()
