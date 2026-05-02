from sqlalchemy.orm import Session as DBSession
from app.db.models import Session
from app.schemas.session import SessionCreate
from app.core.exceptions import NotFoundException
from typing import List

def create_session(db: DBSession, session_data: SessionCreate) -> Session:
    new_session = Session(title=session_data.title)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

def get_session(db: DBSession, session_id: str) -> Session:
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        raise NotFoundException(item_name="Session")
    return session

def get_all_sessions(db: DBSession) -> List[Session]:
    return db.query(Session).order_by(Session.created_at.desc()).all()

def delete_session(db: DBSession, session_id: str):
    session = get_session(db, session_id)
    db.delete(session)
    db.commit()
    return {"message": "Session deleted successfully"}

def update_session(db: DBSession, session_id: str, title: str) -> Session:
    session = get_session(db, session_id)
    session.title = title
    db.commit()
    db.refresh(session)
    return session
