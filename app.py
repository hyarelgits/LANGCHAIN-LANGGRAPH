from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from chroma_db_code.graph_rag import graph

app = FastAPI(
    title="Loan Policy AI Assistant",
    description="RAG + LangGraph + Ollama + ChromaDB",
    version="1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Loan Policy AI Assistant Running",
        "technology": [
            "FastAPI",
            "LangGraph",
            "LangChain",
            "ChromaDB",
            "Ollama"
        ]
    }


@app.get("/health")
def health():
    return {
        "status": "UP"
    }


@app.get("/ask")
def ask(question: str):

    result = graph.invoke(
        {
            "question": question
        }
    )

    return {
        "question": question,
        "answer": result.get("answer", "")
    }
