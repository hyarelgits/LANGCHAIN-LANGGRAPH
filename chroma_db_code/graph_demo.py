
from typing import TypedDict

from langgraph.graph import StateGraph, END


class LoanState(TypedDict):
    question: str
    answer: str


def retrieve_node(state):
    print("Searching policy documents...")

    return {
        "answer": "Minimum CIBIL score is 750"
    }


builder = StateGraph(LoanState)

builder.add_node("retrieve", retrieve_node)

builder.set_entry_point("retrieve")

builder.add_edge("retrieve", END)

graph = builder.compile()

result = graph.invoke(
    {
        "question": "What is minimum CIBIL score?"
    }
)

print(result)
