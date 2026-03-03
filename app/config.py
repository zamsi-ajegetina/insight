import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuration settings loaded from environment variables."""
    # API Keys
    GROQ_API_KEY: str = ""

    # Models
    LLM_MODEL: str = "llama-3.1-8b-instant"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # Paths
    PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
    CHROMA_PERSIST_DIR: str = str(PROJECT_ROOT / "vectorstore")
    CORPUS_DIR: str = str(PROJECT_ROOT / "corpus")

    # Retrieval and Generation defaults
    RETRIEVAL_TOP_K: int = 7
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 100
    MAX_OUTPUT_TOKENS: int = 2048

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore" # Ignore extra env vars not defined here

settings = Settings()
