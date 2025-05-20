# app.py

import streamlit as st
import os
from chatbot.chatbot_engine import (
    parse_pdf, split_pdf_text, store_pdf_docs,
    retrieve_docs, answer_question
)

# --- Mapper ---
data = 'data/'
media = 'media/'
os.makedirs(data, exist_ok=True)
os.makedirs(media, exist_ok=True)

# --- Titel ---
st.title("📄 Talk with Multimodal PDF")

# --- Upload ---
uploaded_file = st.file_uploader("Upload PDF", type="pdf", accept_multiple_files=False)

if uploaded_file:
    file_path = os.path.join(data, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ {uploaded_file.name} uploadet")

    with st.spinner("🔍 Læser og analyserer PDF..."):
        text = parse_pdf(file_path, media)
        chunks = split_pdf_text(text)
        store_pdf_docs(chunks)

# --- Chat ---
st.markdown("---")
st.subheader("💬 Stil dit spørgsmål til dokumentet")
question = st.chat_input("Your message")

if question:
    st.chat_message("user").write(question)
    with st.spinner("✍️ Finder svar..."):
        related_documents = retrieve_docs(question)
        answer = answer_question(question, related_documents)
    st.chat_message("assistant").write(answer)
