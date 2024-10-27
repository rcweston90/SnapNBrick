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

def main():
    st.title("🧱 LEGO Mosaic Creator")
    st.write("Transform your photos into LEGO brick mosaics!")

    # Sidebar controls
    st.sidebar.header("Customization Options")
    brick_size = st.sidebar.slider("Brick Size (pixels)", 10, 50, 30)
    color_count = st.sidebar.slider("Number of Colors", 5, 20, 12)
    
    # New pattern and style selectors
    pattern_style = st.sidebar.selectbox(
        "Brick Pattern",
        list(BRICK_PATTERNS.keys()),
        index=0
    )
    
    mosaic_style = st.sidebar.selectbox(
        "Mosaic Style",
        list(MOSAIC_STYLES.keys()),
        index=0
    )
    
    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file is not None:
        # Load and display original image
        image = Image.open(uploaded_file)
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Image")
            st.image(image, use_column_width=True)
        
        # Convert image to LEGO mosaic
        img_array = np.array(image)
        lego_mosaic = convert_to_lego_mosaic(
            img_array, 
            brick_size, 
            color_count,
            pattern_style,
            mosaic_style
        )
        
        with col2:
            st.subheader("LEGO Mosaic")
            st.image(lego_mosaic, use_column_width=True)
        
        # Download button
        if st.button("Download LEGO Mosaic"):
            buf = io.BytesIO()
            Image.fromarray(lego_mosaic).save(buf, format="PNG")
            btn = st.download_button(
                label="Click to Download",
                data=buf.getvalue(),
                file_name="lego_mosaic.png",
                mime="image/png"
            )

if __name__ == "__main__":
    main()
