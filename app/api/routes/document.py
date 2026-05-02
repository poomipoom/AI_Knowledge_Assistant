from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.api.dependencies import get_db_session
from app.schemas.document import DocumentResponse
from app.services import document_svc

router = APIRouter(prefix="/sessions/{session_id}/documents", tags=["Documents"])

@router.post("", response_model=DocumentResponse)
async def upload_document(
    session_id: str, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db_session)
):
    doc = await document_svc.process_and_save_document(db, session_id, file)
    return doc
