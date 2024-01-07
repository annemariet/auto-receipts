
import os

import pandas as pd
import streamlit as st

from constants import *
from data_io import load_receipt_ocr_csv, save_output


st.write(
    """
# ✍️ Add categories, clean descriptions
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

loaded_descriptions = load_receipt_ocr_csv(receipt_file)
if any(col  not in loaded_descriptions for col in CLASSIFICATION_COLUMNS):
    loaded_descriptions[CLASSIFICATION_COLUMNS] = "" 
else:
    loaded_descriptions[CLASSIFICATION_COLUMNS] = loaded_descriptions[CLASSIFICATION_COLUMNS].fillna("").astype(str)


form2 = st.form(key="my_form2")
edited_df = form2.data_editor(
    loaded_descriptions[["Description"] + CLASSIFICATION_COLUMNS],
    use_container_width=True,
    hide_index=True,
    disabled="Description"
)
submit_button2 = form2.form_submit_button(label="Save")
if submit_button2:
    final_df = loaded_descriptions.copy()
    final_df[CLASSIFICATION_COLUMNS] = edited_df[CLASSIFICATION_COLUMNS]
    result = save_output(final_df, receipt_file)
    st.session_state.saved[os.path.join(CSV_DIR, receipt_file)] = result

    if os.path.join(CSV_DIR, receipt_file) in st.session_state.saved:
        form2.write(f"New data saved to {os.path.join(CSV_DIR, receipt_file)}")