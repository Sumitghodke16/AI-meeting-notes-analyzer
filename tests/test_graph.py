from src.graph import graph


def test_graph_with_action_items():

    state = {
        "transcript": """
        John: We need to improve the website performance.

        David: I will optimize the database queries
        immediately because the production server is slow.

        Sarah: I will redesign the homepage layout
        before Friday.

        John: Let's complete both tasks this week.
        """,

        "topics": [],
        "summary": "",
        "action_items": [],
        "has_action_items": False,
        "priorities": [],
        "final_report": {},
    }

    result = graph.invoke(state)

    print("\n========== FINAL REPORT ==========")

    print(result["final_report"])

    assert result["topics"]

    assert result["summary"]

    assert result["action_items"]

    assert result["has_action_items"] is True

    assert result["priorities"]

    assert result["final_report"]

    assert "summary" in result["final_report"]

    assert "topics" in result["final_report"]

    assert "action_items" in result["final_report"]

    assert "priorities" in result["final_report"]

    assert "task_owners" not in result["final_report"]


def test_graph_without_action_items():

    state = {
        "transcript": """
        John: Today's meeting was about the company's
        overall marketing strategy.

        Sarah: We discussed the current market trends
        and customer feedback.

        David: The team agreed that the current strategy
        is performing reasonably well.
        """,

        "topics": [],
        "summary": "",
        "action_items": [],
        "has_action_items": False,
        "priorities": [],
        "final_report": {},
    }

    result = graph.invoke(state)

    print("\n========== FINAL REPORT WITHOUT ACTION ITEMS ==========")

    print(result["final_report"])

    assert result["topics"]

    assert result["summary"]

    assert result["action_items"] == []

    assert result["has_action_items"] is False

    assert result["priorities"] == []

    assert (
        result["final_report"]["action_items"]
        == "No action items identified in this meeting."
    )

    assert (
        result["final_report"]["priorities"]
        == "No action items identified in this meeting."
    )

    assert "task_owners" not in result["final_report"]