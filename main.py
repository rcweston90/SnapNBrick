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
    # Create a row for title and reset button
    title_col, reset_col = st.columns([5, 1])
    
    with title_col:
        st.title("🧱 LEGO Mosaic Creator")
        st.write("Transform your photos into LEGO brick mosaics!")

    # Initialize session state if not exists
    if 'image' not in st.session_state:
        st.session_state.image = None

    # Show reset button if image is loaded
    with reset_col:
        if st.session_state.image is not None:
            if st.button("Reset"):
                st.session_state.image = None
                st.rerun()

    # Show file uploader only if no image is loaded
    if st.session_state.image is None:
        uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
        if uploaded_file is not None:
            st.session_state.image = Image.open(uploaded_file)
            st.rerun()
    
    # If image is loaded, process and display it
    if st.session_state.image is not None:
        # Create expandable customization section
        with st.expander("⚙️ Customization Options", expanded=True):
            # Two columns for canvas size
            st.subheader("Canvas Size")
            size_col1, size_col2 = st.columns(2)
            
            # Get image dimensions
            img_array = np.array(st.session_state.image)
            img_h, img_w = img_array.shape[:2]
            aspect_ratio = img_w / img_h
            
            with size_col1:
                canvas_width = st.number_input("Canvas Width (bricks)", 
                                          min_value=10, 
                                          max_value=100, 
                                          value=min(50, img_w // 10))
                
            with size_col2:
                suggested_height = int(canvas_width / aspect_ratio)
                canvas_height = st.number_input("Canvas Height (bricks)", 
                                           min_value=10, 
                                           max_value=100, 
                                           value=min(50, suggested_height))

            # Calculate optimal brick size
            brick_size = calculate_brick_size(img_array.shape, canvas_width, canvas_height)
            st.info(f"Calculated brick size: {brick_size}px per brick")
            
            # Style options in two columns
            st.subheader("Style Options")
            opt_col1, opt_col2 = st.columns(2)
            
            with opt_col1:
                color_count = st.slider("Number of Colors", 5, 20, 12)
                pattern_style = "Smooth Tile" if st.checkbox("Use Smooth Tile Pattern", False) else "Classic Studs"
            
            with opt_col2:
                mosaic_style = st.selectbox(
                    "Mosaic Style",
                    list(MOSAIC_STYLES.keys()),
                    index=0
                )
        
        # Display images side by side
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Image")
            st.image(st.session_state.image, use_column_width=True)

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
            
            # Add download button right after the mosaic
            buf = io.BytesIO()
            Image.fromarray(lego_mosaic).save(buf, format="PNG")
            st.download_button(
                label="Download LEGO Mosaic",
                data=buf.getvalue(),
                file_name="lego_mosaic.png",
                mime="image/png"
            )
        
        # Brick count statistics in expandable section
        with st.expander("📊 Brick Count Statistics", expanded=False):
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

if __name__ == "__main__":
    main()
