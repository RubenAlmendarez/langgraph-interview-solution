
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# 1. Define shared state
class AgentState(TypedDict):
    message: str
    route: str
    result: str


# 2. Classification node
def classify_request(state: AgentState):
    message = state["message"].lower()

    if "error" in message:
        return {"route": "review"}

    return {"route": "auto"}


# 3. Processing nodes
def automatic_processing(state: AgentState):
    return {"result": "AUTO"}


def manual_review(state: AgentState):
    return {"result": "REVIEW"}


# 4. Conditional routing
def router(state: AgentState):
    return state["route"]


# 5. Build the graph
def build_graph():
    graph = StateGraph(AgentState)

    # Register nodes
    graph.add_node("classify", classify_request)
    graph.add_node("automatic", automatic_processing)
    graph.add_node("manual", manual_review)

    # Define entry point
    graph.add_edge(START, "classify")

    # Conditional routing
    graph.add_conditional_edges(
        "classify",
        router,
        {
            "auto": "automatic",
            "review": "manual"
        }
    )

    # Define terminal edges
    graph.add_edge("automatic", END)
    graph.add_edge("manual", END)

    return graph.compile()


# 6. Run tests
if __name__ == "__main__":
    app = build_graph()

    test_cases = [
        ("Process sales report", "AUTO"),
        ("Error in transactions", "REVIEW"),
        ("Check inventory levels", "AUTO"),
        ("ERROR in database", "REVIEW")
    ]

    for message, expected in test_cases:
        response = app.invoke({
            "message": message,
            "route": "",
            "result": ""
        })

        assert response["result"] == expected, (
            f"Expected {expected}, got {response['result']}"
        )

        print(f"PASS: {message} -> {response['result']}")

    print("All tests passed!")
