"""Pydantic schemas for structured outputs"""

from pydantic import BaseModel, Field
from typing import List


class ResearchFinding(BaseModel):
    """A single research finding with source"""
    finding: str = Field(description="Key insight or finding from research")
    source_url: str = Field(description="URL of the source")
    relevance: str = Field(description="Why this finding matters for the topic")


class ResearchReport(BaseModel):
    """Complete research report structure"""
    topic: str = Field(description="The research topic")
    key_findings: List[ResearchFinding] = Field(
        description="3-5 key findings from research with sources",
        min_items=3,
        max_items=5
    )
    statistics: str = Field(description="Relevant statistics, market size, growth rates, etc.")
    expert_insights: str = Field(description="Expert opinions and professional perspectives")
    trends: str = Field(description="Current trends and future outlook")
    practical_takeaway: str = Field(description="Main actionable insight for professionals")


class LinkedInPost(BaseModel):
    """LinkedIn post structure"""
    hook: str = Field(description="Attention-grabbing opening (1-2 sentences)")
    context: str = Field(description="Why this matters now (2-3 sentences)")
    key_points: List[str] = Field(
        description="3-5 bullet points with insights",
        min_items=3,
        max_items=5
    )
    takeaway: str = Field(description="Practical 'so what' conclusion (1-2 sentences)")
    call_to_action: str = Field(description="Engagement question (1 sentence)")
    hashtags: List[str] = Field(
        description="3-5 relevant hashtags",
        min_items=3,
        max_items=5
    )
    
    def format_for_linkedin(self) -> str:
        """Format the post for LinkedIn"""
        post = f"{self.hook}\n\n"
        post += f"{self.context}\n\n"
        
        for point in self.key_points:
            post += f"• {point}\n\n"
        
        post += f"{self.takeaway}\n\n"
        post += f"{self.call_to_action}\n\n"
        post += " ".join(self.hashtags)
        
        return post

