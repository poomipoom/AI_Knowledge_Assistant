from pydantic import BaseModel
from datetime import datetime
from typing import List
from app.db.models import ChatRole

class ChatMessageCreate(BaseModel):
    content: str

class ChatMessageResponse(BaseModel):
    id: str
    session_id: str
    role: ChatRole
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Citation(BaseModel):
    document_name: str
    content: str

class ChatAgentResponse(BaseModel):
    message: ChatMessageResponse
    citations: List[Citation] = []
