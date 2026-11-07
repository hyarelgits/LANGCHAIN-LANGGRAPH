from pathlib import Path
from typing import TypedDict

from langgraph.graph import StateGraph, END

from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

from chroma_db_code.db_tools import get_customer


# =====================================================
# PATHS
# =====================================================

BASE = Path(__file__).resolve().parent.parent
DB_DIR = str(BASE / "chroma_db_storage")


# =====================================================
# EMBEDDINGS
# =====================================================

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# =====================================================
# CHROMADB
# =====================================================

db = Chroma(
    persist_directory=DB_DIR,
    embedding_function=embeddings
)


# =====================================================
# LLM
# =====================================================

llm = ChatOllama(
    model="llama3.2:1b"
)


# =====================================================
# STATE
# =====================================================

class State(TypedDict):
    question: str
    route: str
    context: str
    answer: str


# =====================================================
# ROUTER
# =====================================================

def router(state):

    q = state["question"].lower()

    if "customer" in q:
        return {"route": "mcp"}

    if (
        "loan" in q
        or "cibil" in q
        or "policy" in q
        or "eligibility" in q
    ):
        return {"route": "rag"}

    return {"route": "direct"}


# =====================================================
# RAG NODE
# =====================================================

def rag_node(state):

    print("******** RAG NODE EXECUTED ********")

    docs = db.similarity_search(
        state["question"],
        k=2
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    print("CONTEXT FOUND:")
    print(context)

    prompt = f"""
You are a Loan Policy Assistant.

Use ONLY information from context.

Context:
{context}

Question:
{state["question"]}
"""

    response = llm.invoke(prompt)

    return {
        "context": context,
        "answer": response.content
    }


# =====================================================
# MCP NODE (POSTGRESQL)
# =====================================================

def mcp_node(state):

    print("******** MCP NODE EXECUTED ********")

    customer = get_customer("1001")

    if not customer:
        return {
            "answer": "Customer not found"
        }

    prompt = f"""
Customer Details

Customer Name: {customer[0]}
CIBIL Score: {customer[1]}
Income: {customer[2]}
Loan Type: {customer[3]}

Answer the user question:

{state["question"]}
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }


# =====================================================
# DIRECT LLM NODE
# =====================================================

def direct_node(state):

    print("******** DIRECT NODE EXECUTED ********")

    response = llm.invoke(
        state["question"]
    )

    return {
        "answer": response.content
    }


# =====================================================
# ROUTE DECISION
# =====================================================

def choose_route(state):
    return state["route"]


# =====================================================
# BUILD GRAPH
# =====================================================

builder = StateGraph(State)

builder.add_node(
    "router",
    router
)

builder.add_node(
    "rag",
    rag_node
)

builder.add_node(
    "mcp",
    mcp_node
)

builder.add_node(
    "direct",
    direct_node
)

builder.set_entry_point(
    "router"
)

builder.add_conditional_edges(
    "router",
    choose_route,
    {
        "rag": "rag",
        "mcp": "mcp",
        "direct": "direct"
    }
)

builder.add_edge("rag", END)
builder.add_edge("mcp", END)
builder.add_edge("direct", END)

graph = builder.compile()
