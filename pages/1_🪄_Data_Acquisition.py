import os

import streamlit as st

from constants import IMG_DIR, OCR_DIR
from image_processing import autorotate
from streamlit_components import (get_image_file_component, run_ocr_on_image,
                                  upload_image)


def get_non_processed_images():
    if len(st.session_state.image_filenames) == 0:
        receipt_list = [f for f in os.listdir(OCR_DIR) if f.endswith(".csv")]
        img_list = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
        st.session_state.image_filenames = [
            img_file
            for img_file in img_list
            if img_file.replace(".jpg", ".csv") not in receipt_list
        ]
        st.write(
            f"{len(st.session_state.image_filenames)} images have been uploaded but not fully processed."
        )


def rotate_90():
    image_path = os.path.join(IMG_DIR, st.session_state.next_image)
    image = autorotate(image_path, 270)


def rotate_270():
    image_path = os.path.join(IMG_DIR, st.session_state.next_image)
    image = autorotate(image_path, 90)


def rotate_images():
    col1, col2, col3 = st.columns([0.05, 0.05, 0.9])
    with col1:
        st.button(
            "↪️",
            key="rotate270",
            on_click=rotate_270,
            use_container_width=True,
        )
    with col2:
        st.button(
            "↩️",
            key="rotate90",
            on_click=rotate_90,
            use_container_width=True,
        )
    image_path = os.path.join(IMG_DIR, st.session_state.next_image)
    image = autorotate(image_path)
    st.image(image)


st.write(
    """
# 🪄 Scan new receipt
"""
)

upload_image()
get_image_file_component()
rotate_images()


get_non_processed_images()
run_ocr_on_image()
