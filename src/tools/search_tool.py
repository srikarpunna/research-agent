"""
Tavily search tool wrapper.
Returns AI-optimized, clean search results without HTML noise.
"""

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import Tool
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class ResearchSearchTool:
    def __init__(self, api_key: str, max_results: int = 5):
        self.api_key = api_key
        self.max_results = max_results
        self.tavily = TavilySearchResults(
            tavily_api_key=api_key,
            max_results=max_results
        )
    
    def search(self, query: str) -> List[Dict]:
        """
        Execute search and return structured results.
        
        Returns:
            List of dicts with 'title', 'url', 'content', 'score'
        """
        try:
            logger.info(f"Executing Tavily search: {query}")
            results = self.tavily.invoke({"query": query})
            logger.info(f"Found {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            raise
    
    def as_langchain_tool(self) -> Tool:
        """Return as LangChain Tool for agent use"""
        return Tool(
            name="web_search",
            description=(
                "Search the web for current information on any topic. "
                "Returns clean, AI-optimized summaries of the most relevant sources. "
                "Use this to find recent articles, research papers, and expert opinions. "
                "Input should be a clear, specific search query."
            ),
            func=self.search
        )

