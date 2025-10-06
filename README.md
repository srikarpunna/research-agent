# LinkedIn Research Agent

Production-grade autonomous research agent that generates publication-ready LinkedIn posts using Google Gemini AI.

## Features

- **Comprehensive Web Research** - AI-optimized search using Tavily
- **Intelligent Web Scraping** - Managed scraping with FireCrawl
- **Powered by Google Gemini** - Latest Gemini 1.5 Pro model
- **Professional Content Generation** - LinkedIn-optimized posts
- **Transparent Workflows** - Debuggable with LangChain LCEL
- **Full Observability** - Monitoring with LangSmith
- **Quality Validation** - Automated output checks
- **Web Interface** - Beautiful Streamlit UI + CLI support
- **Easy Deployment** - One-click deploy to Streamlit Cloud

## Quick Start

### 1. Installation

```bash
# Clone and navigate to project
cd /Users/srikarpunna/Documents/research-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API keys:
# - Google Gemini API key from https://makersuite.google.com/app/apikey
# - Tavily API key from https://tavily.com/
# - FireCrawl API key from https://firecrawl.dev/
# - LangSmith API key from https://smith.langchain.com/
```

### 3. Validate Setup

```bash
python -m src.main validate-config
```

### 4. Run Your First Research

**Option A: Web Interface (Recommended)**
```bash
streamlit run app.py
```
Then open your browser to `http://localhost:8501`

**Option B: Command Line**
```bash
python -m src.main research "AI Agent Frameworks in 2025"
```

## Usage

### Web Interface (Streamlit)

The easiest way to use the research agent is through the web interface:

```bash
streamlit run app.py
```

**Features:**
- Beautiful, user-friendly interface
- Real-time progress tracking
- One-click download of posts and research reports
- Live configuration display
- Example topics for inspiration
- Automatic API key validation

### Command Line Usage

```bash
# Research a topic and generate LinkedIn post
python -m src.main research "Your Topic Here"
```

### Advanced Options

```bash
# Custom output directory
python -m src.main research "Your Topic" --output-dir ./my-posts

# Skip research report save (only save the post)
python -m src.main research "Your Topic" --no-save-research

# Non-interactive mode (no preview, just save files)
python -m src.main research "Your Topic" --no-interactive
```

### Examples

```bash
# Technology trends
python -m src.main research "The Rise of AI Agents in 2025"

# Business insights
python -m src.main research "Remote Work Productivity Statistics 2025"

# Industry analysis
python -m src.main research "Cloud Computing Market Trends"

# Product launches
python -m src.main research "Latest Features in LangChain Framework"
```

## Project Structure

```
research-agent/
├── config/
│   ├── __init__.py
│   └── settings.py          # Centralized configuration with Pydantic
├── src/
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── search_tool.py   # Tavily search wrapper
│   │   └── scrape_tool.py   # FireCrawl scraping wrapper
│   ├── agents/
│   │   └── __init__.py
│   ├── workflows/
│   │   ├── __init__.py
│   │   └── research_workflow.py  # Main LCEL workflow
│   ├── prompts/
│   │   ├── __init__.py
│   │   ├── research_prompts.py   # Research agent prompts
│   │   └── writer_prompts.py     # Content writer prompts
│   ├── output/
│   │   ├── __init__.py
│   │   └── formatters.py    # Output formatting
│   └── utils/
│       ├── __init__.py
│       ├── logger.py        # Logging configuration
│       └── validators.py    # Input/output validation
├── outputs/                 # Generated posts and reports
├── logs/                    # Application logs
├── .env                     # Your API keys (create from .env.example)
├── .env.example             # Template for environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

## Output Files

Each research run generates three files with timestamps:

1. **`*_post.txt`** - LinkedIn-ready post (copy-paste ready)
2. **`*_research.md`** - Full research report with sources
3. **`*_metadata.json`** - Execution details and validation results

Example output filenames:
```
ai_agent_frameworks_in_2025_20250930_143022_post.txt
ai_agent_frameworks_in_2025_20250930_143022_research.md
ai_agent_frameworks_in_2025_20250930_143022_metadata.json
```

## API Keys Required

### 1. Google Gemini API Key (Required)
- **Get it:** https://makersuite.google.com/app/apikey
- **Cost:** Free tier available (60 requests/minute)
- **Note:** Gemini 1.5 Pro offers great quality at lower cost than GPT-4

### 2. Tavily API Key (Required)
- **Get it:** https://tavily.com/
- **Free Tier:** 1,000 searches/month
- **Cost:** ~$0.01/search after free tier

### 3. FireCrawl API Key (Required)
- **Get it:** https://firecrawl.dev/
- **Free Tier:** 500 scrapes/month
- **Cost:** ~$0.01/scrape after free tier

### 4. LangSmith API Key (Optional, Recommended)
- **Get it:** https://smith.langchain.com/
- **Free Tier:** Available for development
- **Purpose:** Debugging, monitoring, and observability

## Configuration Options

Edit `.env` to customize:

### Model Selection
```bash
# Choose your Gemini model
LLM_MODEL=gemini-1.5-pro      # Best quality (default)
# LLM_MODEL=gemini-1.5-flash  # Faster, cheaper
# LLM_MODEL=gemini-1.0-pro    # Older but stable
```

### Research Depth
```bash
MAX_SEARCH_RESULTS=5          # Number of search results to analyze
MAX_SCRAPE_PAGES=3            # Number of pages to scrape deeply
RESEARCH_DEPTH=comprehensive  # quick, standard, or comprehensive
```

### Output Preferences
```bash
LINKEDIN_MAX_CHARS=3000       # Max post length
INCLUDE_HASHTAGS=true         # Add hashtags automatically
NUM_HASHTAGS=5                # Number of hashtags to include
```

## Monitoring & Debugging

### View Logs
```bash
# Real-time logs
tail -f logs/research_agent.log

