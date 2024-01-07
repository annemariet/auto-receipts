import os

import pandas as pd
import streamlit as st

from constants import *
from data_io import load_receipt_ocr_csv, save_output

def add_n_rows_duplicate(df, n_rows):
    return pd.concat((df, df.sample(n_rows)))

st.write(
    """
# 🧹 Correct receipt
"""
)


receipt_list = [f for f in os.listdir(OCR_DIR) if f.endswith(".csv")]
if st.session_state.receipt["file"] is not None:
    receipt_file = st.session_state.receipt["file"]
    st.session_state.receipt["index"] = receipt_list.index(receipt_file)
else:
    st.write(f"Loading from directory.")
    st.session_state.receipt["index"] = 0
    receipt_file = receipt_list[0]
    st.session_state.receipt["file"] = receipt_file

loaded_df = load_receipt_ocr_csv(receipt_file)
if any(col  not in loaded_df for col in CLASSIFICATION_COLUMNS):
    loaded_df[CLASSIFICATION_COLUMNS] = "" 

first_row = loaded_df.iloc[0]
try:
    image_file = os.path.join(IMG_DIR, first_row.original_filename)
except :
    image_file = os.path.join(IMG_DIR, st.session_state.image_filenames[0])
    loaded_df["original_filename"] = st.session_state.image_filenames[0]
global_infos = first_row[GLOBAL_INFO_COLUMNS].copy()
# For some reason, renaming the column makes it non-editable in streamlit
# global_infos.name = "Ticket information"
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
    form.write("### Ticket information")
    global_df = form.data_editor(
        global_infos.reset_index(),
        use_container_width=True,
        hide_index=True,
        disabled=["index"],
    )
    form.write("### Items")
    edited_items = form.data_editor(
        loaded_df[EDITABLE_COLUMNS],
        num_rows="dynamic",
        use_container_width=True,
    )

    submit_button = form.form_submit_button(label="Save")
    if submit_button:
        final_df = loaded_df.copy()
        # Convert DF back to Series with a weird trick
        final_df[GLOBAL_INFO_COLUMNS] = global_df.set_index("index").T.iloc[0]
        final_df = edited_items.join(final_df[ALL_BUT_EDITABLE_COLUMNS]).ffill()
        result = save_output(final_df, receipt_file)
        st.session_state.saved[os.path.join(CSV_DIR, receipt_file)] = result

        if os.path.join(CSV_DIR, receipt_file) in st.session_state.saved:
            form.write(f"New data saved to {os.path.join(CSV_DIR, receipt_file)}")
