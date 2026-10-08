from src.agents.action_agent import action_agent


def test_action_agent():

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

    result = action_agent(state)

    print("\nAction Items:")
    print(result["action_items"])

    assert len(result["action_items"]) > 0
    assert result["has_action_items"] is True

    for item in result["action_items"]:
        assert "task" in item
        assert "owner" in item


def test_action_agent_without_owner():

    state = {
        "transcript": """
        John: The website security needs improvement.
        Sarah: We discussed reviewing the authentication system.
        John: This needs to be completed by Friday.
        """,
        "topics": [],
        "summary": "",
        "action_items": [],
        "has_action_items": False,
        "priorities": [],
        "final_report": {},
    }

    result = action_agent(state)

    print("\nAction Items Without Explicit Owner:")
    print(result["action_items"])

    assert len(result["action_items"]) > 0
    assert result["has_action_items"] is True

    for item in result["action_items"]:
        assert "task" in item
        assert "owner" in item

        assert item["owner"].lower() in [
            "not specified",
            "owner: not specified",
        ]

def test_action_agent_preserves_urgency():
    state = {
        "transcript": (
            "David: I will optimize the database "
            "queries immediately."
        ),
        "topics": [],
        "summary": "",
        "action_items": [],
        "has_action_items": False,
        "priorities": [],
        "final_report": {},
    }

    result = action_agent(state)

    assert result["has_action_items"] is True
    assert len(result["action_items"]) == 1

    task = result["action_items"][0]["task"].lower()

    assert (
        "immediately" in task
        or "immediate" in task
    )