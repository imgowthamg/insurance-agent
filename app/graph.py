from langgraph.graph import StateGraph, END

from app.agents import (
    intent_agent,
    retriever_agent,
    policy_agent,
    decision_agent,
    report_agent
)


def route_after_retrieval(state):
    if not state.get("context"):
        return "end"
    return "continue"


def create_graph():

    workflow = StateGraph(dict)

    workflow.add_node("intent", intent_agent)
    workflow.add_node("retrieve", retriever_agent)
    workflow.add_node("analyze", policy_agent)
    workflow.add_node("decide", decision_agent)
    workflow.add_node("report", report_agent)

    workflow.set_entry_point("intent")

    workflow.add_edge("intent", "retrieve")

    # Conditional routing: skip to END if no context found
    workflow.add_conditional_edges(
        "retrieve",
        route_after_retrieval,
        {
            "continue": "analyze",
            "end": END
        }
    )

    workflow.add_edge("analyze", "decide")
    workflow.add_edge("decide", "report")

    # FIX: set_finish_point() does not exist in LangGraph; use add_edge to END
    workflow.add_edge("report", END)

    return workflow.compile()
