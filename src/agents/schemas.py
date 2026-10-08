from pydantic import BaseModel, Field


# --------------------------------------------------
# Topic Extraction
# --------------------------------------------------

class TopicExtraction(BaseModel):
    topics: list[str] = Field(
        description="A list of the main discussion topics from the meeting."
    )


# --------------------------------------------------
# Meeting Summary
# --------------------------------------------------

class MeetingSummary(BaseModel):
    summary: str = Field(
        description="A concise 3 to 5 sentence summary of the meeting."
    )


# --------------------------------------------------
# Action Item
# --------------------------------------------------

class ActionItem(BaseModel):
    task: str = Field(
        description="The specific task that needs to be completed."
    )

    owner: str = Field(
        description=(
            "The person responsible for the task. "
            "Use 'Not specified' if no owner is explicitly assigned."
        )
    )


# --------------------------------------------------
# Action Item Extraction
# --------------------------------------------------

class ActionItemExtraction(BaseModel):
    action_items: list[ActionItem] = Field(
        description="List of action items identified in the meeting."
    )


# --------------------------------------------------
# Task Priority
# --------------------------------------------------

class TaskPriority(BaseModel):
    task: str = Field(
        description="The action item being classified."
    )

    owner: str = Field(
        description="The owner of the action item."
    )

    priority: str = Field(
        description="Priority level: High, Medium, or Low."
    )

    reason: str = Field(
        description="Short explanation for why this priority was assigned."
    )


# --------------------------------------------------
# Priority Classification
# --------------------------------------------------

class PriorityClassification(BaseModel):
    priorities: list[TaskPriority] = Field(
        description="Priority classification for each action item."
    )


# --------------------------------------------------
# Final Report
# --------------------------------------------------

class FinalReport(BaseModel):
    summary: str = Field(
        description="Concise summary of the meeting."
    )

    topics: list[str] = Field(
        description="Main discussion topics from the meeting."
    )

    action_items: list[ActionItem] | str = Field(
        description=(
            "List of action items with their owners, "
            "or a message stating that no action items "
            "were identified."
        )
    )

    priorities: list[TaskPriority] | str = Field(
        description=(
            "Priority classifications for the action items, "
            "or a message stating that no action items "
            "were identified."
        )
    )