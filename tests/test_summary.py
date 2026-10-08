from src.agents.summary_agent import summary_agent


def test_summary_agent():

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

    result = summary_agent(state)

    print("\nMeeting Summary:")
    print(result["summary"])

    assert result["summary"]
    assert len(result["summary"]) > 20