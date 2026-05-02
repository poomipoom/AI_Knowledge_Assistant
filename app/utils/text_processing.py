import fitz  # PyMuPDF
from typing import List

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    with fitz.open("pdf", file_bytes) as doc:
        for page in doc:
            text += page.get_text() + "\n"
    return text

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Simple chunking strategy by character count with overlap.
    """
    if not text:
        return []
    
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)
        
    return chunks
