import os

import pandas as pd
import streamlit as st

from constants import *
from data_io import load_receipt_ocr_csv, save_output
from streamlit_components import get_receipt_file_component

st.write(
    """
# ✍️ Add categories, clean descriptions
"""
)

receipt_file = get_receipt_file_component()
loaded_descriptions = load_receipt_ocr_csv(receipt_file)


form2 = st.form(key="my_form2")
edited_df = form2.data_editor(
    loaded_descriptions[["Description"] + CLASSIFICATION_COLUMNS],
    use_container_width=True,
    hide_index=True,
    disabled="Description",
)
submit_button2 = form2.form_submit_button(label="Save")
if submit_button2:
    final_df = loaded_descriptions.copy()
    final_df[CLASSIFICATION_COLUMNS] = edited_df[CLASSIFICATION_COLUMNS]
    result = save_output(final_df, receipt_file)
    st.session_state.saved[os.path.join(CSV_DIR, receipt_file)] = result

    if os.path.join(CSV_DIR, receipt_file) in st.session_state.saved:
        form2.write(f"New data saved to {os.path.join(CSV_DIR, receipt_file)}")
