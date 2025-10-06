"""
Unit tests for research tools.
Run with: pytest tests/test_tools.py
"""

import pytest
from unittest.mock import Mock, patch
from src.tools.search_tool import ResearchSearchTool
from src.tools.scrape_tool import ResearchScrapeTool


class TestResearchSearchTool:
    """Tests for Tavily search tool"""
    
    def test_initialization(self):
        """Test tool initialization"""
        tool = ResearchSearchTool(api_key="test-key", max_results=3)
        assert tool is not None
        assert tool.tavily is not None
    
    def test_as_langchain_tool(self):
        """Test LangChain tool conversion"""
        tool = ResearchSearchTool(api_key="test-key")
        langchain_tool = tool.as_langchain_tool()
        
        assert langchain_tool.name == "web_search"
        assert "search" in langchain_tool.description.lower()
        assert callable(langchain_tool.func)
    
    @patch('src.tools.search_tool.TavilySearchResults')
    def test_search_success(self, mock_tavily):
        """Test successful search"""
        mock_instance = Mock()
        mock_instance.invoke.return_value = [
            {"title": "Test", "url": "https://example.com", "content": "Test content"}
        ]
        mock_tavily.return_value = mock_instance
        
        tool = ResearchSearchTool(api_key="test-key")
        results = tool.search("test query")
        
        assert len(results) == 1
        assert results[0]["title"] == "Test"


class TestResearchScrapeTool:
    """Tests for FireCrawl scraping tool"""
    
    def test_initialization(self):
        """Test tool initialization"""
        tool = ResearchScrapeTool(api_key="test-key")
        assert tool is not None
        assert tool.api_key == "test-key"
        assert tool.base_url == "https://api.firecrawl.dev/v0/scrape"
    
    def test_as_langchain_tool(self):
        """Test LangChain tool conversion"""
        tool = ResearchScrapeTool(api_key="test-key")
        langchain_tool = tool.as_langchain_tool()
        
        assert langchain_tool.name == "scrape_webpage"
        assert "scrape" in langchain_tool.description.lower()
        assert callable(langchain_tool.func)
    
    @patch('src.tools.scrape_tool.requests.post')
    def test_scrape_success(self, mock_post):
        """Test successful scraping"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": {"markdown": "# Test Content\n\nThis is test content."}
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        tool = ResearchScrapeTool(api_key="test-key")
        content = tool.scrape("https://example.com")
        
        assert "Test Content" in content
        assert len(content) > 0
    
    @patch('src.tools.scrape_tool.requests.post')
    def test_scrape_failure(self, mock_post):
        """Test scraping failure handling"""
        mock_post.side_effect = Exception("Network error")
        
        tool = ResearchScrapeTool(api_key="test-key")
        content = tool.scrape("https://example.com")
        
        assert "Error scraping" in content
        assert "https://example.com" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

