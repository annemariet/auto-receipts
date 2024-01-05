import os

import pandas as pd
import streamlit as st

from constants import *
from data_io import load_receipt_ocr_csv, save_output
from nanonet import run_single_image_ocr
from streamlit_components import upload_image, run_ocr_on_image


if "saved" not in st.session_state:
    st.session_state.saved = {}


if "receipt" not in st.session_state:
    st.session_state.receipt = {}

# Streamlit view
st.set_page_config(
    page_title="Edit receipt app",
    page_icon="X",
    layout="wide",
)

st.write(
    """
# Scan new receipt
"""
)


image_filename = upload_image()
receipt_file = run_ocr_on_image(image_filename)

st.write(
    """
# Correct receipt
"""
)


receipt_list = [f for f in os.listdir(OCR_DIR) if f.endswith(".csv")]
if receipt_file is None:
    if "last_run" in st.session_state.receipt:
        receipt_file = st.session_state.receipt["last_run"]
    else:
        st.write(f"Loading from directory.")
        receipt_file = receipt_list[0]

loaded_df = load_receipt_ocr_csv(receipt_file)

first_row = loaded_df.iloc[0]

image_file = os.path.join(IMG_DIR, first_row.original_filename)
global_infos = first_row[GLOBAL_INFO_COLUMNS].copy()
# For some reason, renaming the column makes it non-editable in streamlit
#global_infos.name = "Ticket information"
global_infos = pd.DataFrame(global_infos)

st.write(f"Editing receipt from {receipt_file}, with image {image_file}")

col1, col2 = st.columns(2)

with col1:
    st.image(image_file)

with col2:
    form = st.form(key="my_form")
    form.write(
        "Here you can correct OCR errors. Price is per unity or per kilogram, as defined in Quantity."
    )
    print(global_infos)
    form.write("### Ticket information")
    global_df = form.data_editor(
        global_infos.reset_index(),
        use_container_width=True,
        hide_index=True,
        disabled=["index"]
    )
    form.write("### Items")
    edited_df = form.data_editor(
        loaded_df[EDITABLE_COLUMNS],
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
    )
    submit_button = form.form_submit_button(label="Submit")
    if submit_button:
        final_df = loaded_df.copy()
        final_df[EDITABLE_COLUMNS] = edited_df
        # Convert DF back to Series with a weird trick
        final_df[GLOBAL_INFO_COLUMNS] = global_df.set_index("index").T.iloc[0]
        result = save_output(final_df, receipt_file)
        st.session_state.saved[os.path.join(CSV_DIR, receipt_file)] = result

        if os.path.join(CSV_DIR, receipt_file) in st.session_state.saved:
            form.write(f"New data saved to {os.path.join(CSV_DIR, receipt_file)}")


st.write(
    """
# Add categories, clean descriptions
"""
)
