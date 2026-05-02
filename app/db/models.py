from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.db.database import Base
from app.core.config import get_settings
import uuid
import enum

settings = get_settings()

class ChatRole(enum.Enum):
    user = "user"
    assistant = "assistant"

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    title = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    documents = relationship("Document", back_populates="session", cascade="all, delete-orphan")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    session_id = Column(String, ForeignKey("sessions.id"))
    filename = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    session = relationship("Session", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    document_id = Column(String, ForeignKey("documents.id"))
    content = Column(Text)
    embedding = Column(Vector(settings.EMBEDDING_DIMENSION))
    chunk_index = Column(Integer)
    
    document = relationship("Document", back_populates="chunks")


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    session_id = Column(String, ForeignKey("sessions.id"))
    role = Column(Enum(ChatRole))
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    session = relationship("Session", back_populates="messages")
