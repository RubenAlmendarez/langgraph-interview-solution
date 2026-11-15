
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from mock_tools import search_policy, fetch_booking


# MODULE 1: Shared state
class AgentState(TypedDict):
    question: str
    route: str
    context: str
    error: str
    answer: str


# MODULE 2: Classify the request
def classify_request(state: AgentState):
    question = state["question"].lower()

    if "booking" in question:
        return {"route": "booking"}

    if "baggage" in question or "policy" in question:
        return {"route": "policy"}

    return {"route": "fallback"}


# MODULE 3: Execute the selected tool
def execute_tool(state: AgentState):
    try:
        if state["route"] == "policy":
            context = search_policy(state["question"])

        elif state["route"] == "booking":
            context = fetch_booking(state["question"])

        else:
            return {
                "context": "",
                "error": "Unknown tool route"
            }

        return {
            "context": context,
            "error": ""
        }

    except TimeoutError as exc:
        return {
            "context": "",
            "error": str(exc)
        }


# MODULE 4: Determine what happens after the tool
def route_after_tool(state: AgentState):
    if state["error"] or not state["context"]:
        return "fallback"

    return "format"


# MODULE 5: Generate a response
def format_response(state: AgentState):
    return {
        "answer": f"ANSWER: {state['context']}"
    }


# MODULE 6: Handle unsupported requests or failures
def fallback(state: AgentState):
    if state["error"]:
        reason = state["error"]

    elif state["route"] == "policy":
        reason = "No matching policy"

    else:
        reason = "Unsupported request"

    return {
        "answer": f"ESCALATED: {reason}"
    }


# MODULE 7: Build the LangGraph workflow
def build_graph():
    graph = StateGraph(AgentState)

    # Register nodes
    graph.add_node("classify", classify_request)
    graph.add_node("tool", execute_tool)
    graph.add_node("format", format_response)
    graph.add_node("fallback", fallback)

    # Entry point
    graph.add_edge(START, "classify")

    # Conditional routing after classification
    graph.add_conditional_edges(
        "classify",
        lambda state: state["route"],
        {
            "booking": "tool",
            "policy": "tool",
            "fallback": "fallback"
        }
    )

    # Conditional routing after tool execution
    graph.add_conditional_edges(
        "tool",
        route_after_tool,
        {
            "format": "format",
            "fallback": "fallback"
        }
    )

    # Terminal edges
    graph.add_edge("format", END)
    graph.add_edge("fallback", END)

    return graph.compile()


# MODULE 8: Execute example requests
if __name__ == "__main__":
    app = build_graph()

    questions = [
        "What is the baggage policy?",
        "Check my booking",
        "Booking timeout",
        "Tell me a joke",
        "What is the refund policy?"
    ]

    for question in questions:
        result = app.invoke({
            "question": question,
            "route": "",
            "context": "",
            "error": "",
            "answer": ""
        })

        print(f"\nQuestion: {question}")
        print(f"Route: {result['route']}")
        print(f"Answer: {result['answer']}")
