import os

DATA_DIR = "data"
OCR_DIR = os.path.join(DATA_DIR, "receipts", "ocr")
IMG_DIR = os.path.join(DATA_DIR, "receipts", "images")
CSV_DIR = os.path.join(DATA_DIR, "receipts", "csv")


BAK_COLUMNS = [
    "Price_original",
    "Description_original",
    "Line_Amount_original",
    "Quantity_original",
]

GLOBAL_INFO_COLUMNS = [
    "currency",
    "Merchant_Name",
    "Merchant_Phone",
    "Merchant_Address",
    "Total_Amount",
    "Tax_Amount",
    "Date",
]

EDITABLE_COLUMNS = ["Price", "Description", "Line_Amount", "Quantity"]
CLASSIFICATION_COLUMNS = [
    "Quantity of unit",
    "Unit of quantity",
    "Simplified Description",
    "Category 1",
    "Category 2",
]

ALL_BUT_EDITABLE_COLUMNS = (
    GLOBAL_INFO_COLUMNS + CLASSIFICATION_COLUMNS + ["original_filename"]
)
