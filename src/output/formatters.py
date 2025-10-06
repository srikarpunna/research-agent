"""Output formatting utilities for LinkedIn content"""

from typing import Dict
import json


def format_linkedin_post(post: str, metadata: Dict) -> str:
    """
    Format a LinkedIn post with metadata for display.
    
    Args:
        post: The LinkedIn post text
        metadata: Execution metadata
        
    Returns:
        Formatted string with post and metadata
    """
    separator = "=" * 80
    
    output = f"""
{separator}
LINKEDIN POST (READY TO PUBLISH)
{separator}

{post}

{separator}
METADATA
{separator}
Research Steps: {metadata.get('research_steps', 'N/A')}
Post Length: {metadata.get('post_length', 'N/A')} characters
Model Used: {metadata.get('model_used', 'N/A')}
Validation: {'✓ Passed' if metadata.get('validation', {}).get('valid') else '⚠ Warnings'}

"""
    
    if metadata.get('validation', {}).get('warnings'):
        output += "\nWarnings:\n"
        for warning in metadata['validation']['warnings']:
            output += f"  - {warning}\n"
    
    return output


def save_research_bundle(topic: str, research: str, post: str, metadata: Dict, output_dir: str) -> Dict[str, str]:
    """
    Save complete research bundle to files.
    
    Args:
        topic: Research topic
        research: Full research report
        post: LinkedIn post
        metadata: Execution metadata
        output_dir: Directory to save files
        
    Returns:
        Dict mapping file types to paths
    """
    from pathlib import Path
    from datetime import datetime
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    topic_slug = topic.lower().replace(" ", "_")[:50]
    
    files = {}
    
    # Save post
    post_file = output_path / f"{topic_slug}_{timestamp}_post.txt"
    post_file.write_text(post)
    files['post'] = str(post_file)
    
    # Save research
    research_file = output_path / f"{topic_slug}_{timestamp}_research.md"
    research_file.write_text(research)
    files['research'] = str(research_file)
    
    # Save metadata
    metadata_file = output_path / f"{topic_slug}_{timestamp}_metadata.json"
    metadata_file.write_text(json.dumps(metadata, indent=2))
    files['metadata'] = str(metadata_file)
    
    return files