# All logs
cat logs/research_agent.log
```

### LangSmith Tracing
View detailed execution traces at: https://smith.langchain.com/

Each research run is automatically traced showing:
- Tool calls (searches, scrapes)
- Agent reasoning
- Token usage
- Execution time
- Errors and retries

## Customization

### Change Writing Style
Edit `src/prompts/writer_prompts.py` to adjust:
- Tone (professional, casual, technical)
- Structure (hooks, CTAs)
- LinkedIn best practices

### Change Research Focus
Edit `src/prompts/research_prompts.py` to modify:
- Research depth
- Source prioritization
- Analysis approach

### Add New Tools
1. Create tool file in `src/tools/`
2. Implement tool wrapper class
3. Add to workflow in `src/workflows/research_workflow.py`

## Troubleshooting

### API Key Issues
```bash
# Validate configuration
python -m src.main validate-config

# Check .env file exists
ls -la .env

# Verify format (no quotes, no spaces around =)
cat .env
```

### Import Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Rate Limiting
If you hit rate limits:
- **Gemini:** Wait 1 minute or upgrade plan
- **Tavily:** Reduce MAX_SEARCH_RESULTS
- **FireCrawl:** Reduce MAX_SCRAPE_PAGES

### Empty Output
Check logs for errors:
```bash
tail -n 50 logs/research_agent.log
```

## Deployment

### Deploy to Streamlit Cloud (Recommended - FREE)

The easiest way to make your research agent publicly accessible:

**Step 1: Push to GitHub**
```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit: LinkedIn Research Agent"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR-USERNAME/research-agent.git
git branch -M main
git push -u origin main
```

**Step 2: Deploy to Streamlit Cloud**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository and branch
5. Set main file path to: `app.py`
6. Click "Advanced settings" and add your API keys:
   ```
   GOOGLE_API_KEY = "your-key"
   TAVILY_API_KEY = "your-key"
   FIRECRAWL_API_KEY = "your-key"
   LANGSMITH_API_KEY = "your-key" (optional)
   ```
7. Click "Deploy!"

Your app will be live at: `https://your-app-name.streamlit.app`

**Note:** Streamlit Cloud is completely free for public apps!

### Alternative Deployment Options

**Option 1: Railway** ($5/month)
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

**Option 2: Render** (Free tier available)
1. Connect your GitHub repository
2. Select "Web Service"
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `streamlit run app.py`
5. Add environment variables in settings

**Option 3: Docker Deployment**
```dockerfile
# Create Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

Deploy to any cloud provider that supports Docker (AWS ECS, Google Cloud Run, Azure, etc.)

## Production Considerations

For production use, consider:

1. **Error Monitoring** - Integrate Sentry or similar
2. **Rate Limiting** - Implement request throttling
3. **Caching** - Cache research results to reduce API calls
4. **Queue System** - Use Celery for async processing
5. **CI/CD** - Set up automated testing and deployment
6. **Cost Monitoring** - Track API usage with LangSmith

## Cost Estimation

Per research + LinkedIn post generation:

- **Gemini 1.5 Pro:** ~$0.002-0.01 (free tier available)
- **Tavily Searches:** 3-5 searches × $0.01 = $0.03-0.05
- **FireCrawl Scrapes:** 2-3 scrapes × $0.01 = $0.02-0.03
- **Total:** ~$0.05-0.09 per post (free tier covers first 500+ posts)

## Architecture

### Workflow Pipeline
```
1. Input Validation
   ↓
2. Research Agent
   ├── Web Search (Tavily)
   ├── Content Scraping (FireCrawl)
   └── Synthesis
   ↓
3. Writer Agent
   └── LinkedIn Post Generation
   ↓
4. Output Validation
   ↓
5. File Export
```

### Key Design Decisions

- **LangChain LCEL** - Explicit, debuggable workflows
- **Gemini API** - Cost-effective with excellent quality
- **Managed Services** - Tavily + FireCrawl for reliability
- **Modular Architecture** - Independently testable components
- **Production Logging** - Comprehensive error tracking
- **Validation Layer** - Quality assurance before output

## Contributing

This is a production-ready system. To contribute:

1. Maintain type hints
2. Add comprehensive error handling
3. Update tests for new features
4. Document API changes
5. Follow existing code style

## License

MIT License - Use freely for commercial and personal projects.

## Support

For issues or questions:
1. Check logs: `logs/research_agent.log`
2. Validate config: `python -m src.main validate-config`
3. Review LangSmith traces: https://smith.langchain.com/

---

**Built with LangChain + Google Gemini + Tavily + FireCrawl + Streamlit**

*Production-ready AI research agent for LinkedIn content generation*

**Interfaces:** Web UI (Streamlit) + CLI (Typer) | **Deployment:** Streamlit Cloud (Free) | **AI:** Google Gemini

