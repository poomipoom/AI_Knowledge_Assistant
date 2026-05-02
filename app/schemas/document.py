from pydantic import BaseModel
from datetime import datetime

class DocumentResponse(BaseModel):
    id: str
    session_id: str
    filename: str
    created_at: datetime
    
    class Config:
        from_attributes = True
