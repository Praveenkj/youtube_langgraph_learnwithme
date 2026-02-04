from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv("./env")

google_api_key = os.getenv("GOOGLE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

google_llm = ChatGoogleGenerativeAI(
    temperature=0, 
    model="gemini-2.5-flash", 
    api_key=google_api_key,
    max_tokens=200
)

openai_llm = ChatOpenAI(
    temperature=0, 
    model="gpt-4", 
    api_key=openai_api_key
)

# openai_llm.invoke("Hello")


from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from IPython.display import display, Image
from typing import Literal
from langchain_core.messages import HumanMessage, AIMessage, RemoveMessage


class MessagesState(MessagesState):
    summary: str

def conversation(state: MessagesState):
    summary = state.get('summary')
    if summary:
        messages_for_invoke = [SystemMessage(content=f"Here is the summary of the conversation to date: {summary}")] + state.get('messages')
    else:
        messages_for_invoke = state.get('messages')
    
    return {"messages": google_llm.invoke(messages_for_invoke)}

def summarize(state: MessagesState):
    print("Summarizing...")

    summary = state.get('summary')
    if summary:
        summary_message = (
            f"Here is the summary of the conversation to date: {summary}.\n\n"
            "Extend this summary with the new messages above:"
        )
    else:
        summary_message = f"Summarize this conversation: "

    messages = [HumanMessage(content=summart_message)] + state.get('messages')
    res = google_llm.invoke(messages)
    
    delete_messages = [RemoveMessage(msg.id) for msg in state['messages'][:-2]]
    
    print(f"After summary: \n {res.content} \n Delete messages: \n{delete_messages}")

    return {"summary": res.content, "messages": delete_messages}

def should_summarize(state: MessagesState) -> Literal['__end__', "summarize"]:
    messages =  state['messages']
    print("Checking should summarize...")
    print(f"Messages length: {len(messages)}")
    if len(messages) <= 4:
        print("Not summarizing...")
        return END
    else:
        return "summarize"

memory = MemorySaver()

builder = StateGraph(MessagesState)

builder.add_node("conversation", conversation)
builder.add_node("summarize", summarize)

builder.add_edge(START, "conversation")
builder.add_conditional_edges("conversation", should_summarize)
builder.add_edge("summarize", END)


graph = builder.compile(checkpointer=memory)


config = {"configurable": {"thread_id": 1}}


graph.invoke({"messages": HumanMessage(content="Hi, tell me a joke")}, config=config)
graph.invoke({"messages": HumanMessage(content="That joke was bad.")}, config=config)
graph.invoke({"messages": HumanMessage(content="My name is Praveen.")}, config=config)