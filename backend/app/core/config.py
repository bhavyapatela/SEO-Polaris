import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "SEO Polaris"
    API_V1_STR: str = "/api/v1"
    
    # Use SQLite locally by default, override with DATABASE_URL in production
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./seo_polaris.db")
    
    class Config:
        case_sensitive = True

settings = Settings()
