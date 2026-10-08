from langgraph.graph import StateGraph, START, END

from src.state import MeetingState

from src.agents.topic_agent import topic_agent
from src.agents.summary_agent import summary_agent
from src.agents.action_agent import action_agent
from src.agents.priority_agent import priority_agent


# --------------------------------------------------
# Input Node
# --------------------------------------------------

def input_node(state: MeetingState) -> MeetingState:
    """
    Initial node that receives the meeting transcript.
    """
    return state


# --------------------------------------------------
# Conditional Routing
# --------------------------------------------------

def route_after_actions(state: MeetingState) -> str:
    """
    Decide whether the Priority Agent should execute.
    """

    if state["has_action_items"]:
        return "priority"

    return "final"


# --------------------------------------------------
# Final Report Node
# --------------------------------------------------

def final_report_node(state: MeetingState) -> MeetingState:
    """
    Build the final structured meeting analysis report.
    """

    if state["has_action_items"]:

        action_items = state["action_items"]

        priorities = state["priorities"]

    else:

        action_items = "No action items identified in this meeting."

        priorities = "No action items identified in this meeting."

    state["final_report"] = {
        "summary": state["summary"],
        "topics": state["topics"],
        "action_items": action_items,
        "priorities": priorities,
    }

    return state


# --------------------------------------------------
# Build LangGraph
# --------------------------------------------------

builder = StateGraph(MeetingState)


# --------------------------------------------------
# Add Nodes
# --------------------------------------------------

builder.add_node("input", input_node)

builder.add_node("topics", topic_agent)

builder.add_node("summary", summary_agent)

builder.add_node("actions", action_agent)

builder.add_node("priority", priority_agent)

builder.add_node("final", final_report_node)


# --------------------------------------------------
# Graph Edges
# --------------------------------------------------

builder.add_edge(START, "input")

builder.add_edge("input", "topics")

builder.add_edge("topics", "summary")

builder.add_edge("summary", "actions")


# --------------------------------------------------
# Conditional Edge
# --------------------------------------------------

builder.add_conditional_edges(
    "actions",
    route_after_actions,
    {
        "priority": "priority",
        "final": "final",
    },
)


# --------------------------------------------------
# Priority → Final Report
# --------------------------------------------------

builder.add_edge("priority", "final")


# --------------------------------------------------
# Final Report → END
# --------------------------------------------------

builder.add_edge("final", END)


# --------------------------------------------------
# Compile Graph
# --------------------------------------------------

graph = builder.compile()