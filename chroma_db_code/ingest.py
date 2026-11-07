from pathlib import Path
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

BASE = Path(__file__).resolve().parent.parent
DOCS = BASE / "documents"
DB_DIR = str(BASE / "chroma_db_storage")

def main():
    files = [DOCS / "doc1_cibil_rule.txt",
             DOCS / "doc2_loan_policy.txt"]

    docs = []

    for f in files:
        docs.extend(TextLoader(str(f), encoding="utf-8").load())

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    ).split_documents(docs)

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=DB_DIR
    )

    print(f"Ingested {len(chunks)} chunks into {DB_DIR}")

if __name__ == "__main__":
    main()
