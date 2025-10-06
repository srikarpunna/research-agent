"""
Integration tests for research workflow.
Run with: pytest tests/test_workflow.py
"""

import pytest
from unittest.mock import Mock, patch
from src.utils.validators import validate_topic, validate_linkedin_post


class TestValidators:
    """Tests for validation utilities"""
    
    def test_validate_topic_success(self):
        """Test valid topic"""
        validate_topic("AI Agent Frameworks")  # Should not raise
    
    def test_validate_topic_empty(self):
        """Test empty topic raises error"""
        with pytest.raises(ValueError, match="cannot be empty"):
            validate_topic("")
    
    def test_validate_topic_too_short(self):
        """Test too short topic raises error"""
        with pytest.raises(ValueError, match="too short"):
            validate_topic("AI")
    
    def test_validate_topic_too_long(self):
        """Test too long topic raises error"""
        long_topic = "A" * 201
        with pytest.raises(ValueError, match="too long"):
            validate_topic(long_topic)
    
    def test_validate_linkedin_post_valid(self):
        """Test valid LinkedIn post"""
        post = """
AI is transforming how we work.

Here are 3 key trends:
• Trend 1
• Trend 2  
• Trend 3

What do you think?

#AI #Technology #Future
"""
        result = validate_linkedin_post(post)
        assert result["valid"] == True
        assert len(result["warnings"]) == 0
        assert result["stats"]["hashtags"] == 3
    
    def test_validate_linkedin_post_too_short(self):
        """Test post that's too short"""
        post = "Short post"
        result = validate_linkedin_post(post)
        
        assert result["valid"] == False
        assert any("too short" in w.lower() for w in result["warnings"])
    
    def test_validate_linkedin_post_no_hashtags(self):
        """Test post without hashtags"""
        post = "A" * 500  # Valid length but no hashtags
        result = validate_linkedin_post(post)
        
        assert result["valid"] == False
        assert any("hashtag" in w.lower() for w in result["warnings"])
    
    def test_validate_linkedin_post_markdown_headers(self):
        """Test post with markdown headers (invalid for LinkedIn)"""
        post = """
# This is a header

Some content here with enough length to pass the length check.
This needs to be long enough to avoid the short warning.

#Hashtag1 #Hashtag2
"""
        result = validate_linkedin_post(post)
        
        assert result["valid"] == False
        assert any("markdown" in w.lower() for w in result["warnings"])


class TestWorkflowComponents:
    """Tests for workflow components"""
    
    def test_research_prompt_contains_key_instructions(self):
        """Test research prompt has key instructions"""
        from src.prompts.research_prompts import RESEARCHER_SYSTEM_PROMPT, RESEARCH_TASK_TEMPLATE
        
        assert "Research" in RESEARCHER_SYSTEM_PROMPT
        assert "Senior Research Analyst" in RESEARCHER_SYSTEM_PROMPT
        assert "{topic}" in RESEARCH_TASK_TEMPLATE
    
    def test_writer_prompt_contains_linkedin_guidelines(self):
        """Test writer prompt has LinkedIn guidelines"""
        from src.prompts.writer_prompts import WRITER_SYSTEM_PROMPT, WRITER_TASK_TEMPLATE
        
        assert "LinkedIn" in WRITER_SYSTEM_PROMPT
        assert "Hook" in WRITER_SYSTEM_PROMPT
        assert "Hashtag" in WRITER_SYSTEM_PROMPT
        assert "{research_report}" in WRITER_TASK_TEMPLATE
        assert "{topic}" in WRITER_TASK_TEMPLATE


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

