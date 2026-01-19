from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    graph_state: str
    num: int

num = 0

def node_1(state):
    print("node__1")
    state["num"] = state.get("num", 0) + 1 # Updating it just in function won't work. Return it as a state.
    num = state.get("num")
    print(state['graph_state'])
    return {"graph_state": state["graph_state"] + f" {num}", "num": num} 

from typing import Literal
def should_continue(state) -> Literal["node_1", "__end__"]:
    if state.get("num", 0) >= 10:
        return "__end__"
    return "node_1"


# Build graph
builder = StateGraph(State)
builder.add_node("node_1", node_1)


# Logic
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", should_continue)

graph = builder.compile()

graph.invoke({"graph_state": "Hi, I am Praveen. "})

from IPython.display import display,Image
display(Image(graph.get_graph().draw_mermaid_png()))

