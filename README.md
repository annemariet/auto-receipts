# auto-receipts
A Streamlit app to scan and analyze my receipts.
⚠️ _Work in progress_.

Developed while trying out the new [Lightning AI studio](https://lightning.ai).

I use the [Nanonets API](https://app.nanonets.com/documentation#operation/OCRModelLabelFileByModelIdPost) to run OCR on receipt pictures. To use it, you'll need to create Nanonet account. Then you can add a `.nanonet` file in your home directory with:
```
[account]
    apikey=<PASTE YOU API KEY HERE>
```

This is work in progress, so I haven't tested in another environment. The `requirements.txt` file should give the most important ones.