"""
Streamlit web interface for the LinkedIn Research Agent.
A simple, user-friendly UI for generating AI-powered LinkedIn posts.
"""

import streamlit as st
import json
from datetime import datetime
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import settings
from src.workflows.research_workflow import ResearchWorkflow
from src.utils.logger import setup_logging

# Page config
st.set_page_config(
    page_title="LinkedIn Research Agent",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize logging
setup_logging()


def check_api_keys():
    """Check if required API keys are configured"""
    missing_keys = []

    if not settings.google_api_key:
        missing_keys.append("Google/Gemini API Key")
    if not settings.tavily_api_key:
        missing_keys.append("Tavily API Key")
    if not settings.firecrawl_api_key:
        missing_keys.append("FireCrawl API Key")

    return missing_keys


def main():
    # Header
    st.title("LinkedIn Research Agent")
    st.markdown("**AI-powered content generation** using Google Gemini, Tavily, and FireCrawl")
    st.divider()

    # Sidebar - Configuration Info
    with st.sidebar:
        st.header("Configuration")

        # Check API keys
        missing_keys = check_api_keys()

        if missing_keys:
            st.error("Missing API Keys:")
            for key in missing_keys:
                st.markdown(f"- {key}")
            st.info("Please configure your API keys in the `.env` file")
            st.stop()
        else:
            st.success("All API keys configured")

        st.divider()

        # Model Info
        st.subheader("Model Settings")
        st.markdown(f"**Model:** {settings.llm_model}")
        st.markdown(f"**Temperature:** {settings.llm_temperature}")
        st.markdown(f"**Max Tokens:** {settings.max_tokens}")

        st.divider()

        # Research Settings
        st.subheader("Research Settings")
        st.markdown(f"**Search Results:** {settings.max_search_results}")
        st.markdown(f"**Scrape Pages:** {settings.max_scrape_pages}")
        st.markdown(f"**Research Depth:** {settings.research_depth}")

        st.divider()

        # Output Settings
        st.subheader("Output Settings")
        st.markdown(f"**Max Characters:** {settings.linkedin_max_chars}")
        st.markdown(f"**Hashtags:** {settings.num_hashtags if settings.include_hashtags else 'Disabled'}")

        st.divider()

        st.info("**Tip:** Edit `.env` file to customize settings")

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        # Input form
        with st.form("research_form"):
            topic = st.text_input(
                "Enter Research Topic",
                placeholder="e.g., AI Agent Frameworks in 2025",
                help="Enter any topic you want to research and create a LinkedIn post about"
            )

            col_save, col_submit = st.columns([1, 1])

            with col_save:
                save_research = st.checkbox("Save research report", value=True)

            with col_submit:
                submit_button = st.form_submit_button(
                    "Generate Post",
                    use_container_width=True,
                    type="primary"
                )

    with col2:
        # Example topics
        st.markdown("### Example Topics")
        example_topics = [
            "The Rise of AI Agents in 2025",
            "Remote Work Productivity Tips",
            "Cloud Computing Trends",
            "Sustainable Business Practices",
            "Future of Web Development"
        ]
        for example in example_topics:
            if st.button(example, key=example):
                topic = example
                submit_button = True

    # Process the research when form is submitted
    if submit_button and topic:

        # Create outputs directory
        output_dir = Path("./outputs")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Progress container
        with st.spinner("Researching topic... This may take 1-2 minutes"):

            progress_placeholder = st.empty()
            result_placeholder = st.empty()

            try:
                # Stage 1: Research
                progress_placeholder.info("Stage 1/3: Conducting web research...")

                workflow = ResearchWorkflow()
                result = workflow.execute(topic)

                # Stage 2: Writing
                progress_placeholder.info("Stage 2/3: Generating LinkedIn post...")

                # Stage 3: Complete
                progress_placeholder.success("Stage 3/3: Complete!")

                # Display results
                st.success("Research and post generation completed!")
                st.divider()

                # LinkedIn Post - Main display
                st.subheader("LinkedIn Post (Ready to Publish)")
                st.markdown("### Copy and paste this to LinkedIn:")

                # Display post in a nice box
                st.text_area(
                    label="LinkedIn Post",
                    value=result["linkedin_post"],
                    height=300,
                    label_visibility="collapsed"
                )

                # Download button for post
                st.download_button(
                    label="Download Post",
                    data=result["linkedin_post"],
                    file_name=f"linkedin_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True,
                    type="primary"
                )

                st.divider()

                # Metadata display
                col_meta1, col_meta2, col_meta3 = st.columns(3)

                with col_meta1:
                    st.metric("Research Steps", result['metadata']['research_steps'])

                with col_meta2:
                    st.metric("Post Length", f"{result['metadata']['post_length']} chars")

                with col_meta3:
                    st.metric("Model", result['metadata']['model_used'])

                # Warnings if any
                if result['metadata']['validation']['warnings']:
                    st.warning("Validation Warnings:")
                    for warning in result['metadata']['validation']['warnings']:
                        st.markdown(f"- {warning}")

                st.divider()

                # Research Report - Expandable
                if save_research:
                    with st.expander("View Full Research Report", expanded=False):
                        st.markdown(result["research_report"])

                        # Download button for research
                        st.download_button(
                            label="Download Research Report",
                            data=result["research_report"],
                            file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                            mime="text/markdown"
                        )

                # Save files locally
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                topic_slug = topic.lower().replace(" ", "_")[:50]

                # Save LinkedIn post
                post_file = output_dir / f"{topic_slug}_{timestamp}_post.txt"
                post_file.write_text(result["linkedin_post"])

                # Save research report
                if save_research:
                    research_file = output_dir / f"{topic_slug}_{timestamp}_research.md"
                    research_file.write_text(result["research_report"])

                # Save metadata
                metadata_file = output_dir / f"{topic_slug}_{timestamp}_metadata.json"
                metadata_file.write_text(json.dumps(result["metadata"], indent=2))

                st.info(f"Files saved to `{output_dir}/`")

            except Exception as e:
                progress_placeholder.empty()
                st.error(f"An error occurred: {str(e)}")
                st.exception(e)

    elif submit_button and not topic:
        st.warning("Please enter a research topic!")

    # Footer
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: gray; padding: 20px;'>
        Built using LangChain + Google Gemini + Tavily + FireCrawl<br>
        <small>Production-ready AI research agent for LinkedIn content generation</small>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
