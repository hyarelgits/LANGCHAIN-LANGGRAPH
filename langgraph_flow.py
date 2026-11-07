from typing import TypedDict
from langgraph.graph import StateGraph, END
from agents.search_agent import search_agent
from agents.db_agent import db_agent
from agents.writer_agent import writer_agent

class State(TypedDict):
    question: str
    user_name: str
    search_result: dict
    db_result: dict
    answer: str

def search_node(state: State):
    return {"search_result": search_agent(state["question"])}

def db_node(state: State):
    return {"db_result": db_agent(state.get("user_name", "Hyarel"))}

def writer_node(state: State):
    answer = writer_agent(state["question"], state["search_result"], state["db_result"])
    return {"answer": answer}

def route_after_search(state: State):
    if state["search_result"].get("found"):
        return "db"
    return "writer"

graph = StateGraph(State)
graph.add_node("search", search_node)
graph.add_node("db", db_node)
graph.add_node("writer", writer_node)
graph.set_entry_point("search")
graph.add_conditional_edges("search", route_after_search, {"db": "db", "writer": "writer"})
graph.add_edge("db", "writer")
graph.add_edge("writer", END)
app = graph.compile()

def run_loan_flow(question: str, user_name: str = "Hyarel"):
    result = app.invoke({"question": question, "user_name": user_name, "search_result": {}, "db_result": {}, "answer": ""})
    return result["answer"]

if __name__ == "__main__":
    print(run_loan_flow("Am I eligible for 50000 personal loan?", "Hyarel"))
