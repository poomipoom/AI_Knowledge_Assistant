from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .document import DocumentResponse
from .chat import ChatMessageResponse

class SessionCreate(BaseModel):
    title: Optional[str] = "New Session"

class SessionUpdate(BaseModel):
    title: str

class SessionResponse(BaseModel):
    id: str
    title: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class SessionDetailResponse(SessionResponse):
    documents: List[DocumentResponse] = []
    messages: List[ChatMessageResponse] = []
