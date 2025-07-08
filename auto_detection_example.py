#!/usr/bin/env python3
"""
Example script demonstrating auto-detection capabilities for voice vs text interactions.
"""

import os
import sys
from typing import Dict, Any

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'recruiting_agency'))

from recruiting_agency.model_selector import (
    auto_detect_interaction_type,
    get_model_for_interaction,
    detect_voice_from_headers,
    detect_voice_from_environment,
    detect_voice_from_input_format,
    detect_voice_from_url,
    detect_voice_from_user_agent
)
from recruiting_agency.agent_factory import AgentFactory, create_auto_agent, create_text_agent, create_voice_agent

def demonstrate_voice_detection():
    """Demonstrate various voice detection methods."""
    
    print("🔍 Voice Detection Demonstration")
    print("=" * 50)
    
    # Test 1: Headers detection
    print("\n1. Header-based Detection:")
    voice_headers = {
        "content-type": "audio/wav",
        "x-voice-interaction": "true",
        "x-webrtc": "enabled"
    }
    
    text_headers = {
        "content-type": "text/plain",
        "user-agent": "Mozilla/5.0"
    }
    
    print(f"Voice headers: {detect_voice_from_headers(voice_headers)}")
    print(f"Text headers: {detect_voice_from_headers(text_headers)}")
    
    # Test 2: Environment variables
    print("\n2. Environment-based Detection:")
    # Set a voice environment variable
    os.environ["VOICE_INTERACTION"] = "true"
    print(f"Voice env detected: {detect_voice_from_environment()}")
    
    # Clear the environment variable
    os.environ.pop("VOICE_INTERACTION", None)
    print(f"Text env detected: {detect_voice_from_environment()}")
    
    # Test 3: Input format detection
    print("\n3. Input Format Detection:")
    audio_file = "recording.wav"
    text_input = "Hello, this is a text message"
    binary_data = b'\x00\x01\x02\x03'  # Simulated audio bytes
    
    print(f"Audio file: {detect_voice_from_input_format(audio_file)}")
    print(f"Text input: {detect_voice_from_input_format(text_input)}")
    print(f"Binary data: {detect_voice_from_input_format(binary_data)}")
    
    # Test 4: URL detection
    print("\n4. URL-based Detection:")
    voice_url = "https://api.example.com/voice/stream"
    text_url = "https://api.example.com/chat"
    
    print(f"Voice URL: {detect_voice_from_url(voice_url)}")
    print(f"Text URL: {detect_voice_from_url(text_url)}")
    
    # Test 5: User-Agent detection
    print("\n5. User-Agent Detection:")
    voice_ua = "VoiceApp/1.0 (iOS; iPhone)"
    text_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    
    print(f"Voice User-Agent: {detect_voice_from_user_agent(voice_ua)}")
    print(f"Text User-Agent: {detect_voice_from_user_agent(text_ua)}")

def demonstrate_auto_detection():
    """Demonstrate comprehensive auto-detection."""
    
    print("\n🤖 Auto-Detection Examples")
    print("=" * 50)
    
    # Voice scenario
    print("\nVoice Interaction Scenario:")
    voice_context = {
        "headers": {"content-type": "audio/wav", "x-voice-interaction": "true"},
        "url": "https://api.example.com/voice/stream",
        "user_agent": "VoiceApp/1.0",
        "input_data": "recording.wav"
    }
    
    detected_type = auto_detect_interaction_type(**voice_context)
    model = get_model_for_interaction("auto", **voice_context)
    print(f"Detected type: {detected_type}")
    print(f"Selected model: {model}")
    
    # Text scenario
    print("\nText Interaction Scenario:")
    text_context = {
        "headers": {"content-type": "text/plain"},
        "url": "https://api.example.com/chat",
        "user_agent": "Mozilla/5.0",
        "input_data": "Hello, this is a text message"
    }
    
    detected_type = auto_detect_interaction_type(**text_context)
    model = get_model_for_interaction("auto", **text_context)
    print(f"Detected type: {detected_type}")
    print(f"Selected model: {model}")

