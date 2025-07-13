"""Email Sender Agent - Dedicated email sending functionality."""

from typing import Optional, Dict, Any
from google.adk import Agent
from google.adk.tools import FunctionTool
from .model_selector import get_model_for_interaction, InteractionType
from . import prompt
from .tools import (
    send_email_tool,
    send_bulk_emails_tool,
    send_follow_up_email_tool,
    create_email_campaign_tool,
    verify_email_tool,
    test_email_connection_tool
)

def create_email_sender_agent(
    interaction_type: InteractionType = "auto",
    force_model: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
    input_data: Optional[Any] = None,
    url: Optional[str] = None,
    user_agent: Optional[str] = None
) -> Agent:
    """
    Create an email sender agent with the appropriate model.
    
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
        name="email_sender_agent",
        model=model,
        description=(
            "Dedicated email sending agent that can send individual emails, bulk emails, "
            "follow-up emails, and create email campaigns. Supports HTML emails, attachments, "
            "and template personalization."
        ),
        instruction=prompt.EMAIL_SENDER_PROMPT,
        output_key="email_sender_output",
        tools=[
            send_email_tool,
            send_bulk_emails_tool,
            send_follow_up_email_tool,
            create_email_campaign_tool,
            verify_email_tool,
            test_email_connection_tool,
        ],
    )

# Default agent
email_sender_agent = create_email_sender_agent() 