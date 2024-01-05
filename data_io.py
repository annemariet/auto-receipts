import os

import pandas as pd
from PIL import Image
import streamlit as st

from constants import *


def load_receipt_ocr_csv(receipt_file):
    if os.path.exists(os.path.join(CSV_DIR, receipt_file)):
        df = pd.read_csv(os.path.join(CSV_DIR, receipt_file), index_col=0)
    else:
        df = pd.read_csv(os.path.join(OCR_DIR, receipt_file), index_col=0)
        df[BAK_COLUMNS] = df[EDITABLE_COLUMNS].copy()
    return df


def load_image(image_file):
    img = Image.open(image_file)
    return img


def save_output(output_df, receipt_file):
    with st.spinner("Saving..."):
        output_df.to_csv(os.path.join(CSV_DIR, receipt_file))
        print(f"saved to {os.path.join(CSV_DIR, receipt_file)} !")
    return True
