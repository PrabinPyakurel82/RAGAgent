from fastapi.routing import APIRouter
from pydantic import BaseModel

from app.agent.rag_agent import get_agent

router = APIRouter()

class QueryRequest(BaseModel):
    session_id: str
    question: str

@router.post("/agent/")
def query_agent(request:QueryRequest):
    agent = get_agent(session_id=request.session_id)
    answer = agent.invoke(request.question)
    return {"answer":answer}

import uuid

@router.post("/start-session/")
def start_session():
    session_id = str(uuid.uuid4())
    return {"session_id": session_id}