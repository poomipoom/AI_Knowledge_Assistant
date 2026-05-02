from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # Application Info
    PROJECT_NAME: str = "AI Knowledge Assistant"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "DEBUG"

    # Groq API
    GROQ_API_KEY: str
    GROQ_MODEL: str = "openai/gpt-oss-120b"

    # PostgreSQL
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    DATABASE_URL: str | None = None

    # Vector Search (Local HuggingFace embeddings)
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    def get_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

@lru_cache
def get_settings() -> Settings:
    return Settings()
