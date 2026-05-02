from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db_session
from app.schemas.session import SessionCreate, SessionUpdate, SessionResponse, SessionDetailResponse
from app.services import session_svc

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("", response_model=SessionResponse)
def create_session(session_data: SessionCreate, db: Session = Depends(get_db_session)):
    return session_svc.create_session(db, session_data)

@router.get("", response_model=List[SessionResponse])
def get_all_sessions(db: Session = Depends(get_db_session)):
    return session_svc.get_all_sessions(db)

@router.get("/{session_id}", response_model=SessionDetailResponse)
def get_session(session_id: str, db: Session = Depends(get_db_session)):
    return session_svc.get_session(db, session_id)

@router.delete("/{session_id}")
def delete_session(session_id: str, db: Session = Depends(get_db_session)):
    return session_svc.delete_session(db, session_id)

@router.put("/{session_id}", response_model=SessionResponse)
def update_session(session_id: str, session_data: SessionUpdate, db: Session = Depends(get_db_session)):
    return session_svc.update_session(db, session_id, session_data.title)
