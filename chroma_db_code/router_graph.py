from typing import TypedDict

from langgraph.graph import StateGraph, END


class State(TypedDict):
    question: str
    route: str
    answer: str


def router(state):
    q = state["question"].lower()

    if "cibil" in q:
        return {"route": "rag"}

    return {"route": "direct"}


def rag_node(state):
    return {
        "answer": "Minimum CIBIL score is 750"
    }


def direct_node(state):
    return {
        "answer": "General answer"
    }


builder = StateGraph(State)

builder.add_node("router", router)
builder.add_node("rag", rag_node)
builder.add_node("direct", direct_node)

builder.set_entry_point("router")


def choose_route(state):
    return state["route"]


builder.add_conditional_edges(
    "router",
    choose_route,
    {
        "rag": "rag",
        "direct": "direct",
    }
)

builder.add_edge("rag", END)
builder.add_edge("direct", END)

graph = builder.compile()

result = graph.invoke(
    {
        "question": input("Ask: ")
    }
)

print(result["answer"])
