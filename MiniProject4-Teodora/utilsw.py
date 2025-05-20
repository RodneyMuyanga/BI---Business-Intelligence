# for deployment and UI
import streamlit as st
import os

from langchain_community.document_loaders import SeleniumURLLoader
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.utils.constants import PartitionStrategy
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore


embeddings = OllamaEmbeddings(model="llama3:8b")
vector_store = InMemoryVectorStore(embeddings)

llm = OllamaLLM(model="gemma3:12b")

# directories
data = './data/'
media = './media/'

# A template for the dialoque
template = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer:
"""


# load web page
def load_web_page(url):
    loader = SeleniumURLLoader(urls=[url])
    documents = loader.load()
    return documents


# split web text
def split_web_text(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    return text_splitter.split_documents(docs)


# save uploaded PDF
def upload_pdf(file):
    with open(data + file.name, "wb") as f:
        f.write(file.getbuffer())


# extract text from image with LLM
def text_from_image(file_path):
    print(file_path)
    model_with_image_context = llm.bind(images=[file_path])
    return model_with_image_context.invoke("Tell me what do you see in this picture.")


# parse PDF content (text + images)
def parse_pdf(file_path, media_path):
    elements = partition_pdf(
        file_path,
        strategy=PartitionStrategy.HI_RES,
        extract_image_block_types=["Image", "Table"],
        extract_image_block_output_dir=media_path
    )

    # extract text blocks ignoring images/tables
    text_elements = [el.text for el in elements if el.category not in ["Image", "Table"]]
    print(text_elements)
    
    # extract text from images in media_path
    for image_file in os.listdir(media_path):
        fname, extension = os.path.splitext(image_file)
        if extension.lower() in ['.jpg', '.jpeg', '.png']:
            image_path = os.path.join(media_path, image_file)
            image_text = text_from_image(image_path)
            text_elements.append(image_text)

    return "\n\n".join(text_elements)


# split pdf text into chunks
def split_pdf_text(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    return text_splitter.split_text(text)


# store web docs to vector store
def store_web_docs(docs):
    vector_store.add_documents(docs)


# store pdf text chunks to vector store
def store_pdf_docs(texts):
    vector_store.add_texts(texts)


# retrieve similar docs from vector store
def retrieve_docs(query):
    return vector_store.similarity_search(query)


# answer question using LLM + context
def answer_question(question, documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    return chain.invoke({"question": question, "context": context})
