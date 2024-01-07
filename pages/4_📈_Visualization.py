import glob
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from constants import CSV_DIR

"# 📈 My spending"
"## Average basket price"

all_receipts = pd.concat(
    [
        pd.read_csv(f, index_col=0, parse_dates=["Date"])
        for f in glob.glob(os.path.join(CSV_DIR, "*.csv"))
    ]
)
global_infos = all_receipts.groupby("original_filename")[
    ["Merchant_Name", "Total_Amount", "Date"]
].first()
global_infos = all_receipts.sort_values(by="Date")

fig = plt.figure(figsize=(10, 4))
g = sns.barplot(global_infos, x="Date", y="Total_Amount", hue="Merchant_Name")
g.set_title("Amount spent per purchase")
fig
