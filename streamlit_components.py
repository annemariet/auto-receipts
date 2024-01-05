import streamlit as st
import os

from constants import IMG_DIR, OCR_DIR
from data_io import load_image


def validate_and_show_image(uploaded_file, col):
    image_filename = uploaded_file.name
    save_path = os.path.join(IMG_DIR, image_filename)
    with col:
        if os.path.exists(save_path):
            st.text("Already uploaded.")
        else:
            # Couldn't find a better way to save the uploaded_file
            load_image(uploaded_file).save(save_path)
        # Show a small view of the image
        st.image(load_image(uploaded_file), width=250)
    return image_filename


def upload_image():
    uploaded_files = st.file_uploader("Choose a receipt image", type=["jpg"], accept_multiple_files=True)
    image_filenames = []
    if uploaded_files is not None:
        columns = st.columns(len(uploaded_files))
        image_filenames = [validate_and_show_image(uploaded_file, col) for uploaded_file, col in zip(uploaded_files, columns)]
    return image_filenames


def run_ocr_on_image(image_filenames):
    receipt_file = None
    if len(image_filenames) == 0:
        return receipt_file

    submit_nanonet = st.button(label="Extract data as csv")

    if submit_nanonet:
        files_to_submit = []
        files_exist = []
        for image_filename in image_filenames:
            ocr_file = os.path.join(OCR_DIR, image_filename.replace(".jpg", ".csv"))
            if os.path.exists(ocr_file):
                st.write("File already analyzed")
                files_exist.append(image_filename)
            else:
                files_to_submit.append(image_filename)

        if len(files_exist) > 0:
            image_filename = files_exist[0]
        else:
            image_filename = files_to_submit[0]
            with st.spinner(f"Analyzing image {image_filename}"):
                res = run_single_image_ocr(image_filename)
                ocr_file = os.path.join(OCR_DIR, image_filename.replace(".jpg", ".csv"))
                res.to_csv(ocr_file)
                st.session_state.saved[ocr_file] = res
        receipt_file = image_filename.replace(".jpg", ".csv")

        if os.path.join(OCR_DIR, receipt_file) in st.session_state.saved:
            st.write(f"OCR results saved. Loading for correction.")
        st.session_state.receipt["last_run"] = receipt_file
    return receipt_file
