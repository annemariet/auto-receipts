import os

import pandas as pd
import streamlit as st
from PIL import Image

from constants import *
from data_processing import autocorrect, fill_missing_columns


def load_receipt_ocr_csv(receipt_file):
    if os.path.exists(os.path.join(CSV_DIR, receipt_file)):
        df = pd.read_csv(os.path.join(CSV_DIR, receipt_file), index_col=0)
        st.write("Loaded clean file")
    else:
        df = pd.read_csv(os.path.join(OCR_DIR, receipt_file), index_col=0)
        df[BAK_COLUMNS] = df[EDITABLE_COLUMNS].copy()
        st.write("Loaded raw file")

    fill_missing_columns(df, CLASSIFICATION_COLUMNS)
    autocorrect(df)
    return df


def load_image(image_file):
    img = Image.open(image_file)
    return img


def save_output(output_df, receipt_file):
    print(output_df.columns)
    with st.spinner("Saving..."):
        output_df.to_csv(os.path.join(CSV_DIR, receipt_file))
        print(f"saved to {os.path.join(CSV_DIR, receipt_file)} !")
    return True
