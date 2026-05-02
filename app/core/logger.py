import logging
from app.core.config import get_settings

settings = get_settings()

def setup_logging():
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger("rag_chatbot")
    return logger

logger = setup_logging()
