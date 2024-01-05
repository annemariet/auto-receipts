import streamlit as st
import pandas as pd
import os
import shutil
import pathlib
import configparser
from PIL import Image
import requests
import json


def load_image(image_file):
	img = Image.open(image_file)
	return img

def get_nanonet_key():
    config = configparser.ConfigParser()
    config.read(os.path.join(pathlib.Path().home(), ".nanonet"))
    return config["account"]["apikey"]

data_dir = "data"
receipts_ocr_dir = os.path.join(data_dir, "receipts", "ocr")
images_dir = os.path.join(data_dir, "receipts", "images")
final_csv_dir = os.path.join(data_dir, "receipts", "csv")

receipt_file = None
image_file = None

def save_output(output_df):
    with st.spinner('Saving...'):
        output_df.to_csv(os.path.join(final_csv_dir, receipt_file))
    return True
    
if 'saved' not in st.session_state:
    st.session_state.saved = {}

copy_columns = ['Price_original', 'Description_original', 'Line_Amount_original', 'Quantity_original']

columns_global =  ['currency', 'Merchant_Name', 'Merchant_Phone', 'Merchant_Address',
    'Total_Amount', 'Tax_Amount', 'Date',]
# disabled_columns = ['Merchant_Address', 'currency', 'Merchant_Name', 'Total_Amount', 'Date', ]
# Allow edits on these columns only
enabled_columns = ['Price', 'Description', 'Line_Amount', 'Quantity']


def load_receipt_ocr_csv(receipt_file):

    if os.path.exists(os.path.join(final_csv_dir, receipt_file)):
        df = pd.read_csv(os.path.join(final_csv_dir, receipt_file), index_col=0)
        df["Quantity"] = df["Quantity"].fillna(1)
    else:
        df = pd.read_csv(os.path.join(receipts_ocr_dir, receipt_file))
        df["Quantity"] = df["Quantity"].fillna(1)
        df["Line_Amount"] = df["Line_Amount"].apply(lambda x: x.replace("€", "").strip()  if isinstance(x, str) else x)
        df["Price"] = df["Price"].apply(lambda x: x.replace("/kg", "").replace("/ kg", "").replace("€", "").strip()  if isinstance(x, str) else x)

        df[copy_columns] = df[enabled_columns].copy()
    return df


def nanonet_ocr(image_file):
    url = 'https://app.nanonets.com/api/v2/OCR/Model/9bfbc8d7-b21c-48d9-8e74-41cff355b464/LabelFile/?async=false'

    data = {'file': open(image_file, 'rb')}

    response = requests.post(url, auth=requests.auth.HTTPBasicAuth(get_nanonet_key(), ''), files=data)
    return response.json()["result"]


def extract_as_clean_csv(nanonet_result):
    raw_output = pd.DataFrame(nanonet_result["prediction"])
    processed_output1 = pd.DataFrame(columns=raw_output["label"].values, data=[raw_output["ocr_text"].values])
    processed_output = pd.DataFrame(columns=columns_global)
    for c in columns_global:
        if c in processed_output1.columns:
            processed_output[c] = processed_output1[c]
    
    raw_table = pd.DataFrame(raw_output[raw_output.label == "table"].iloc[0].cells)
    processed_table = pd.DataFrame([
        pd.Series(index=row.label, data=row["text"].values, name=i) for i, row in raw_table.groupby("row")
    ]
    )
    processed_table[columns_global] = pd.concat([processed_output for _ in range(len(processed_table))], ignore_index=True)

    processed_table["Quantity"] = processed_table["Quantity"].fillna(1)
    processed_table["Line_Amount"] = processed_table["Line_Amount"].apply(lambda x: x.replace("€", "").strip()  if isinstance(x, str) else x)
    processed_table["Price"] = processed_table["Price"].apply(lambda x: x.replace("/kg", "").replace("/ kg", "").replace("€", "").strip()  if isinstance(x, str) else x)
    processed_table["original_filename"] = nanonet_result["input"]
    return processed_table

def run_single_image_ocr(image_filename):
    image_path = os.path.join(images_dir, image_filename)
    json_path = os.path.join(receipts_ocr_dir, image_filename.replace(".jpg", ".json"))
    nanonet_result = None
    if not os.path.exists(json_path):
        st.write("Querying Nanonet")
        nanonet_result = nanonet_ocr((image_path))
        with open(json_path, "w") as f:
            f.write(json.dumps(nanonet_result))
    else:
        st.write("Reading cache")
        with open(json_path, "r") as f:
            nanonet_result = json.loads(f.read())
    assert nanonet_result
    ocr_df = extract_as_clean_csv(nanonet_result[0])
    return ocr_df


# Streamlit view
st.set_page_config(
    page_title="Edit receipt app",
    page_icon="X",
    layout="wide",
)

st.write("""
# Scan new receipt
""")
    
uploaded_file = st.file_uploader("Choose a receipt image", type=["jpg"])
image_filename = None
if uploaded_file is not None:
    image_filename = uploaded_file.name
    save_path = os.path.join(images_dir, image_filename)
    if os.path.exists(save_path):
        st.text("Already uploaded.")
    else:
        load_image(uploaded_file).save(save_path)
    image_file = save_path
    st.image(load_image(uploaded_file),width=250)

ocr_form = st.form(key="nanonet_submit")
submit_nanonet = ocr_form.form_submit_button(label="Extract data as csv")

if submit_nanonet:
    assert image_filename
    ocr_file = os.path.join(receipts_ocr_dir, image_filename.replace(".jpg", ".csv"))
    if os.path.exists(ocr_file):
        st.write("File already analyzed")
    else:
        with st.spinner('Analyzing image...'):
            res = run_single_image_ocr(image_filename)
            res.to_csv(ocr_file)
            st.session_state.saved[ocr_file] = res
    receipt_file = image_filename.replace(".jpg", ".csv")


    if os.path.join(receipts_ocr_dir, receipt_file) in st.session_state.saved:
        st.write(f'OCR results saved. Loading for correction.')


st.write("""
# Correct receipt
""")
    

receipt_list = [f for f in os.listdir(receipts_ocr_dir) if f.endswith(".csv")]
if receipt_file is None:
    st.write(f'Loading from directory.')
    receipt_file = receipt_list[0]

df = load_receipt_ocr_csv(receipt_file)
image_file = os.path.join(images_dir, df.iloc[0].original_filename)

st.write(f"Editing receipt from {receipt_file}, with image {image_file}")

col1, col2 = st.columns(2)

with col1:
    
    st.image(image_file)

with col2:
    form = st.form(key='my_form')
    form.write("Here you can correct OCR errors. Price is per unity or per kilogram, as defined in Quantity.")
    edited_df = form.data_editor(df[enabled_columns], num_rows="dynamic")
    submit_button = form.form_submit_button(label='Submit')
    if submit_button:
        final_df = df.copy()
        final_df[enabled_columns] = edited_df
        result = save_output(final_df)
        st.session_state.saved[os.path.join(final_csv_dir, receipt_file)] = result

    if os.path.join(final_csv_dir, receipt_file) in st.session_state.saved:
        st.write(f'New data saved')