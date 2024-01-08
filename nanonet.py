import concurrent.futures
import configparser
import json
import os
import pathlib

import pandas as pd
import requests
import streamlit as st

from constants import *


def get_nanonet_key():
    config = configparser.ConfigParser()
    config.read(os.path.join(pathlib.Path().home(), ".nanonet"))
    return config["account"]["apikey"]


def nanonet_ocr(image_file):
    url = "https://app.nanonets.com/api/v2/OCR/Model/9bfbc8d7-b21c-48d9-8e74-41cff355b464/LabelFile/?async=false"

    data = {"file": open(image_file, "rb")}

    response = requests.post(
        url, auth=requests.auth.HTTPBasicAuth(get_nanonet_key(), ""), files=data
    )
    return response.json()["result"]


def extract_as_clean_csv(nanonet_result):
    raw_output = pd.DataFrame(nanonet_result["prediction"])
    processed_output1 = pd.DataFrame(
        columns=raw_output["label"].values, data=[raw_output["ocr_text"].values]
    )
    processed_output = pd.DataFrame(columns=GLOBAL_INFO_COLUMNS)
    for c in GLOBAL_INFO_COLUMNS:
        if c in processed_output1.columns:
            processed_output[c] = processed_output1[c]

    raw_table = pd.DataFrame(raw_output[raw_output.label == "table"].iloc[0].cells)
    processed_table = pd.DataFrame(
        [
            pd.Series(index=row.label, data=row["text"].values, name=i)
            for i, row in raw_table.groupby("row")
        ]
    )
    processed_table[GLOBAL_INFO_COLUMNS] = pd.concat(
        [processed_output for _ in range(len(processed_table))], ignore_index=True
    )

    if "Line_Amount" in processed_table.columns:
        processed_table["Line_Amount"] = processed_table["Line_Amount"].apply(
            lambda x: x.replace("€", "").strip() if isinstance(x, str) else x
        )
    else:
        processed_table["Line_Amount"] = 0.0

    if "Quantity" in processed_table.columns:
        processed_table["Quantity"] = processed_table["Quantity"].fillna(1)
    else:
        processed_table["Quantity"] = 1

    if "Price" in processed_table.columns:
        processed_table["Price"] = processed_table["Price"].apply(
            lambda x: x.replace("/kg", "").replace("/ kg", "").replace("€", "").strip()
            if isinstance(x, str)
            else x
        )
    else:
        processed_table["Price"] = processed_table["Line_Amount"]

    processed_table["original_filename"] = nanonet_result["input"]
    return processed_table


def run_single_image_ocr(image_filename):
    image_path = os.path.join(IMG_DIR, image_filename)
    json_path = os.path.join(OCR_DIR, image_filename.replace(".jpg", ".json"))
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


def run_ocr_and_save(image_filename):
    res = run_single_image_ocr(image_filename)
    ocr_file = os.path.join(OCR_DIR, image_filename.replace(".jpg", ".csv"))
    res.to_csv(ocr_file)
    return ocr_file


def run_multi_image_ocr(image_file_list):
    output_files = []
    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {
            executor.submit(run_ocr_and_save, img_file): img_file
            for img_file in image_file_list
        }
        for future in concurrent.futures.as_completed(future_to_url):
            img_file = future_to_url[future]
            try:
                data = future.result()
                output_files.append(data)
            except Exception as exc:
                print(f"{img_file} generated an exception: {exc}")
            else:
                print(f"{img_file} OCR result saved to {data}")
    return output_files
