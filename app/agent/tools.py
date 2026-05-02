from sqlalchemy.orm import Session as DBSession
from app.db.vector_store import similarity_search
from app.core.config import get_settings
from sentence_transformers import SentenceTransformer
import json

settings = get_settings()
# Initialize local embedding model
embedder = SentenceTransformer(settings.EMBEDDING_MODEL)

async def retrieve_documents(db: DBSession, session_id: str, query: str, top_k: int = 5) -> str:
    """
    Tool function to retrieve relevant document chunks from the database.
    Returns a JSON string of results.
    """
    # 1. Embed query locally
    query_embedding = embedder.encode(query).tolist()
    
    # 2. Search in Vector DB
    results = similarity_search(db, session_id, query_embedding, top_k=top_k)
    
    # 3. Format results
    formatted_results = []
    for r in results:
        chunk = r["chunk"]
        formatted_results.append({
            "document_name": chunk.document.filename,
            "content": chunk.content,
            "distance": float(r["distance"]) if r["distance"] is not None else 0.0
        })
        
    return json.dumps(formatted_results, ensure_ascii=False)

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "retrieve_documents",
            "description": "ค้นหาข้อมูลจากเอกสารที่ผู้ใช้อัปโหลดใน session นี้ ใช้เมื่อผู้ใช้ถามคำถามที่เกี่ยวข้องกับเอกสาร (Search through user uploaded documents)",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "คำค้นหา (Search query)"
                    }
                },
                "required": ["query"]
            }
        }
    }
]
