import os
from langchain_community.document_loaders import SeleniumURLLoader
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.utils.constants import PartitionStrategy
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore

# --- Constants ---
PDF_DIR = "./data/"
MEDIA_DIR = "./media/"
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(MEDIA_DIR, exist_ok=True)

# --- LLM + Vector DB Setup ---
embeddings = OllamaEmbeddings(model="llama3:8b")
vector_store = InMemoryVectorStore(embeddings)
llm = OllamaLLM(model="gemma3:12b")

# --- Prompt Template ---
template = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer:
"""
prompt = ChatPromptTemplate.from_template(template)

# --- PDF Parsing with Image Extraction and OCR ---
def parse_pdf(file_path, media_path):
    elements = partition_pdf(
        file_path,
        strategy=PartitionStrategy.HI_RES,
        extract_image_block_types=["Image", "Table"],
        extract_image_block_output_dir=media_path,
    )

    # Extract text blocks ignoring images and tables
    text_elements = [el.text for el in elements if el.category not in ["Image", "Table"]]

    # Extract text from images by calling LLM bound with images
    for image_file in os.listdir(media_path):
        fname, ext = os.path.splitext(image_file)
        if ext.lower() in ['.jpg', '.jpeg', '.png']:
            image_path = os.path.join(media_path, image_file)
            image_text = text_from_image(image_path)
            text_elements.append(image_text)

    return "\n\n".join(text_elements)

def text_from_image(file_path):
    model_with_image_context = llm.bind(images=[file_path])
    return model_with_image_context.invoke("Tell me what do you see in this picture.")

# --- Text Splitting ---
def split_pdf_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    return splitter.split_text(text)

# --- Store Documents ---
def store_pdf_docs(text_chunks):
    vector_store.add_texts(text_chunks)

def store_web_docs(documents):
    vector_store.add_documents(documents)

# --- Retrieval & QA ---
def retrieve_docs(query):
    return vector_store.similarity_search(query)

def answer_question(question, documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    chain = prompt | llm
    return chain.invoke({"question": question, "context": context})

# --- Web Page Loader (optional) ---
def load_web_page(url):
    loader = SeleniumURLLoader(urls=[url])
    documents = loader.load()
    return documents

def split_web_text(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    return splitter.split_documents(documents)

# --- Upload & Process PDF ---
def upload_pdf(file):
    save_path = os.path.join(PDF_DIR, file.name)
    with open(save_path, "wb") as f:
        f.write(file.getbuffer())

def process_uploaded_pdf(file):
    upload_pdf(file)
    text = parse_pdf(os.path.join(PDF_DIR, file.name), MEDIA_DIR)
    chunks = split_pdf_text(text)
    store_pdf_docs(chunks)
