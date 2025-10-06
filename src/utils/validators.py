"""Input and output validation"""

import re
from typing import Dict, List


def validate_topic(topic: str) -> None:
    """Validate research topic input"""
    if not topic or not topic.strip():
        raise ValueError("Topic cannot be empty")
    
    if len(topic) < 3:
        raise ValueError("Topic too short (minimum 3 characters)")
    
    if len(topic) > 200:
        raise ValueError("Topic too long (maximum 200 characters)")


def validate_linkedin_post(post: str) -> Dict[str, any]:
    """
    Validate LinkedIn post meets platform requirements.
    
    Returns:
        dict with 'valid', 'warnings', and 'stats' keys
    """
    
    warnings = []
    
    # Length check
    length = len(post)
    if length < 100:
        warnings.append("Post might be too short (< 100 chars)")
    elif length > 3000:
        warnings.append("Post exceeds recommended length (> 3000 chars)")
    
    # Hashtag check
    hashtags = re.findall(r'#\w+', post)
    if len(hashtags) == 0:
        warnings.append("No hashtags found")
    elif len(hashtags) > 10:
        warnings.append(f"Too many hashtags ({len(hashtags)}), optimal is 3-5")
    
    # Paragraph check (should have line breaks)
    paragraphs = post.split('\n\n')
    if len(paragraphs) < 3:
        warnings.append("Consider adding more line breaks for readability")
    
    # Check for markdown headers (don't work on LinkedIn)
    if re.search(r'^#{1,6}\s', post, re.MULTILINE):
        warnings.append("Contains markdown headers (# ##) which won't render on LinkedIn")
    
    return {
        "valid": len(warnings) == 0,
        "warnings": warnings,
        "stats": {
            "length": length,
            "paragraphs": len(paragraphs),
            "hashtags": len(hashtags)
        }
    }

