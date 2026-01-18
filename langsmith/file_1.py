from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    graph_state: str

def node_1(state):
    print("node__1")
    return {"graph_state": state["graph_state"] + "I am"}

def node_2(state: State) -> State:
    print("node__2")
    return {"graph_state": state["graph_state"] + " happy."}

def node_3(state: State) -> State:
    print("node__3")
    return {"graph_state": state["graph_state"] + " sad."}

def node_4(state: State) -> State:
    print("node__4")
    return {"graph_state": state["graph_state"] + " neutral."}


import random
from typing import Literal
def decide_mood(state) -> Literal["node_2", "node_3", "node_4"]:
    user_input = state['graph_state']
    ran = random.random()
    if ran < 0.3:
        return "node_2"
    if ran < 0.6:
        return "node_3"
    if ran < 1:
        return "node_4"


# Build graph
builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)
builder.add_node("node_4", node_4)


# Logic
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)
builder.add_edge("node_4", END)

graph = builder.compile()

graph.invoke({"graph_state": "Hi, I am Praveen. "})

from IPython.display import display,Image
display(Image(graph.get_graph().draw_mermaid_png()))

