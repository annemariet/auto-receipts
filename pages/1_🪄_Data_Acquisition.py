import os
import streamlit as st

from streamlit_components import run_ocr_on_image, upload_image
from constants import IMG_DIR, OCR_DIR

def get_non_processed_images():
    if len(st.session_state.image_filenames) == 0:
        receipt_list = [f for f in os.listdir(OCR_DIR) if f.endswith(".csv")]
        img_list = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
        st.session_state.image_filenames = [img_file for img_file in img_list if img_file.replace(".jpg", ".csv") not in receipt_list]
        st.write(f"{len(st.session_state.image_filenames)} images have been uploaded but not fully processed.")

st.write(
    """
# 🪄 Scan new receipt
"""
)

upload_image()

get_non_processed_images()
run_ocr_on_image()
