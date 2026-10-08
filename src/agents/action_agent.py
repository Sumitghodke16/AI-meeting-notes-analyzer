import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from src.state import MeetingState
from src.agents.schemas import ActionItemExtraction


load_dotenv()


def action_agent(state: MeetingState) -> MeetingState:
    """
    Extract action items and explicitly assigned owners.

    The agent must preserve important urgency and deadline
    language because downstream priority classification depends
    on this information.
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )

    structured_llm = llm.with_structured_output(
        ActionItemExtraction
    )

    prompt = f"""
You are a professional meeting action-item extraction AI agent.

Analyze the following meeting transcript and identify every
action item or task that someone is expected to complete.

For every action item:

1. Extract the specific task.

2. Identify the person responsible ONLY when the transcript
   explicitly assigns the task to that person.

3. Do NOT assume that a speaker owns a task merely because
   they mention, discuss, suggest, or ask about the task.

4. If no person is explicitly assigned responsibility,
   use "Not specified".

IMPORTANT URGENCY AND DEADLINE RULE:

Preserve explicit urgency and deadline information from the
original transcript in the task description.

Examples of information that MUST be preserved when relevant:

- immediately
- ASAP
- urgent
- critical
- today
- tomorrow
- before Friday
- by Friday
- this week
- next week
- by the next meeting

Do NOT replace or weaken urgency language.

For example:

Original:
"David: I will optimize the database queries immediately."

Good:
"Optimize the database queries immediately"

Bad:
"Optimize the database queries"

Bad:
"Optimize the database queries before Friday"
unless "before Friday" was actually stated as the task deadline.

Rules:
- Do not invent tasks.
- Do not invent owners.
- Do not invent deadlines.
- Do not invent urgency.
- Include only genuine action items.
- Statements describing past work are not action items.
- Keep task descriptions concise.
- Preserve explicit urgency and deadline wording.

Meeting Transcript:

{state["transcript"]}
"""

    result = structured_llm.invoke(prompt)

    state["action_items"] = [
        {
            "task": item.task,
            "owner": item.owner,
        }
        for item in result.action_items
    ]

    state["has_action_items"] = (
        len(state["action_items"]) > 0
    )

    return state