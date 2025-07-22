from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import init_chat_model
from langchain_core.tracers import LangChainTracer

from app.memory.redis_memory import get_memory
from app.utils.search_utils import search_chunks
from app.core.config import settings
import os

tracer = LangChainTracer()

os.environ['GOOGLE_API_KEY'] = settings.GOOGLE_API_KEY


model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

def get_agent(session_id:str):
    memory = get_memory(session_id)
    tools = [search_chunks]

    agent = initialize_agent(
        tools,
        model,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory,
        callbacks=[tracer] 
    )

    return agent