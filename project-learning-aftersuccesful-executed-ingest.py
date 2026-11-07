File: chroma_db_code/ingest.py
Python


ingest.py

============================
from pathlib import Path




# Import Path class for handling file and folder paths
# Import Path class from pathlib library

# Python has many built-in libraries

# pathlib is one of the built-in libraries

# pathlib helps us work with files and folders

# Without Path we would manually type:
# "/root/my-loan-project/documents"

# That becomes difficult to maintain

# Path provides cleaner code

# Path automatically handles folder separators

# Works on Linux, Windows and Mac

# Makes file handling easier

# Used throughout the project

# We use it later to build folder paths


======================================================================================================================

from langchain_ollama import OllamaEmbeddings


# Import OllamaEmbeddings class from langchain_ollama package

# This class is used to convert normal text into numerical vectors (embeddings)

# Embeddings help AI understand the meaning of text instead of only matching keywords

# Later in ingest.py, this class connects to the local Ollama server and uses the
# "nomic-embed-text" model to generate embeddings

# These embeddings are finally stored inside ChromaDB for semantic search during RAG


=============================================================


# Import Ollama embedding model



# Import the OllamaEmbeddings class from the langchain_ollama package

# This class is used to convert normal text into AI-understandable vectors (embeddings)

# Embeddings help the system understand the meaning of text instead of only exact words

# The generated vectors are later stored in ChromaDB for semantic search operations

# This class communicates with the Ollama embedding model (for example: nomic-embed-text)


=========================================


from langchain_community.vectorstores import Chroma


# Import the Chroma class from LangChain's vector database module

# Chroma is a vector database used to store document embeddings

# After documents are converted into vectors, Chroma keeps them for fast retrieval

# During RAG, Chroma performs similarity search to find the most relevant document chunks

# This allows the AI assistant to answer questions using company documents instead of only LLM knowledge


=====================
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Import text splitter
# Splits large documents into smaller chunks
# Import RecursiveCharacterTextSplitter from LangChain

# This class is used to break large documents into smaller chunks

# Chunking helps the LLM process and search document content efficiently

# Overlapping chunks preserve context between consecutive text segments

# These chunks are later converted into embeddings and stored in ChromaDB

=======================
from langchain_community.document_loaders import TextLoader

# Import text file reader
# Reads .txt files from disk
# Import the TextLoader class from LangChain's document loader module

# TextLoader is used to read text files (.txt) from the local file system

# It converts raw text files into LangChain Document objects

# Document objects can later be split into chunks and converted into embeddings

# This is the first step of the RAG ingestion process because documents must be loaded before processing
====================================
# --------------------------------------------------
# PROJECT ROOT PATH
# --------------------------------------------------


BASE = Path(__file__).resolve().parent.parent




# __file__
# Current file location:
# /root/my-loan-project/chroma_db_code/ingest.py

# resolve()
# converts to full absolute path

# parent
# moves one folder up

# parent.parent
# moves two folders up

# Result:
# /root/my-loan-project



# --------------------------------------------------
# DOCUMENTS DIRECTORY
# --------------------------------------------------

DOCS = BASE / "documents"


# Creates path:
# /root/my-loan-project/documents



# --------------------------------------------------
# CHROMADB STORAGE DIRECTORY
# --------------------------------------------------


DB_DIR = str(BASE / "chroma_db_storage")

# Creates path:
# /root/my-loan-project/chroma_db_storage


# --------------------------------------------------
# MAIN FUNCTION
# --------------------------------------------------

# Program execution starts here

def main():

    # List of files we want to load

    files = [
        DOCS / "doc1_cibil_rule.txt",
        DOCS / "doc2_loan_policy.txt"
    ]

    # Empty list

    # Before:
    # []

    # Later:
    # [Document1, Document2]

    docs = []

    # --------------------------------------------------
    # LOAD DOCUMENTS
    # --------------------------------------------------

    # Loop through all files

    for f in files:

        # TextLoader reads file

        # str(f)
        # converts Path object to string

        # load()
        # reads text content

        # extend()
        # appends loaded document into docs list

        docs.extend(
            TextLoader(
                str(f),
                encoding="utf-8"
            ).load()
        )

    # --------------------------------------------------
    # SPLIT DOCUMENTS INTO CHUNKS
    # --------------------------------------------------



 splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    # Create smaller document pieces

    chunks = splitter.split_documents(docs)

    

    # Example:

    # Original Document:
    #
    # 5000 words

    # Chunk 1:
    # words 1-500

    # Chunk 2:
    # words 450-950

    # Chunk 3:
    # words 900-1400

    # overlap = 50 words

   

    # --------------------------------------------------
    # CREATE EMBEDDING MODEL
    # --------------------------------------------------

    # Uses Ollama

    # Model:
    # nomic-embed-text

    # Purpose:
    # Convert text to vectors

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    # --------------------------------------------------
    # STORE INSIDE CHROMADB
    # --------------------------------------------------

    # ChromaDB steps:

    # 1. Take chunks
    # 2. Generate embeddings
    # 3. Store vectors
    # 4. Save database to disk

    Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=DB_DIR
    )

    # --------------------------------------------------
    # SUCCESS MESSAGE
    # --------------------------------------------------

    print(
        f"Ingested {len(chunks)} chunks into {DB_DIR}"
    )


# --------------------------------------------------
# PROGRAM ENTRY POINT
# --------------------------------------------------

# If file is executed directly,
# call main()

if __name__ == "__main__":
    main()
