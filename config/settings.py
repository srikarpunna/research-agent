"""
Centralized configuration using Pydantic for validation.
Load all API keys and settings from environment variables or Streamlit secrets.
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os

# Try to import streamlit for secrets support
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False


class Settings(BaseSettings):
    # API Keys
    google_api_key: str  # Gemini API key
    tavily_api_key: str
    firecrawl_api_key: str
    langsmith_api_key: Optional[str] = None

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


def load_settings():
    """Load settings from Streamlit secrets if available, otherwise from .env"""
    if HAS_STREAMLIT and hasattr(st, 'secrets'):
        # Check if we have secrets without triggering an error
        try:
            # Try to access a secret to see if secrets are configured
            if "GOOGLE_API_KEY" in st.secrets:
                # Running in Streamlit Cloud - use secrets
                return Settings(
                    google_api_key=st.secrets.get("GOOGLE_API_KEY", ""),
                    tavily_api_key=st.secrets.get("TAVILY_API_KEY", ""),
                    firecrawl_api_key=st.secrets.get("FIRECRAWL_API_KEY", ""),
                    langsmith_api_key=st.secrets.get("LANGSMITH_API_KEY"),
                    langsmith_project=st.secrets.get("LANGSMITH_PROJECT", "research-agent-production"),
                    langsmith_tracing=st.secrets.get("LANGSMITH_TRACING", "true").lower() == "true",
                    llm_model=st.secrets.get("LLM_MODEL", "gemini-1.5-flash"),
                    llm_temperature=float(st.secrets.get("LLM_TEMPERATURE", "0.7")),
                    max_tokens=int(st.secrets.get("MAX_TOKENS", "4000")),
                    max_search_results=int(st.secrets.get("MAX_SEARCH_RESULTS", "5")),
                    max_scrape_pages=int(st.secrets.get("MAX_SCRAPE_PAGES", "3")),
                    research_depth=st.secrets.get("RESEARCH_DEPTH", "comprehensive"),
                    linkedin_max_chars=int(st.secrets.get("LINKEDIN_MAX_CHARS", "3000")),
                    include_hashtags=st.secrets.get("INCLUDE_HASHTAGS", "true").lower() == "true",
                    num_hashtags=int(st.secrets.get("NUM_HASHTAGS", "5"))
                )
        except:
            # No secrets configured, fall through to .env
            pass

    # Running locally - use .env file
    return Settings()


# Singleton instance
settings = load_settings()

