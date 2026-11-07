from pathlib import Path
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

BASE = Path(__file__).resolve().parent.parent
DB_DIR = str(BASE / "chroma_db_storage")

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

db = Chroma(
    persist_directory=DB_DIR,
    embedding_function=embeddings
)

question = input("Ask a question: ")

results = db.similarity_search(
    question,
    k=2
)

print("\nResults:\n")

for doc in results:
    print(doc.page_content)
    print("-" * 50)