def demonstrate_agent_creation():
    """Demonstrate agent creation with auto-detection."""
    
    print("\n🤖 Agent Creation with Auto-Detection")
    print("=" * 50)
    
    # Voice context
    voice_context = {
        "headers": {"content-type": "audio/wav"},
        "url": "https://api.example.com/voice",
        "user_agent": "VoiceApp/1.0",
        "input_data": "recording.wav"
    }
    
    print("\nCreating agents for voice interaction:")
    try:
        agents = AgentFactory.create_all_agents(
            interaction_type="auto",
            **voice_context
        )
        
        for agent_name, agent in agents.items():
            print(f"{agent_name}: {agent.model}")
    except Exception as e:
        print(f"Error creating agents: {e}")
    
    # Text context
    text_context = {
        "headers": {"content-type": "text/plain"},
        "url": "https://api.example.com/chat",
        "user_agent": "Mozilla/5.0",
        "input_data": "Hello, this is a text message"
    }
    
    print("\nCreating agents for text interaction:")
    try:
        agents = AgentFactory.create_all_agents(
            interaction_type="auto",
            **text_context
        )
        
        for agent_name, agent in agents.items():
            print(f"{agent_name}: {agent.model}")
    except Exception as e:
        print(f"Error creating agents: {e}")

def demonstrate_manual_override():
    """Demonstrate manual model override."""
    
    print("\n🔧 Manual Override Examples")
    print("=" * 50)
    
    # Force voice model even with text context
    text_context = {
        "headers": {"content-type": "text/plain"},
        "url": "https://api.example.com/chat",
        "user_agent": "Mozilla/5.0",
        "input_data": "Hello, this is a text message"
    }
    
    print("\nForcing voice model with text context:")
    model = get_model_for_interaction(
        interaction_type="auto",
        force_model="gemini-2.0-flash-live-001",
        **text_context
    )
    print(f"Selected model: {model}")
    
    # Force text model even with voice context
    voice_context = {
        "headers": {"content-type": "audio/wav"},
        "url": "https://api.example.com/voice",
        "user_agent": "VoiceApp/1.0",
        "input_data": "recording.wav"
    }
    
    print("\nForcing text model with voice context:")
    model = get_model_for_interaction(
        interaction_type="auto",
        force_model="gemini-1.5-pro-latest",
        **voice_context
    )
    print(f"Selected model: {model}")

def demonstrate_web_integration():
    """Demonstrate how this would work in a web context."""
    
    print("\n🌐 Web Integration Example")
    print("=" * 50)
    
    # Simulate a Flask/FastAPI request context
    class MockRequest:
        def __init__(self, headers: Dict[str, str], url: str, user_agent: str, data: Any = None):
            self.headers = headers
            self.url = url
            self.user_agent = user_agent
            self.data = data
    
    # Voice request
    voice_request = MockRequest(
        headers={"content-type": "audio/wav", "x-voice-interaction": "true"},
        url="https://api.example.com/voice/stream",
        user_agent="VoiceApp/1.0",
        data="recording.wav"
    )
    
    print("\nVoice web request:")
    detected_type = auto_detect_interaction_type(
        headers=voice_request.headers,
        url=voice_request.url,
        user_agent=voice_request.user_agent,
        input_data=voice_request.data
    )
    print(f"Detected type: {detected_type}")
    
    # Text request
    text_request = MockRequest(
        headers={"content-type": "text/plain"},
        url="https://api.example.com/chat",
        user_agent="Mozilla/5.0",
        data="Hello, this is a text message"
    )
    
    print("\nText web request:")
    detected_type = auto_detect_interaction_type(
        headers=text_request.headers,
        url=text_request.url,
        user_agent=text_request.user_agent,
        input_data=text_request.data
    )
    print(f"Detected type: {detected_type}")

def demonstrate_simple_agent_creation():
    """Demonstrate simple agent creation without complex dependencies."""
    
    print("\n🚀 Simple Agent Creation")
    print("=" * 50)
    
    try:
        # Create auto-detecting agent
        agent = create_auto_agent(
            headers={"content-type": "audio/wav"},
            url="https://api.example.com/voice",
            user_agent="VoiceApp/1.0"
        )
        print(f"Created auto-detecting agent with model: {agent.model}")
        
        # Create text agent
        text_agent = create_text_agent()
        print(f"Created text agent with model: {text_agent.model}")
        
        # Create voice agent
        voice_agent = create_voice_agent()
        print(f"Created voice agent with model: {voice_agent.model}")
        
    except Exception as e:
        print(f"Error creating agents: {e}")

def main():
    """Run all demonstrations."""
    print("🚀 Recruiting Agency Auto-Detection Demo")
    print("=" * 60)
    
    try:
        demonstrate_voice_detection()
        demonstrate_auto_detection()
        demonstrate_manual_override()
        demonstrate_web_integration()
        demonstrate_simple_agent_creation()
        
        print("\n✅ All demonstrations completed successfully!")
        print("\nKey Features:")
        print("- Multi-method voice detection (headers, env, input, URL, User-Agent)")
        print("- Automatic model selection based on interaction type")
        print("- Manual override capability")
        print("- Web integration ready")
        print("- Simple agent creation functions")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 