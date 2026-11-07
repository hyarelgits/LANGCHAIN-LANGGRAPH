GRAPH_RAG.PY - DETAILED EXPLANATION GUIDE

OVERVIEW
--------
graph_rag.py is the brain of the application. It uses LangGraph to decide which path a user question should take.

Possible paths:
1. RAG Node      -> Loan policy questions
2. MCP Node      -> Customer database questions
3. Direct Node   -> General chat questions

HIGH LEVEL FLOW
---------------
User Question
      |
      v
   Router
      |
   +--+----------------+
   |                   |
   v                   v
 RAG Node          MCP Node
   |                   |
 ChromaDB         PostgreSQL
   |                   |
   +--------+----------+
            |
            v
         Ollama
            |
            v
         Answer

SECTION 1 - IMPORTS
-------------------
from pathlib import Path
Used for folder and file path handling.

from typing import TypedDict
Used to define the graph state structure.

from langgraph.graph import StateGraph, END
StateGraph creates the workflow.
END marks workflow completion.

from langchain_ollama import ChatOllama
Loads the LLM through Ollama.

from langchain_ollama import OllamaEmbeddings
Creates embedding vectors.

from langchain_community.vectorstores import Chroma
Loads ChromaDB vector database.

from chroma_db_code.db_tools import get_customer
Imports PostgreSQL utility function.

SECTION 2 - PROJECT PATHS
-------------------------
BASE = Path(__file__).resolve().parent.parent
Finds project root path.

DB_DIR = str(BASE / "chroma_db_storage")
Points to vector database location.

SECTION 3 - EMBEDDING MODEL
---------------------------
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

Purpose:
Convert text into vectors.

Example:
"minimum cibil score" -> [0.12,0.44,0.98,...]

SECTION 4 - CHROMADB
--------------------
db = Chroma(...)

Loads existing ChromaDB vectors.
Used during retrieval.

SECTION 5 - LLM
---------------
llm = ChatOllama(
    model="llama3.2:1b"
)

Responsible for final response generation.

SECTION 6 - STATE
-----------------
class State(TypedDict):

question : user question
route    : selected route
context  : retrieved documents
answer   : final answer

State travels between graph nodes.

SECTION 7 - ROUTER NODE
-----------------------
def router(state):

Reads user question.

If contains:
customer
-> MCP route

If contains:
loan
cibil
policy
eligibility
-> RAG route

Otherwise:
-> Direct route

Acts like a traffic controller.

SECTION 8 - RAG NODE
--------------------
def rag_node(state):

Steps:
1. Receive question
2. Search ChromaDB
3. Retrieve matching chunks
4. Build prompt
5. Call Ollama
6. Return answer

Used for:
Loan policy questions
Eligibility questions
CIBIL questions

SECTION 9 - MCP NODE
--------------------
def mcp_node(state):

Steps:
1. Receive question
2. Call get_customer()
3. Query PostgreSQL
4. Fetch customer data
5. Build prompt
6. Call Ollama
7. Return answer

Used for:
Show customer details
Customer information
Customer profile

SECTION 10 - DIRECT NODE
------------------------
def direct_node(state):

Directly calls Ollama.
No ChromaDB.
No Database.

Used for:
Hello
Good morning
General conversation

SECTION 11 - CHOOSE ROUTE
-------------------------
def choose_route(state):

Returns selected route.

Example:
return 'rag'

LangGraph then moves to RAG node.

SECTION 12 - BUILD GRAPH
------------------------
builder = StateGraph(State)

Creates graph object.

builder.add_node(...)

Registers nodes:
router
rag
mcp
direct

builder.set_entry_point('router')

Every question starts at router.

builder.add_conditional_edges(...)

Defines routing logic.

RAG -> rag node
MCP -> mcp node
DIRECT -> direct node

builder.add_edge(..., END)

Marks completion after node execution.

graph = builder.compile()

Creates executable graph.

FINAL EXECUTION FLOW
--------------------
Question
   |
   v
Router
   |
   +-------------+--------------+
   |             |              |
   v             v              v
 RAG           MCP          DIRECT
   |             |              |
   v             v              v
ChromaDB    PostgreSQL      Ollama
   |             |              |
   +-------------+--------------+
                 |
                 v
              Answer



      =========================



LANGGRAPH - STATE(TypedDict) DETAILED EXPLANATION

CODE
-----
class State(TypedDict):
    question: str
    route: str
    context: str
    answer: str

WHAT IS STATE?
--------------
State is the shared data container used by LangGraph.

Think of State as a school notebook that travels between all graph nodes.

Router Node writes information into the notebook.
RAG Node reads information from the notebook.
MCP Node reads information from the notebook.
LLM Node writes the final answer into the notebook.

WHY DO WE NEED STATE?
---------------------
Without State, nodes cannot share information.

Example:
User asks:
What is minimum CIBIL score?

Router must know the question.
RAG node must know the question.
LLM must know the context.
FastAPI must know the final answer.

State carries all this information.

UNDERSTANDING TypedDict
-----------------------
TypedDict is a dictionary with predefined fields.

Normal dictionary:
{
    "anything": "allowed"
}

TypedDict:
{
    "question": str,
    "route": str,
    "context": str,
    "answer": str
}

This helps developers understand what data is expected.

FIELD 1 - question
------------------
question: str

Stores the user's question.

Example:
question = "What is minimum CIBIL score?"

This field is used by:
- router()
- rag_node()
- mcp_node()
- direct_node()

FIELD 2 - route
---------------
route: str

Stores routing decision.

Possible values:
rag
mcp
direct

Example:
route = "rag"

Meaning:
Send request to RAG node.

FIELD 3 - context
-----------------
context: str

Stores retrieved information.

Example:
"Minimum CIBIL score is 750"

Generated by RAG search.

Passed to Ollama.

FIELD 4 - answer
----------------
answer: str

Stores final answer.

Example:
"Minimum CIBIL score required is 750."

Returned back to FastAPI.

STATE EVOLUTION
---------------
STEP 1
{
  "question": "What is minimum CIBIL score?"
}

STEP 2
{
  "question": "What is minimum CIBIL score?",
  "route": "rag"
}

STEP 3
{
  "question": "What is minimum CIBIL score?",
  "route": "rag",
  "context": "Minimum CIBIL score is 750"
}

STEP 4
{
  "question": "What is minimum CIBIL score?",
  "route": "rag",
  "context": "Minimum CIBIL score is 750",
  "answer": "Minimum CIBIL score required is 750"
}

INTERVIEW ANSWER
----------------
State(TypedDict) defines the shared data structure that flows between LangGraph nodes. It stores the user's question, routing decision, retrieved context and final answer. Each node reads from and writes to the State object during graph execution.

