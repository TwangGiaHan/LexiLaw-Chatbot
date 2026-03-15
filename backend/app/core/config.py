from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra="ignore")

    # App
    APP_NAME: str = "Legal Labor RAG Chatbot"
    DEBUG: bool = False

    # Qdrant Cloud
    QDRANT_URL: str
    QDRANT_API_KEY: Optional[str] = None
    COLLECTION_NAME: str = "legal_laws"

    # OpenAi LLM
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = 'gpt-4o-mini'


    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    # REDIS_URL: str = "redis://redis:6379/0"

    # # Neo4j (GraphRAG)
    NEO4J_URI: str
    NEO4J_USERNAME: str
    NEO4J_PASSWORD: str
    NEO4J_DATABASE: str
    AURA_INSTANCEID: str
    AURA_INSTANCENAME: str


    VECTOR_SEARCH_TOP_K: int = 10
    ALLOW_ORIGINS: str = '*'

    COHERE_API_KEY: str

settings = Settings()