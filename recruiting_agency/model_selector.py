"""
Model selector utility for choosing between voice and text models.
"""

import os
from typing import Literal, Optional, Dict, Any
from urllib.parse import urlparse

# Model configurations - Simplified to use only text model
TEXT_MODEL = "gemini-1.5-pro-latest"

InteractionType = Literal["voice", "text", "auto"]

def detect_voice_from_headers(headers: Optional[Dict[str, str]] = None) -> bool:
    """
    Detect voice interaction from HTTP headers.
    
    Args:
        headers: HTTP headers dictionary
    
    Returns:
        True if voice interaction is detected
    """
    if not headers:
        return False
    
    # Check for audio content types
    content_type = headers.get("content-type", "").lower()
    if any(audio_type in content_type for audio_type in ["audio/", "multipart/audio"]):
        return True
    
    # Check for voice-specific headers
    if headers.get("x-voice-interaction") == "true":
        return True
    
    # Check for WebRTC or voice API headers
    if any(header in headers for header in ["x-webrtc", "x-voice-api", "x-audio-stream"]):
        return True
    
    return False

def detect_voice_from_environment() -> bool:
    """
    Detect voice interaction from environment variables.
    
    Returns:
        True if voice interaction is detected
    """
    # Check environment variables
    voice_env_vars = [
        "VOICE_INTERACTION",
        "AUDIO_INPUT",
        "SPEECH_RECOGNITION",
        "RECRUITING_AGENCY_VOICE_MODE"
    ]
    
    for var in voice_env_vars:
        if os.getenv(var, "").lower() in ["true", "1", "yes", "on"]:
            return True
    
    return False

def detect_voice_from_input_format(input_data: Optional[Any] = None) -> bool:
    """
    Detect voice interaction from input data format.
    
    Args:
        input_data: The input data to analyze
    
    Returns:
        True if voice interaction is detected
    """
    if not input_data:
        return False
    
    # Check if input is audio data
    if hasattr(input_data, 'content_type'):
        if 'audio' in str(input_data.content_type).lower():
            return True
    
    # Check if input contains audio file extensions
    if isinstance(input_data, str):
        audio_extensions = ['.wav', '.mp3', '.m4a', '.ogg', '.flac', '.aac']
        if any(ext in input_data.lower() for ext in audio_extensions):
            return True
    
    # Check if input is bytes (likely audio data)
    if isinstance(input_data, bytes):
        # Simple heuristic: if it's bytes and not text, likely audio
        try:
            input_data.decode('utf-8')
            return False  # Successfully decoded as text
        except UnicodeDecodeError:
            return True  # Likely binary/audio data
    
    return False

def detect_voice_from_url(url: Optional[str] = None) -> bool:
    """
    Detect voice interaction from URL patterns.
    
    Args:
        url: The URL to analyze
    
    Returns:
        True if voice interaction is detected
    """
    if not url:
        return False
    
    url_lower = url.lower()
    
    # Check for voice/audio endpoints
    voice_patterns = [
        '/voice', '/audio', '/speech', '/call', '/phone',
        '/webrtc', '/stream', '/live', '/conversation'
    ]
    
    if any(pattern in url_lower for pattern in voice_patterns):
        return True
    
    return False

def detect_voice_from_user_agent(user_agent: Optional[str] = None) -> bool:
    """
    Detect voice interaction from User-Agent header.
    
    Args:
        user_agent: User-Agent string
    
    Returns:
        True if voice interaction is detected
    """
    if not user_agent:
        return False
    
    user_agent_lower = user_agent.lower()
    
    # Check for voice/audio applications
    voice_apps = [
        'voice', 'audio', 'speech', 'call', 'phone',
        'webrtc', 'stream', 'live', 'conversation'
    ]
    
    if any(app in user_agent_lower for app in voice_apps):
        return True
    
    return False

def auto_detect_interaction_type(
    headers: Optional[Dict[str, str]] = None,
    input_data: Optional[Any] = None,
    url: Optional[str] = None,
    user_agent: Optional[str] = None
) -> str:
    """
    Automatically detect if this should be a voice or text interaction.
    
    Args:
        headers: HTTP headers
        input_data: Input data to analyze
        url: Request URL
        user_agent: User-Agent string
    
    Returns:
        "voice" or "text"
    """
    # Check all detection methods
    detection_methods = [
        detect_voice_from_headers(headers),
        detect_voice_from_environment(),
        detect_voice_from_input_format(input_data),
        detect_voice_from_url(url),
        detect_voice_from_user_agent(user_agent)
    ]
    
    # If any method detects voice, use voice model
    if any(detection_methods):
        return "voice"
    
    # Default to text for safety
    return "text"

def get_model_for_interaction(
    interaction_type: InteractionType = "auto",
    force_model: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
    input_data: Optional[Any] = None,
    url: Optional[str] = None,
    user_agent: Optional[str] = None
) -> str:
    """
    Select the appropriate model based on interaction type.
    
    Args:
        interaction_type: Type of interaction ("voice", "text", or "auto")
        force_model: Override to use a specific model
        headers: HTTP headers for auto-detection
        input_data: Input data for auto-detection
        url: Request URL for auto-detection
        user_agent: User-Agent for auto-detection
    
    Returns:
        Model name to use
    """
    if force_model:
        return force_model
    
    # Always use the text model for all interactions
    return TEXT_MODEL

def is_voice_model(model: str) -> bool:
    """Check if a model supports voice interactions."""
    # Since we're using the same model for both voice and text,
    # we'll consider it voice-capable if it's the current model
    return model == TEXT_MODEL

def is_text_model(model: str) -> bool:
    """Check if a model supports text interactions."""
    return model == TEXT_MODEL

def get_model_capabilities(model: str) -> dict:
    """Get the capabilities of a specific model."""
    if model == TEXT_MODEL:
        return {
            "voice": True,
            "text": True,
            "streaming": False,
            "real_time": False,
            "turn_detection": False
        }
    else:
        return {
            "voice": False,
            "text": True,
            "streaming": False,
            "real_time": False,
            "turn_detection": False
        } 