from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, ConfigDict
from typing import List, Optional


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", case_sensitive=False)

    # App
    APP_ENV: str = "development"
    API_BASE_URL: AnyHttpUrl | str = "http://localhost:8000"
    CORS_ORIGINS: List[str] = ["*"]

    # Deepgram STT
    DEEPGRAM_API_KEY: Optional[str] = None

    # OpenAI (GPT + TTS)
    OPENAI_API_KEY: Optional[str] = None

    # LangChain (for future async LLM integration)
    LANGCHAIN_ENABLED: bool = False


settings = Settings()
