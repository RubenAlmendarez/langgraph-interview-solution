
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# Shared state
class AgentState(TypedDict):
    message: str
    result: str


# Node 1
def process_message(state: AgentState):
    return {
        "result": state["message"].upper()
    }


# Build workflow
graph = StateGraph(AgentState)

graph.add_node("process", process_message)
graph.add_edge(START, "process")
graph.add_edge("process", END)

app = graph.compile()


# Execute
response = app.invoke({
    "message": "Hello LangGraph",
    "result": ""
})

print(response)
