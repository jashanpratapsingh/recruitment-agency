"""Model selection for email sender agent."""

from typing import Optional, Dict, Any, Literal

# Model configurations - Use text model for email composition
TEXT_MODEL = "gemini-1.5-pro-latest"

InteractionType = Literal["voice", "text", "auto"]

def get_model_for_interaction(
    interaction_type: InteractionType = "auto",
    force_model: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
    input_data: Optional[Any] = None,
    url: Optional[str] = None,
    user_agent: Optional[str] = None
) -> str:
    """
    Get the appropriate model for email sender agent based on interaction type.
    
    Args:
        interaction_type: Type of interaction ("voice", "text", or "auto")
        force_model: Override to use a specific model
        headers: HTTP headers for auto-detection
        input_data: Input data for auto-detection
        url: Request URL for auto-detection
        user_agent: User-Agent for auto-detection
    
    Returns:
        Model name string
    """
    # For email sending, we prefer text-based models for better email composition
    if force_model:
        return force_model
    
    # Always use text model for email composition
    return TEXT_MODEL 