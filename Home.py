import os

import pandas as pd
import streamlit as st

from constants import *
from data_io import load_receipt_ocr_csv, save_output
from nanonet import run_single_image_ocr
from streamlit_components import run_ocr_on_image, upload_image


# Streamlit view
st.set_page_config(
    page_title="Edit receipt app",
    page_icon="X",
    layout="wide",
)

"# 🧾This is your new accounting home!"

"""
 - 🪄 Go to Data Acquisition to Scan receipts
 - 🧹 Fix OCR errors in Data Cleaning
 - ✍️ Add Categories and other data in Data Enrichment
 - 📈 Explore your spending in Visualization
"""

if "saved" not in st.session_state:
    st.session_state.saved = {}


if "receipt" not in st.session_state:
    st.session_state.receipt = {
        "file": None,
        "index": None
    }

if "image_filenames" not in st.session_state:
    st.session_state.image_filenames = {}
    

