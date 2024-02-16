# auto-receipts
A Streamlit app to scan and analyze my receipts.
⚠️ _Work in progress_.

Developed while trying out the new [Lightning AI studio](https://lightning.ai).

I use the [Nanonets API](https://app.nanonets.com/documentation#operation/OCRModelLabelFileByModelIdPost) to run OCR on receipt pictures. To use it, put it in an environment variable called `nanonet-apikey`. In Lightning AI studio you can use it by adding it in your [secrets](https://lightning.ai/docs/app/stable/glossary/secrets.html).

This is work in progress, so I haven't tested in another environment. The `requirements.txt` file should give the most important ones.