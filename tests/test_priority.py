from src.agents.priority_agent import priority_agent


def test_priority_agent():

    state = {
        "transcript": "",
        "topics": [],
        "summary": "",
        "action_items": [
            {
                "task": "Fix the production server immediately",
                "owner": "David",
            },
            {
                "task": "Prepare the weekly performance report",
                "owner": "Sarah",
            },
            {
                "task": "Update the documentation when possible",
                "owner": "John",
            },
        ],
        "has_action_items": True,
        "priorities": [],
        "final_report": {},
    }

    result = priority_agent(state)

    print("\nPriority Results:")

    for item in result["priorities"]:
        print(item)

    assert len(result["priorities"]) == 3

    for item in result["priorities"]:
        assert "task" in item
        assert "owner" in item
        assert "priority" in item
        assert "reason" in item

        assert item["priority"] in [
            "High",
            "Medium",
            "Low",
        ]
def test_priority_agent_uses_original_transcript():
    state = {
        "transcript": (
            "David: I will optimize the database "
            "queries immediately.\n"
            "Sarah: I will redesign the homepage "
            "before Friday.\n"
            "John: We can update the documentation "
            "when possible."
        ),
        "topics": [],
        "summary": "",
        "action_items": [
            {
                "task": "Optimize the database queries",
                "owner": "David",
            },
            {
                "task": "Redesign the homepage before Friday",
                "owner": "Sarah",
            },
            {
                "task": "Update the documentation when possible",
                "owner": "John",
            },
        ],
        "has_action_items": True,
        "priorities": [],
        "final_report": {},
    }

    result = priority_agent(state)

    assert len(result["priorities"]) == 3

    priorities = {
        item["owner"]: item["priority"]
        for item in result["priorities"]
    }

    assert priorities["David"] == "High"
    assert priorities["Sarah"] == "Medium"
    assert priorities["John"] == "Low"