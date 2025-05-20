import streamlit as st
import os
from utils import *

# Directories
data = 'data/'
media = 'media/'

st.title("Talk with Multimodal PDF")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type="pdf",
    accept_multiple_files=False
)

if uploaded_file:
    file_path = os.path.join(data, uploaded_file.name)
    print(f"Uploaded file path: {file_path}")

    upload_pdf(uploaded_file)
    text = parse_pdf(file_path, media)
    chunked = split_pdf_text(text)
    store_pdf_docs(chunked)

    question = st.chat_input()

    if question:
        st.chat_message("user").write(question)
        related_documents = retrieve_docs(question)
        answer = answer_question(question, related_documents)
        st.chat_message("assistant").write(answer)
