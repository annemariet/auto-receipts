import streamlit as st
import os

from constants import IMG_DIR, OCR_DIR
from data_io import load_image


def upload_image():
    uploaded_file = st.file_uploader("Choose a receipt image", type=["jpg"])
    image_filename = None
    if uploaded_file is not None:
        image_filename = uploaded_file.name
        save_path = os.path.join(IMG_DIR, image_filename)
        if os.path.exists(save_path):
            st.text("Already uploaded.")
        else:
            # Couldn't find a better way to save the uploaded_file
            load_image(uploaded_file).save(save_path)
        image_file = save_path
        # Show a small view of the image
        st.image(load_image(uploaded_file), width=250)
    return image_filename


def run_ocr_on_image(image_filename):
    receipt_file = None
    if not image_filename:
        return receipt_file

    submit_nanonet = st.button(label="Extract data as csv")

    if submit_nanonet:
        ocr_file = os.path.join(OCR_DIR, image_filename.replace(".jpg", ".csv"))
        if os.path.exists(ocr_file):
            st.write("File already analyzed")
        else:
            with st.spinner("Analyzing image..."):
                res = run_single_image_ocr(image_filename)
                res.to_csv(ocr_file)
                st.session_state.saved[ocr_file] = res
        receipt_file = image_filename.replace(".jpg", ".csv")

        if os.path.join(OCR_DIR, receipt_file) in st.session_state.saved:
            st.write(f"OCR results saved. Loading for correction.")
        st.session_state.receipt["last_run"] = receipt_file
    return receipt_file
