import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from src.state import MeetingState
from src.agents.schemas import PriorityClassification


load_dotenv()


def priority_agent(state: MeetingState) -> MeetingState:
    """
    Classify the priority of each meeting action item.

    Priority is determined using both:
    1. Extracted action items
    2. Original meeting transcript

    Using the original transcript prevents important urgency
    or deadline information from being lost between agents.
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )

    structured_llm = llm.with_structured_output(
        PriorityClassification
    )

    action_items_text = "\n".join(
        [
            (
                f"Task: {item['task']}\n"
                f"Owner: {item['owner']}"
            )
            for item in state["action_items"]
        ]
    )

    prompt = f"""
You are a professional meeting priority classification AI agent.

Your task is to classify the priority of every extracted
meeting action item.

You have TWO sources of information:

1. Original Meeting Transcript
2. Extracted Action Items

Use the original transcript to verify urgency, deadlines,
and business context before assigning priority.

Allowed priority levels:

- High
- Medium
- Low


HIGH PRIORITY:

Use High when the meeting explicitly indicates:

- immediately
- ASAP
- urgent
- critical
- production issue
- security issue
- severe issue
- today
- by tomorrow
- must be completed immediately
- a very close explicit deadline


MEDIUM PRIORITY:

Use Medium for:

- important tasks
- near-term tasks
- tasks due this week
- tasks with a normal upcoming deadline
- tasks that matter but are not explicitly urgent


LOW PRIORITY:

Use Low for:

- future improvements
- optional improvements
- nice-to-have tasks
- tasks without urgency
- tasks without an immediate deadline


IMPORTANT RULES:

1. Do NOT invent urgency.

2. Do NOT invent deadlines.

3. Do NOT change the priority based on assumptions.

4. If the original transcript contains an explicit urgency
   word such as "immediately", "ASAP", or "urgent", respect it.

5. If the extracted action item accidentally omits urgency
   but the original transcript clearly contains it, use the
   original transcript as the source of truth.

6. Return exactly one classification for every action item.

7. Priority must be exactly one of:
   High, Medium, Low.

8. Keep the reason concise and explain the evidence from
   the meeting.

ORIGINAL MEETING TRANSCRIPT:

{state["transcript"]}


EXTRACTED ACTION ITEMS:

{action_items_text}
"""

    result = structured_llm.invoke(prompt)

    state["priorities"] = [
        {
            "task": item.task,
            "owner": item.owner,
            "priority": item.priority,
            "reason": item.reason,
        }
        for item in result.priorities
    ]

    return state