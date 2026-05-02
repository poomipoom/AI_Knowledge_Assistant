from sqlalchemy.orm import Session as DBSession
from typing import List
from sqlalchemy import select
from app.db.models import DocumentChunk, Document

def save_chunks(db: DBSession, document_id: str, chunks_data: List[dict]):
    """
    chunks_data is a list of dicts: {"content": "...", "embedding": [...], "chunk_index": 0}
    """
    db_chunks = []
    for data in chunks_data:
        chunk = DocumentChunk(
            document_id=document_id,
            content=data["content"],
            embedding=data["embedding"],
            chunk_index=data["chunk_index"]
        )
        db_chunks.append(chunk)
    
    db.add_all(db_chunks)
    db.commit()

def similarity_search(db: DBSession, session_id: str, query_embedding: List[float], top_k: int = 5):
    """
    Perform a similarity search using pgvector's cosine distance (`<=>`)
    We filter by session_id by joining with Document.
    """
    stmt = (
        select(DocumentChunk, DocumentChunk.embedding.cosine_distance(query_embedding).label('distance'))
        .join(Document)
        .where(Document.session_id == session_id)
        .order_by('distance')
        .limit(top_k)
    )
    
    results = db.execute(stmt).all()
    
    return [{"chunk": row[0], "distance": row[1]} for row in results]
