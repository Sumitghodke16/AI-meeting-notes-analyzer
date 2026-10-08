import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from src.state import MeetingState
from src.agents.schemas import TopicExtraction


load_dotenv()


def topic_agent(state: MeetingState) -> MeetingState:
    """
    Extract the main discussion topics from the meeting transcript.
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )

    structured_llm = llm.with_structured_output(TopicExtraction)

    prompt = f"""
You are a meeting analysis AI agent.

Analyze the following meeting transcript and identify
the main discussion topics.

Rules:
- Extract only meaningful discussion topics.
- Avoid duplicate topics.
- Do not include individual tasks as topics unless
  they represent an important discussion area.
- Return between 2 and 7 topics.
- Keep each topic concise.

Meeting Transcript:

{state["transcript"]}
"""

    result = structured_llm.invoke(prompt)

    state["topics"] = result.topics

    return state