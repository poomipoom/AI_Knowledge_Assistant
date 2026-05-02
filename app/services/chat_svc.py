from sqlalchemy.orm import Session as DBSession
from app.db.models import ChatMessage, ChatRole
from app.schemas.chat import ChatMessageCreate
from app.services.session_svc import get_session

async def chat_with_agent(db: DBSession, session_id: str, message: ChatMessageCreate):
    # Ensure session exists
    get_session(db, session_id)
    
    # 1. Save user message
    user_msg = ChatMessage(
        session_id=session_id,
        role=ChatRole.user,
        content=message.content
    )
    db.add(user_msg)
    db.commit()
    
    # 2. Invoke Agent
    from app.agent.orchestrator import run_agent_loop
    agent_response = await run_agent_loop(db, session_id, message.content)
    
    # 3. Save assistant message
    assistant_msg = ChatMessage(
        session_id=session_id,
        role=ChatRole.assistant,
        content=agent_response["content"]
    )
    db.add(assistant_msg)
    db.commit()
    db.refresh(assistant_msg)
    
    return {
        "message": assistant_msg,
        "citations": agent_response.get("citations", [])
    }
