"""
FireCrawl scraping tool wrapper.
Handles JavaScript rendering, anti-bot measures, and returns clean text.
"""

from langchain.tools import Tool
import requests
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class ResearchScrapeTool:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.firecrawl.dev/v0/scrape"
    
    def scrape(self, url: str) -> str:
        """
        Scrape a URL and return clean, markdown-formatted content.
        
        Args:
            url: The URL to scrape
            
        Returns:
            Clean text content of the page
        """
        try:
            logger.info(f"Scraping URL: {url}")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "url": url,
                "formats": ["markdown"],
                "onlyMainContent": True
            }
            
            response = requests.post(
                self.base_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            content = data.get("data", {}).get("markdown", "")
            
            logger.info(f"Successfully scraped {len(content)} characters")
            return content
            
        except Exception as e:
            logger.error(f"Scraping failed for {url}: {str(e)}")
            return f"Error scraping {url}: {str(e)}"
    
    def as_langchain_tool(self) -> Tool:
        """Return as LangChain Tool for agent use"""
        return Tool(
            name="scrape_webpage",
            description=(
                "Extract the full text content from a specific webpage URL. "
                "Returns clean, readable text without HTML. "
                "Use this after finding relevant URLs with web_search to get detailed information. "
                "Input should be a valid HTTP/HTTPS URL."
            ),
            func=self.scrape
        )

