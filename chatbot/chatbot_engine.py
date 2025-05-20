# chatbot_engine.py

import os
from langchain_community.document_loaders import SeleniumURLLoader
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.utils.constants import PartitionStrategy
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore

# --- Environment setup ---
embeddings = OllamaEmbeddings(model="llama3:8b")
vector_store = InMemoryVectorStore(embeddings)
llm = OllamaLLM(model="llama3:8b")

# --- Web loader ---
def load_web_page(url):
    loader = SeleniumURLLoader(urls=[url])
    documents = loader.load()
    return documents

# --- PDF loader ---
def parse_pdf(file_path, media_dir):
    elements = partition_pdf(
        file_path,
        strategy=PartitionStrategy.HI_RES,
        extract_image_block_types=["Image", "Table"],
        extract_image_block_output_dir=media_dir
    )
    texts = [el.text for el in elements if el.category not in ["Image", "Table"] and el.text]
    return "\n\n".join(texts)

# --- Text splitting ---
def split_web_text(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
    return splitter.split_documents(docs)

def split_pdf_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
    return splitter.split_text(text)

# --- Vector storage ---
def store_web_docs(docs):
    vector_store.add_documents(docs)

def store_pdf_docs(texts):
    vector_store.add_texts(texts)

# --- Retrieval ---
def retrieve_docs(query):
    return vector_store.similarity_search(query)

# --- QA ---
def answer_question(question, documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    prompt = ChatPromptTemplate.from_template(TEMPLATE)
    chain = prompt | llm
    return chain.invoke({"question": question, "context": context})

# --- Prompt Template ---
TEMPLATE = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question.

Question: {question}
Context: {context}
Answer:
"""
