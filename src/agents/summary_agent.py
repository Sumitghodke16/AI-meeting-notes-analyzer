import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from src.state import MeetingState
from src.agents.schemas import MeetingSummary


load_dotenv()


def summary_agent(state: MeetingState) -> MeetingState:
    """
    Generate a concise summary of the meeting transcript.
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )

    structured_llm = llm.with_structured_output(MeetingSummary)

    prompt = f"""
You are a professional meeting summarization AI agent.

Summarize the following meeting transcript.

Requirements:
- Write 3 to 5 concise sentences.
- Explain what the meeting was mainly about.
- Include important decisions or outcomes.
- Mention important deadlines when present.
- Do not invent information.
- Do not list action items separately.
- Use professional business language.

Meeting Transcript:

{state["transcript"]}
"""

    result = structured_llm.invoke(prompt)

    state["summary"] = result.summary

    return state