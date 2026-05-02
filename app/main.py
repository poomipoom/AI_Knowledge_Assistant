from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import session, document, chat
from app.core.config import get_settings
from app.db.database import engine, Base

settings = get_settings()

# Create tables for now
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(session.router)
app.include_router(document.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "Welcome to the AI Knowledge Assistant API. Visit /docs for the Swagger UI."}
