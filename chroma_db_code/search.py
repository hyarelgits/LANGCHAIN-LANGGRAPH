from pathlib import Path
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

BASE = Path(__file__).resolve().parent.parent
DB_DIR = str(BASE / "chroma_db_storage")

def search_documents(question: str, k: int = 3):
    db = Chroma(persist_directory=DB_DIR, embedding_function=OllamaEmbeddings(model="llama3.2:1b"))
    results = db.similarity_search(question, k=k)
    return [r.page_content for r in results]

if __name__ == "__main__":
    q = "What is the exception if CIBIL is 680?"
    for i, text in enumerate(search_documents(q), 1):
        print(f"--- Result {i} ---\n{text}\n")
