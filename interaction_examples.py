#!/usr/bin/env python3
"""
Example scripts for using the recruiting agency with different interaction types.
"""

import os
from recruiting_agency.agent_factory import (
    create_voice_agent,
    create_text_agent,
    create_auto_agent,
    create_recruiting_coordinator
)
from recruiting_agency.model_selector import get_model_capabilities

def example_text_interaction():
    """Example of text-based interaction."""
    print("=== Text Interaction Example ===")
    
    # Create a text-only agent
    agent = create_text_agent()
    
    # Check capabilities
    model = agent.model
    capabilities = get_model_capabilities(model)
    print(f"Model: {model}")
    print(f"Capabilities: {capabilities}")
    
    # Example text interaction
    user_input = "I need help with hiring blockchain developers for my startup"
    
    print(f"\nUser: {user_input}")
    print("Agent: [Text response would be generated here]")
    print("Note: This agent is optimized for text conversations")

def example_voice_interaction():
    """Example of voice-based interaction."""
    print("\n=== Voice Interaction Example ===")
    
    # Create a voice-capable agent
    agent = create_voice_agent()
    
    # Check capabilities
    model = agent.model
    capabilities = get_model_capabilities(model)
    print(f"Model: {model}")
    print(f"Capabilities: {capabilities}")
    
    # Example voice interaction
    user_input = "I need help with hiring blockchain developers for my startup"
    
    print(f"\nUser: [Voice input]: {user_input}")
    print("Agent: [Voice response would be generated here]")
    print("Note: This agent supports real-time voice conversations")

def example_auto_detection():
    """Example of auto-detecting interaction type."""
    print("\n=== Auto-Detection Example ===")
    
    # Create an auto-detecting agent
    agent = create_auto_agent()
    
    # Check capabilities
    model = agent.model
    capabilities = get_model_capabilities(model)
    print(f"Model: {model}")
    print(f"Capabilities: {capabilities}")
    
    print("Note: Auto-detection currently defaults to text for safety")

def example_custom_model():
    """Example of using a custom model."""
    print("\n=== Custom Model Example ===")
    
    # Create agent with custom model
    custom_model = "gemini-2.0-flash-live-001"
    agent = create_recruiting_coordinator(force_model=custom_model)
    
    # Check capabilities
    model = agent.model
    capabilities = get_model_capabilities(model)
    print(f"Model: {model}")
    print(f"Capabilities: {capabilities}")

def main():
    """Run all examples."""
    print("Recruiting Agency - Interaction Type Examples")
    print("=" * 50)
    
    example_text_interaction()
    example_voice_interaction()
    example_auto_detection()
    example_custom_model()
    
    print("\n" + "=" * 50)
    print("Usage Tips:")
    print("- Use create_text_agent() for web chat interfaces")
    print("- Use create_voice_agent() for voice/audio applications")
    print("- Use create_auto_agent() for applications that can detect input type")
    print("- Use create_recruiting_coordinator() for custom model selection")

if __name__ == "__main__":
    main() 