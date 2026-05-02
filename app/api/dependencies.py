from fastapi import Depends
from app.db.database import get_db
from sqlalchemy.orm import Session

def get_db_session(db: Session = Depends(get_db)):
    return db
