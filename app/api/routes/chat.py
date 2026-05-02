from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db_session
from app.schemas.chat import ChatMessageCreate, ChatAgentResponse
from app.services import chat_svc

router = APIRouter(prefix="/sessions/{session_id}/chat", tags=["Chat"])

@router.post("", response_model=ChatAgentResponse)
async def chat(
    session_id: str, 
    message: ChatMessageCreate, 
    db: Session = Depends(get_db_session)
):
    response = await chat_svc.chat_with_agent(db, session_id, message)
    return response
