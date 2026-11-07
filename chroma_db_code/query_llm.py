from pathlib import Path

from langchain_ollama import ChatOllama
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

llm = ChatOllama(
    model="llama3.2:1b"
)

question = input("Ask Question: ")

docs = db.similarity_search(
    question,
    k=2
)

context = "\n".join(
    [doc.page_content for doc in docs]
)

prompt = f"""
You are a loan assistant.

Context:
{context}

Question:
{question}

Answer based only on the context.
"""

response = llm.invoke(prompt)

print("\nANSWER:\n")
print(response.content)
