"""
Agent factory for creating agents based on interaction type.
"""

from typing import Optional, Dict, Any, Literal
from google.adk import Agent
from google.adk.tools.agent_tool import AgentTool

from .model_selector import get_model_for_interaction, InteractionType
from . import prompt
from .sub_agents.bd_agent import bd_agent
from .sub_agents.candidate_outreach_agent import candidate_outreach_agent
from .sub_agents.marketing_content_agent import marketing_content_agent
from .sub_agents.backend_matching_agent import backend_matching_agent
from .sub_agents.google_search_agent import google_search_agent
from .sub_agents.email_discovery_agent import email_discovery_agent
from .sub_agents.email_sender_agent import email_sender_agent

def create_recruiting_coordinator(
    interaction_type: InteractionType = "auto",
    force_model: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
    input_data: Optional[Any] = None,
    url: Optional[str] = None,
    user_agent: Optional[str] = None
) -> Agent:
    """
    Create a recruiting coordinator agent with the appropriate model.
    
    Args:
        interaction_type: Type of interaction ("voice", "text", or "auto")
        force_model: Override to use a specific model
        headers: HTTP headers for auto-detection
        input_data: Input data for auto-detection
        url: Request URL for auto-detection
        user_agent: User-Agent for auto-detection
    
    Returns:
        Configured Agent instance
    """
    model = get_model_for_interaction(
        interaction_type=interaction_type,
        force_model=force_model,
        headers=headers,
        input_data=input_data,
        url=url,
        user_agent=user_agent
    )
    
    return Agent(
        name="recruiting_coordinator",
        model=model,
        description=(
            "Orchestrates a comprehensive recruiting process by coordinating specialized "
            "sub-agents for business development, candidate outreach, marketing content, "
            "backend matching, and real-time research to provide end-to-end hiring solutions."
        ),
        instruction=prompt.RECRUITING_COORDINATOR_PROMPT,
        output_key="recruiting_coordinator_output",
        tools=[
            AgentTool(agent=bd_agent),
            AgentTool(agent=candidate_outreach_agent),
            AgentTool(agent=marketing_content_agent),
            AgentTool(agent=backend_matching_agent),
            AgentTool(agent=google_search_agent),
            AgentTool(agent=email_discovery_agent),
            AgentTool(agent=email_sender_agent),
        ],
    )

def create_voice_agent(
    headers: Optional[Dict[str, str]] = None,
    input_data: Optional[Any] = None,
    url: Optional[str] = None,
    user_agent: Optional[str] = None
) -> Agent:
    """Create a voice-capable recruiting coordinator."""
    return create_recruiting_coordinator(
        "voice",
        headers=headers,
        input_data=input_data,
        url=url,
        user_agent=user_agent
    )

def create_text_agent(
    headers: Optional[Dict[str, str]] = None,
    input_data: Optional[Any] = None,
    url: Optional[str] = None,
    user_agent: Optional[str] = None
) -> Agent:
    """Create a text-only recruiting coordinator."""
    return create_recruiting_coordinator(
        "text",
        headers=headers,
        input_data=input_data,
        url=url,
        user_agent=user_agent
    )

def create_auto_agent(
    headers: Optional[Dict[str, str]] = None,
    input_data: Optional[Any] = None,
    url: Optional[str] = None,
    user_agent: Optional[str] = None
) -> Agent:
    """Create an auto-detecting recruiting coordinator."""
    return create_recruiting_coordinator(
        "auto",
        headers=headers,
        input_data=input_data,
        url=url,
        user_agent=user_agent
    )

# Default agent (text-based for safety)
root_agent = create_text_agent()

