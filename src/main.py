"""
Command-line interface for the research agent.
Provides interactive and script-friendly interfaces.
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path
import json
from datetime import datetime

from config.settings import settings
from src.workflows.research_workflow import ResearchWorkflow
from src.utils.logger import setup_logging

# Initialize
app = typer.Typer(help="LinkedIn Research Agent - AI-powered content generation")
console = Console()
setup_logging()


@app.command()
def research(
    topic: str = typer.Argument(..., help="Topic to research"),
    output_dir: Path = typer.Option("./outputs", help="Output directory for results"),
    save_research: bool = typer.Option(True, help="Save full research report"),
    interactive: bool = typer.Option(True, help="Show interactive preview")
):
    """
    Research a topic and generate a LinkedIn post.
    
    Example:
        python -m src.main research "AI Agent Frameworks in 2025"
    """
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Execute workflow with progress indication
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        task1 = progress.add_task("[cyan]Researching topic...", total=None)
        
        try:
            workflow = ResearchWorkflow()
            result = workflow.execute(topic)
            
            progress.update(task1, description="[green]✓ Research complete")
            
        except Exception as e:
            console.print(f"[red]✗ Error: {str(e)}")
            raise typer.Exit(1)
    
    # Display results
    if interactive:
        console.print("\n")
        console.print(Panel(
            result["linkedin_post"],
            title="[bold green]LinkedIn Post (Ready to Publish)",
            border_style="green"
        ))
        
        console.print("\n[bold]Metadata:[/bold]")
        console.print(f"  • Research steps: {result['metadata']['research_steps']}")
        console.print(f"  • Post length: {result['metadata']['post_length']} characters")
        console.print(f"  • Model: {result['metadata']['model_used']}")
        
        if result['metadata']['validation']['warnings']:
            console.print("\n[yellow]Warnings:[/yellow]")
            for warning in result['metadata']['validation']['warnings']:
                console.print(f"  ⚠ {warning}")
    
    # Save outputs
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    topic_slug = topic.lower().replace(" ", "_")[:50]
    
    # Save LinkedIn post
    post_file = output_dir / f"{topic_slug}_{timestamp}_post.txt"
    post_file.write_text(result["linkedin_post"])
    console.print(f"\n[green]✓[/green] LinkedIn post saved: {post_file}")
    
    # Save research report (optional)
    if save_research:
        research_file = output_dir / f"{topic_slug}_{timestamp}_research.md"
        research_file.write_text(result["research_report"])
        console.print(f"[green]✓[/green] Research report saved: {research_file}")
    
    # Save metadata
    metadata_file = output_dir / f"{topic_slug}_{timestamp}_metadata.json"
    metadata_file.write_text(json.dumps(result["metadata"], indent=2))
    console.print(f"[green]✓[/green] Metadata saved: {metadata_file}")


@app.command()
def validate_config():
    """Validate that all required API keys and settings are configured correctly."""
    
    console.print("[bold]Validating Configuration...[/bold]\n")
    
    checks = {
        "Google/Gemini API Key": bool(settings.google_api_key),
        "Tavily API Key": bool(settings.tavily_api_key),
        "FireCrawl API Key": bool(settings.firecrawl_api_key),
        "LangSmith API Key": bool(settings.langsmith_api_key),
        "LangSmith Tracing Enabled": settings.langsmith_tracing
    }
    
    all_valid = True
    for check, status in checks.items():
        icon = "[green]✓[/green]" if status else "[red]✗[/red]"
        console.print(f"{icon} {check}")
        if not status:
            all_valid = False
    
    if all_valid:
        console.print("\n[bold green]✓ All configuration valid![/bold green]")
    else:
        console.print("\n[bold red]✗ Configuration incomplete. Check your .env file.[/bold red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()

