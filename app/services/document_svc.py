import asyncio
from sqlalchemy.orm import Session as DBSession
from fastapi import UploadFile
from app.db.models import Document
from app.utils.text_processing import extract_text_from_pdf, chunk_text
from app.db.vector_store import save_chunks
from app.services.session_svc import get_session
from app.core.exceptions import DocumentProcessingError
from app.core.logger import logger
from app.core.config import get_settings
from sentence_transformers import SentenceTransformer

settings = get_settings()
# Initialize local embedding model
embedder = SentenceTransformer(settings.EMBEDDING_MODEL)

async def process_and_save_document(db: DBSession, session_id: str, file: UploadFile):
    # Ensure session exists
    get_session(db, session_id)
    
    # 1. Create Document metadata
    doc = Document(session_id=session_id, filename=file.filename)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    try:
        # 2. Extract text
        file_bytes = await file.read()
        text = extract_text_from_pdf(file_bytes)
        
        # 3. Chunk text
        chunks = chunk_text(text)
        logger.info(f"Extracted {len(chunks)} chunks from {file.filename}")
        
        # 4. Generate Embeddings (Local processing using SentenceTransformers)
        chunks_data = []
        
        # Encode all chunks at once for better performance
        embeddings = embedder.encode(chunks)
        
        for i, (chunk_text_content, embedding) in enumerate(zip(chunks, embeddings)):
            chunks_data.append({
                "content": chunk_text_content,
                "embedding": embedding.tolist(),
                "chunk_index": i
            })
            
        # 5. Save to Vector Store
        save_chunks(db, doc.id, chunks_data)
        
        return doc
        
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        # Rollback document creation if processing fails
        db.delete(doc)
        db.commit()
        raise DocumentProcessingError(detail=f"Failed to process document: {str(e)}")
