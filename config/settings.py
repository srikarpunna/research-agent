"""
Centralized configuration using Pydantic for validation.
Load all API keys and settings from environment variables.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API Keys
    google_api_key: str  # Gemini API key
    tavily_api_key: str
    firecrawl_api_key: str
    langsmith_api_key: str
    
    # LangSmith Configuration
    langsmith_project: str = "research-agent-production"
    langsmith_tracing: bool = True
    
    # Model Configuration
    llm_model: str = "gemini-1.5-flash"  # gemini-1.5-pro, gemini-1.5-flash (flash = faster + higher limits)
    llm_temperature: float = 0.7
    max_tokens: int = 4000
    
    # Research Configuration
    max_search_results: int = 5
    max_scrape_pages: int = 3
    research_depth: str = "comprehensive"  # quick, standard, comprehensive
    
    # Output Configuration
    linkedin_max_chars: int = 3000
    include_hashtags: bool = True
    num_hashtags: int = 5
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Singleton instance
settings = Settings()