class AgentFactory:
    """Factory for creating agents with appropriate model selection."""
    
    @staticmethod
    def create_main_agent(
        interaction_type: InteractionType = "auto",
        force_model: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        input_data: Optional[Any] = None,
        url: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Agent:
        """
        Create the main recruiting agency agent.
        
        Args:
            interaction_type: Type of interaction ("voice", "text", or "auto")
            force_model: Override to use a specific model
            headers: HTTP headers for auto-detection
            input_data: Input data for auto-detection
            url: Request URL for auto-detection
            user_agent: User-Agent for auto-detection
        
        Returns:
            Configured Agent
        """
        return create_recruiting_coordinator(
            interaction_type=interaction_type,
            force_model=force_model,
            headers=headers,
            input_data=input_data,
            url=url,
            user_agent=user_agent
        )
    
    @staticmethod
    def create_bd_agent(
        interaction_type: InteractionType = "auto",
        force_model: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        input_data: Optional[Any] = None,
        url: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Agent:
        """
        Create a BD agent with appropriate model.
        
        Args:
            interaction_type: Type of interaction ("voice", "text", or "auto")
            force_model: Override to use a specific model
            headers: HTTP headers for auto-detection
            input_data: Input data for auto-detection
            url: Request URL for auto-detection
            user_agent: User-Agent for auto-detection
        
        Returns:
            Configured BD Agent
        """
        model = get_model_for_interaction(
            interaction_type=interaction_type,
            force_model=force_model,
            headers=headers,
            input_data=input_data,
            url=url,
            user_agent=user_agent
        )
        
        # Create a new BD agent with the selected model
        from .sub_agents.bd_agent import prompt as bd_prompt
        from .sub_agents.bd_agent.tools import (
            fetch_recent_funding_rounds_tool,
            filter_blockchain_companies_tool,
            personalize_outreach_tool,
            send_personalized_emails_tool,
            book_meeting_tool
        )
        
        return Agent(
            model=model,
            name="bd_agent",
            instruction=bd_prompt.BD_AGENT_PROMPT,
            output_key="business_development_analysis_output",
            tools=[
                fetch_recent_funding_rounds_tool,
                filter_blockchain_companies_tool,
                personalize_outreach_tool,
                send_personalized_emails_tool,
                book_meeting_tool
            ],
        )
    
    @staticmethod
    def create_google_search_agent(
        interaction_type: InteractionType = "auto",
        force_model: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        input_data: Optional[Any] = None,
        url: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Agent:
        """
        Create a Google Search agent with appropriate model.
        
        Args:
            interaction_type: Type of interaction ("voice", "text", or "auto")
            force_model: Override to use a specific model
            headers: HTTP headers for auto-detection
            input_data: Input data for auto-detection
            url: Request URL for auto-detection
            user_agent: User-Agent for auto-detection
        
        Returns:
            Configured Google Search Agent
        """
        model = get_model_for_interaction(
            interaction_type=interaction_type,
            force_model=force_model,
            headers=headers,
            input_data=input_data,
            url=url,
            user_agent=user_agent
        )
        
        # Create a new Google Search agent with the selected model
        from .sub_agents.google_search_agent import prompt as search_prompt
        from google.adk.tools import google_search
        
        return Agent(
            model=model,
            name="google_search_agent",
            instruction=search_prompt.GOOGLE_SEARCH_AGENT_PROMPT,
            output_key="google_search_output",
            tools=[google_search],
        )
    
    @staticmethod
    def create_email_sender_agent(
        interaction_type: InteractionType = "auto",
        force_model: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        input_data: Optional[Any] = None,
        url: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Agent:
        """
        Create the dedicated email sender agent.
        """
        from .sub_agents.email_sender_agent import create_email_sender_agent
        return create_email_sender_agent(
            interaction_type=interaction_type,
            force_model=force_model,
            headers=headers,
            input_data=input_data,
            url=url,
            user_agent=user_agent
        )
    
    @staticmethod
    def create_all_agents(
        interaction_type: InteractionType = "auto",
        force_model: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        input_data: Optional[Any] = None,
        url: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Dict[str, Agent]:
        """
        Create all agents with consistent model selection.
        
        Args:
            interaction_type: Type of interaction ("voice", "text", or "auto")
            force_model: Override to use a specific model
            headers: HTTP headers for auto-detection
            input_data: Input data for auto-detection
            url: Request URL for auto-detection
            user_agent: User-Agent for auto-detection
        
        Returns:
            Dictionary containing all agents
        """
        return {
            "main_agent": AgentFactory.create_main_agent(
                interaction_type, force_model, headers, input_data, url, user_agent
            ),
            "bd_agent": AgentFactory.create_bd_agent(
                interaction_type, force_model, headers, input_data, url, user_agent
            ),
            "google_search_agent": AgentFactory.create_google_search_agent(
                interaction_type, force_model, headers, input_data, url, user_agent
            ),
            # Note: Other sub-agents would need similar implementation
            # For now, returning the existing agents
            "candidate_outreach_agent": candidate_outreach_agent,
            "marketing_content_agent": marketing_content_agent,
            "backend_matching_agent": backend_matching_agent
        } 