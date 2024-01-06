
import streamlit as st

from streamlit_components import run_ocr_on_image, upload_image


st.write(
    """
# 🪄 Scan new receipt
"""
)

upload_image()

run_ocr_on_image()
