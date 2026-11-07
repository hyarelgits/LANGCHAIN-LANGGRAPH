APP.PY - DETAILED EXPLANATION GUIDE

OVERVIEW
========
app.py is the entry point of the application.

Think of app.py as the reception desk of the project.

Users do not directly talk to:
- LangGraph
- ChromaDB
- PostgreSQL
- Ollama

Users talk to FastAPI through app.py.

HIGH LEVEL FLOW
===============
Browser
   |
   v
app.py
   |
   v
graph_rag.py
   |
   +---- RAG
   |
   +---- MCP
   |
   +---- Direct LLM
   |
   v
Answer

IMPORT SECTION
==============
from fastapi import FastAPI

Purpose:
Import FastAPI framework.

FastAPI is used to create APIs.

Without FastAPI:
- No REST API
- No Swagger UI
- No HTTP endpoints

----------------------------------

from chroma_db_code.graph_rag import graph

Purpose:
Import compiled LangGraph workflow.

This graph contains:
- Router Node
- RAG Node
- MCP Node
- Direct Node

This line connects FastAPI with LangGraph.

APPLICATION CREATION
====================
app = FastAPI()

Purpose:
Create FastAPI application object.

Think:
New web server application created.

This object stores:
- Routes
- Endpoints
- Request handlers
- Swagger metadata

UVICORN STARTUP
===============
When you run:

uvicorn app:app --reload

Meaning:

First app = app.py file
Second app = FastAPI object

Uvicorn loads app.py
Then finds:

app = FastAPI()

HOME ENDPOINT
=============
@app.get("/")

def home():

Purpose:
Application landing endpoint.

Request:
GET /

Response:
{
  "message": "Loan Policy AI Assistant Running"
}

HEALTH ENDPOINT
===============
@app.get("/health")

def health():

Used for monitoring.

Request:
GET /health

Response:
{
  "status":"UP"
}

Useful for:
- Docker
- Kubernetes
- Monitoring tools

ASK ENDPOINT
============
@app.get("/ask")

def ask(question:str):

Most important API.

Receives question from browser.

Example:

/ask?question=What is minimum CIBIL score?

FastAPI automatically stores value in:

question

GRAPH INVOCATION
================
result = graph.invoke(
{
   "question": question
}
)

Purpose:
Send user question into LangGraph.

State created:

{
   "question":"What is minimum CIBIL score?"
}

LangGraph then starts execution.

LANGGRAPH FLOW
==============
Question
   |
   v
Router
   |
   +--- RAG
   |
   +--- MCP
   |
   +--- Direct

RAG EXAMPLE
===========
Question:
What is minimum CIBIL score?

Flow:
Router
 -> RAG Node
 -> ChromaDB
 -> Ollama
 -> Answer

MCP EXAMPLE
===========
Question:
Show customer details

Flow:
Router
 -> MCP Node
 -> PostgreSQL
 -> Ollama
 -> Answer

DIRECT EXAMPLE
==============
Question:
Hello

Flow:
Router
 -> Direct Node
 -> Ollama
 -> Answer

FINAL RESPONSE
==============
return {
   "question": question,
   "answer": result["answer"]
}

Purpose:
Return JSON response back to client.

Example:
{
   "question":"Show customer details",
   "answer":"Customer Ravi has CIBIL score 760"
}

END TO END EXECUTION
====================
User Question
    |
    v
FastAPI Endpoint
    |
    v
graph.invoke()
    |
    v
LangGraph Router
    |
    +---- RAG
    +---- MCP
    +---- Direct
    |
    v
Ollama
    |
    v
Answer
    |
    v
JSON Response

INTERVIEW ANSWER
================
app.py is the FastAPI entry point of the application. It exposes REST endpoints, receives user requests, invokes the LangGraph workflow using graph.invoke(), and returns responses as JSON. It acts as the bridge between the frontend and the backend AI components such as LangGraph, ChromaDB, PostgreSQL, MCP tools, and Ollama.




===========================



# Import FastAPI framework

# FastAPI helps us create REST APIs

# It provides HTTP endpoints like GET and POST

# Swagger documentation is automatically generated

from fastapi import FastAPI


# Import LangGraph workflow

# graph is the compiled LangGraph object

# This graph contains Router, RAG, MCP and Direct nodes

# FastAPI will call graph.invoke() whenever a user asks a question

from chroma_db_code.graph_rag import graph


# Create FastAPI application object

# This is the main web application

# All API endpoints will be attached to this object

# Uvicorn looks for this object during startup

app = FastAPI()


# Create API endpoint "/"

# @app.get means this endpoint handles HTTP GET requests

# When user opens http://localhost:8000/

# FastAPI executes home() function

@app.get("/")
def home():

    # Return JSON response

    # Useful for checking whether application is running

    # Browser receives this data as JSON

    return {
        "message": "Loan Policy AI Assistant Running"
    }


# Create health endpoint

# Used by monitoring systems

# Used by Docker and Kubernetes health checks

# Confirms API service is alive

@app.get("/health")
def health():

    # Return simple status response

    # If response comes back, service is healthy

    return {
        "status": "UP"
    }


# Main AI endpoint

# User sends question using query parameter

# Example:
# /ask?question=What is minimum CIBIL score?

@app.get("/ask")
def ask(question: str):

    # Create LangGraph state object

    # Question is placed into graph state

    # Graph execution starts from Router node

    result = graph.invoke(
        {
            "question": question
        }
    )

    # graph.invoke() returns state

    # Example:
    # {
    #   "question":"Show customer details",
    #   "route":"mcp",
    #   "answer":"Customer Ravi..."
    # }

    # Return final JSON response

    # Question returned for reference

    # Answer generated by LangGraph workflow

    return {
        "question": question,
        "answer": result["answer"]
    }



===============================
