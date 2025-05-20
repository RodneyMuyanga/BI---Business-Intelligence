import os
import streamlit as st

# Imports
from langchain_community.document_loaders import SeleniumURLLoader
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.utils.constants import PartitionStrategy

from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore

# Directories
data = './data/'
media = './media/'

# Models — adjusted to your versions
embeddings = OllamaEmbeddings(model="llama3:8b")
vector_store = InMemoryVectorStore(embeddings)
llm = OllamaLLM(model="gemma3:12b")

# Prompt template
template = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer:
"""

# Load web page
def load_web_page(url):
    loader = SeleniumURLLoader(urls=[url])
    documents = loader.load()
    return documents

# Split web page text into chunks
def split_web_text(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    data = text_splitter.split_documents(docs)
    return data

# Save uploaded PDF file
def upload_pdf(file):
    os.makedirs(data, exist_ok=True)
    with open(os.path.join(data, file.name), "wb") as f:
        f.write(file.getbuffer())

# Extract text from image using LLM bound with images
def text_from_image(file_path):
    print(f"Processing image: {file_path}")
    model_with_image_context = llm.bind(images=[file_path])
    return model_with_image_context.invoke("Tell me what do you see in this picture.")

# Parse PDF content and extract text + text from images
def parse_pdf(file_path, media_path):
    os.makedirs(media_path, exist_ok=True)
    elements = partition_pdf(
        file_path,
        strategy=PartitionStrategy.HI_RES,
        extract_image_block_types=["Image", "Table"],
        extract_image_block_output_dir=media_path,
    )

    # Extract text excluding images and tables
    text_elements = [el.text for el in elements if el.category not in ["Image", "Table"]]

    # Extract text from images saved in media_path
    for image_file in os.listdir(media_path):
        fname, ext = os.path.splitext(image_file)
        if ext.lower() in ['.jpg', '.jpeg', '.png']:
            image_path = os.path.join(media_path, image_file)
            image_text = text_from_image(image_path)
            text_elements.append(image_text)

    return "\n\n".join(text_elements)

# Split large text into smaller chunks for vector storage
def split_pdf_text(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    return text_splitter.split_text(text)

# Store chunks of pdf text in vector store
def store_pdf_docs(text_chunks):
    vector_store.add_texts(text_chunks)

# Store web documents in vector store
def store_web_docs(docs):
    vector_store.add_documents(docs)

# Search similar documents for a query
def retrieve_docs(query):
    return vector_store.similarity_search(query)

# Generate answer from question and retrieved docs
def answer_question(question, documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    return chain.invoke({"question": question, "context": context})
