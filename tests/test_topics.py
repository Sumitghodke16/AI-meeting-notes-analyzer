from src.agents.topic_agent import topic_agent


def test_topic_agent():

    state = {
        "transcript": """
        John: We need to improve the website performance.
        Sarah: Page load time is too slow.
        David: I will optimize the database queries this week.
        Sarah: I will redesign the homepage layout.
        John: Let's finish these tasks before Friday.
        """,
        "topics": [],
        "summary": "",
        "action_items": [],
        "has_action_items": False,
        "priorities": [],
        "final_report": {},
    }

    result = topic_agent(state)

    print("\nExtracted Topics:")
    print(result["topics"])

    assert len(result["topics"]) > 0