from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document

from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os
import shutil

load_dotenv()
USE_OPENAI = os.getenv("USE_OPENAI", "False") == "True"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CHROMA_PATH = "chroma"
DATA_PATH = "pdf"


def main():
    generate_data_store()


def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[0]
    print(document.page_content)
    print(document.metadata)

    return chunks


def save_to_chroma(chunks: list[Document]):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    if USE_OPENAI:
        db = Chroma.from_documents(
            chunks,
            OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY),
            persist_directory=CHROMA_PATH,
            # chunks, HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"), persist_directory=CHROMA_PATH
        )
    else:
        db = Chroma.from_documents(
            chunks,
            HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
            persist_directory=CHROMA_PATH,
        )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    main()
