"""
Main research workflow using LangChain Expression Language (LCEL).
Implements: Research → Synthesis → Writing → Validation
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain import hub
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnablePassthrough

from config.settings import settings
from src.tools.search_tool import ResearchSearchTool
from src.tools.scrape_tool import ResearchScrapeTool
from src.prompts.research_prompts import RESEARCHER_SYSTEM_PROMPT, RESEARCH_TASK_TEMPLATE
from src.prompts.writer_prompts import WRITER_SYSTEM_PROMPT, WRITER_TASK_TEMPLATE
from src.utils.logger import get_logger
from src.utils.validators import validate_topic, validate_linkedin_post
from src.types.schemas import LinkedInPost

import logging
import os
import json

logger = get_logger(__name__)


class ResearchWorkflow:
    """
    Orchestrates the complete research-to-LinkedIn pipeline.
    Uses LCEL for transparent, debuggable workflow.
    """
    
    def __init__(self):
        # Set environment variables for tools that need them
        os.environ['TAVILY_API_KEY'] = settings.tavily_api_key
        os.environ['GOOGLE_API_KEY'] = settings.google_api_key
        
        self.llm = ChatGoogleGenerativeAI(
            model=settings.llm_model,
            temperature=0.1,  # Lower temperature for strict format adherence
            max_output_tokens=settings.max_tokens,
            google_api_key=settings.google_api_key,
            convert_system_message_to_human=True
        )
        
        # Initialize tools
        self.search_tool = ResearchSearchTool(
            api_key=settings.tavily_api_key,
            max_results=settings.max_search_results
        )
        
        self.scrape_tool = ResearchScrapeTool(
            api_key=settings.firecrawl_api_key
        )
        
        # Setup agents
        self._setup_research_agent()
        self._setup_writer_agent()
    
    def _setup_research_agent(self):
        """Configure the research agent with tools"""
        tools = [
            self.search_tool.as_langchain_tool(),
            self.scrape_tool.as_langchain_tool()
        ]
        
        # Create explicit ReAct prompt for Gemini
        template = """You are a research assistant. Answer questions using ONLY the following format. DO NOT deviate from this format.

Tools available:
{tools}

CRITICAL: You MUST use this EXACT format for EVERY response:

Thought: [your reasoning about what to do next]
Action: [MUST be EXACTLY one of: {tool_names}]
Action Input: [the exact input for the tool]

After you receive an Observation, repeat the cycle:
Thought: [your reasoning based on the observation]
Action: [tool name]
Action Input: [tool input]

When you have gathered enough information:
Thought: I have enough information to provide the final answer
Final Answer: [your complete research summary]

RULES:
- NEVER write a full response before using tools
- ALWAYS follow the Thought/Action/Action Input format
- ONLY write "Final Answer" after you've used the tools and have observations
- Keep each Thought brief (1-2 sentences)

Begin!

Question: {input}
{agent_scratchpad}"""
        
        prompt = PromptTemplate.from_template(template)
        
        agent = create_react_agent(
            llm=self.llm,
            tools=tools,
            prompt=prompt
        )
        
        self.research_agent = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            max_iterations=10,
            handle_parsing_errors="Check your output and make sure it conforms to the expected format!",
            return_intermediate_steps=True,
            max_execution_time=300,  # 5 minutes timeout
        )
    
    def _setup_writer_agent(self):
        """Configure the content writer with structured output"""
        # Create parser for LinkedIn post structure
        parser = PydanticOutputParser(pydantic_object=LinkedInPost)
        
        # Add format instructions to the prompt
        template = f"""{WRITER_SYSTEM_PROMPT}

{WRITER_TASK_TEMPLATE}

CRITICAL: You MUST respond with ONLY valid JSON matching this exact format:
{{format_instructions}}

Do not include any other text, explanations, or markdown. Only the JSON object."""
        
        self.writer_prompt = PromptTemplate(
            template=template,
            input_variables=["research_report", "topic"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )
        
        # Try structured output first, fallback to parsing
        try:
            # Use Gemini's native structured output if available
            structured_llm = self.llm.with_structured_output(LinkedInPost)
            self.writer_chain = self.writer_prompt | structured_llm
        except:
            # Fallback to manual parsing
            self.writer_chain = self.writer_prompt | self.llm | parser
    
    def execute(self, topic: str) -> dict:
        """
        Execute the complete workflow.
        
        Args:
            topic: Research topic
            
        Returns:
            dict with:
                - topic: original topic
                - research_report: full research findings
                - linkedin_post: final post text
                - metadata: execution details
        """
        
        # Validate input
        validate_topic(topic)
        logger.info(f"Starting research workflow for topic: {topic}")
        
        try:
            # Stage 1: Research
            logger.info("Stage 1: Conducting research...")
            research_result = self.research_agent.invoke({
                "input": RESEARCH_TASK_TEMPLATE.format(topic=topic)
            })
            
            # Extract research report - handle different output formats
            raw_output = research_result["output"]
            if isinstance(raw_output, list):
                # Extract text from list of agent steps
                research_report = "\n\n".join([
                    step.get("text", str(step)) for step in raw_output 
                    if isinstance(step, dict) and "text" in step
                ])
                if not research_report:
                    research_report = str(raw_output)
            else:
                research_report = str(raw_output)
            
            intermediate_steps = research_result.get("intermediate_steps", [])
            
            logger.info(f"Research completed. Report length: {len(research_report)} chars")
            logger.info(f"Tools used: {len(intermediate_steps)} times")
            
            # Stage 2: Content Generation
            logger.info("Stage 2: Generating LinkedIn post...")
            post_structured = self.writer_chain.invoke({
                "research_report": research_report,
                "topic": topic
            })
            
            # Convert structured output to formatted text
            if isinstance(post_structured, LinkedInPost):
                linkedin_post = post_structured.format_for_linkedin()
            elif isinstance(post_structured, str):
                # Try to parse JSON if we got a string
                try:
                    post_dict = json.loads(post_structured)
                    post_obj = LinkedInPost(**post_dict)
                    linkedin_post = post_obj.format_for_linkedin()
                except:
                    # Fallback to raw string
                    linkedin_post = post_structured
            else:
                linkedin_post = str(post_structured)
            
            logger.info(f"LinkedIn post generated. Length: {len(linkedin_post)} chars")
            
            # Stage 3: Validation
            logger.info("Stage 3: Validating output...")
            validation_result = validate_linkedin_post(linkedin_post)
            
            if not validation_result["valid"]:
                logger.warning(f"Validation warnings: {validation_result['warnings']}")
            
            # Compile results
            result = {
                "topic": topic,
                "research_report": research_report,
                "linkedin_post": linkedin_post,
                "metadata": {
                    "research_steps": len(intermediate_steps),
                    "post_length": len(linkedin_post),
                    "validation": validation_result,
                    "model_used": settings.llm_model
                }
            }
            
            logger.info("Workflow completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Workflow failed: {str(e)}", exc_info=True)
            raise

