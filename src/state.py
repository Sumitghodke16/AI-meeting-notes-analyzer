from typing import TypedDict


class MeetingState(TypedDict):
    transcript: str
    topics: list[str]
    summary: str
    action_items: list[dict]
    has_action_items: bool
    priorities: list[dict]
    final_report: dict