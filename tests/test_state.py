from src.state import MeetingState


def test_meeting_state():

    state: MeetingState = {
        "transcript": "John: We need to improve the website.",
        "topics": [],
        "summary": "",
        "action_items": [],
        "has_action_items": False,
        "priorities": [],
        "final_report": {},
    }

    assert state["transcript"] != ""
    assert state["topics"] == []
    assert state["action_items"] == []
    assert state["has_action_items"] is False


if __name__ == "__main__":
    test_meeting_state()
    print("MeetingState test passed!")