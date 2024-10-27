import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
from lego_utils import (
    convert_to_lego_mosaic,
    get_lego_palette
)
from assets.brick_patterns import BRICK_PATTERNS, MOSAIC_STYLES
from instruction_generator import create_building_instructions

# Page configuration
st.set_page_config(
    page_title="LEGO Mosaic Creator",
    page_icon="🧱",
    layout="wide"
)

# Load custom CSS
with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def calculate_brick_size(image_shape, canvas_width, canvas_height):
    """Calculate optimal brick size maintaining aspect ratio"""
    img_h, img_w = image_shape[:2]
    img_aspect = img_w / img_h
    canvas_aspect = canvas_width / canvas_height
    
    if img_aspect > canvas_aspect:
        # Image is wider relative to canvas
        brick_size = img_w // canvas_width
    else:
        # Image is taller relative to canvas
        brick_size = img_h // canvas_height
        
    return max(10, brick_size)  # Ensure minimum brick size of 10 pixels

def main():
    st.title("🧱 LEGO Mosaic Creator")
    st.write("Transform your photos into LEGO brick mosaics!")

    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file is not None:
        # Load and display original image
        image = Image.open(uploaded_file)
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Image")
            st.image(image, use_column_width=True)

        # Canvas Size and Customization Options Section
        st.subheader("Canvas Size")
        col_size1, col_size2 = st.columns(2)
        
        # Get image dimensions
        img_array = np.array(image)
        img_h, img_w = img_array.shape[:2]
        aspect_ratio = img_w / img_h
        
        with col_size1:
            canvas_width = st.number_input("Canvas Width (bricks)", 
                                         min_value=10, 
                                         max_value=100, 
                                         value=min(50, img_w // 10))
            
        with col_size2:
            suggested_height = int(canvas_width / aspect_ratio)
            canvas_height = st.number_input("Canvas Height (bricks)", 
                                          min_value=10, 
                                          max_value=100, 
                                          value=min(50, suggested_height))

        # Calculate optimal brick size
        brick_size = calculate_brick_size(img_array.shape, canvas_width, canvas_height)
        
        st.info(f"Calculated brick size: {brick_size}px per brick")
        
        # Additional Customization Options
        st.subheader("Customization Options")
        col_opt1, col_opt2 = st.columns(2)
        
        with col_opt1:
            color_count = st.slider("Number of Colors", 5, 20, 12)
            pattern_style = st.selectbox(
                "Brick Pattern",
                list(BRICK_PATTERNS.keys()),
                index=0
            )
        
        with col_opt2:
            mosaic_style = st.selectbox(
                "Mosaic Style",
                list(MOSAIC_STYLES.keys()),
                index=0
            )
        
        # Convert image to LEGO mosaic
        lego_mosaic, brick_counts = convert_to_lego_mosaic(
            img_array, 
            brick_size, 
            color_count,
            pattern_style,
            mosaic_style
        )
        
        with col2:
            st.subheader("LEGO Mosaic")
            st.image(lego_mosaic, use_column_width=True)
            
            # Display grid information
            actual_cols = lego_mosaic.shape[1] // brick_size
            actual_rows = lego_mosaic.shape[0] // brick_size
            st.info(f"Final Grid Size: {actual_rows} rows × {actual_cols} columns")
        
        # Display brick counts
        st.subheader("Brick Count Estimation")
        col3, col4 = st.columns(2)
        
        with col3:
            st.write("Number of bricks needed for each color:")
            for color, count in brick_counts.items():
                st.write(f"- {color}: {count} bricks")
        
        with col4:
            total_bricks = sum(brick_counts.values())
            st.write("Total Statistics:")
            st.write(f"- Total bricks needed: {total_bricks}")
            st.write(f"- Mosaic dimensions: {actual_cols} × {actual_rows} bricks")
        
        # Export options
        st.subheader("Export Options")
        col5, col6 = st.columns(2)
        
        with col5:
            if st.button("Download LEGO Mosaic Image"):
                buf = io.BytesIO()
                Image.fromarray(lego_mosaic).save(buf, format="PNG")
                st.download_button(
                    label="Click to Download Image",
                    data=buf.getvalue(),
                    file_name="lego_mosaic.png",
                    mime="image/png"
                )
        
        with col6:
            if st.button("Download Building Instructions"):
                # Generate PDF instructions
                pdf_data = create_building_instructions(lego_mosaic, brick_size, brick_counts)
                st.download_button(
                    label="Click to Download Instructions",
                    data=pdf_data,
                    file_name="lego_instructions.pdf",
                    mime="application/pdf"
                )

if __name__ == "__main__":
    main()
