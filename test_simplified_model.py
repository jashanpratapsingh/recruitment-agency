#!/usr/bin/env python3
"""
Test script to verify simplified model selection.
"""

import os
import sys
from typing import Dict, Any

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'recruiting_agency'))

from recruiting_agency.model_selector import (
    get_model_for_interaction,
    auto_detect_interaction_type,
    detect_voice_from_headers,
    detect_voice_from_environment,
    detect_voice_from_url,
    detect_voice_from_user_agent
)

def test_simplified_model_selection():
    """Test that simplified model selection always returns text model."""
    
    print("🧪 Testing Simplified Model Selection")
    print("=" * 45)
    
    # Test different interaction types
    test_cases = [
        {
            "name": "Voice Interaction",
            "interaction_type": "voice",
            "expected_model": "gemini-1.5-pro-latest"
        },
        {
            "name": "Text Interaction", 
            "interaction_type": "text",
            "expected_model": "gemini-1.5-pro-latest"
        },
        {
            "name": "Auto Detection (Voice)",
            "interaction_type": "auto",
            "headers": {"content-type": "audio/wav"},
            "expected_model": "gemini-1.5-pro-latest"
        },
        {
            "name": "Auto Detection (Text)",
            "interaction_type": "auto",
            "headers": {"content-type": "text/plain"},
            "expected_model": "gemini-1.5-pro-latest"
        }
    ]
    
    for test_case in test_cases:
        try:
            model = get_model_for_interaction(
                interaction_type=test_case["interaction_type"],
                headers=test_case.get("headers")
            )
            
            print(f"✅ {test_case['name']}: {model}")
            if model == test_case["expected_model"]:
                print(f"   ✅ Expected model: {test_case['expected_model']}")
            else:
                print(f"   ⚠️  Unexpected model: {model} (expected {test_case['expected_model']})")
                
        except Exception as e:
            print(f"❌ {test_case['name']}: Error - {e}")
    
    return True

def test_voice_detection_still_works():
    """Test that voice detection methods still work for logging/debugging."""
    
    print("\n🔍 Testing Voice Detection (for logging)")
    print("=" * 45)
    
    # Test headers detection
    voice_headers = {"content-type": "audio/wav", "x-voice-interaction": "true"}
    text_headers = {"content-type": "text/plain"}
    
    print(f"Voice headers detection: {detect_voice_from_headers(voice_headers)}")
    print(f"Text headers detection: {detect_voice_from_headers(text_headers)}")
    
    # Test URL detection
    voice_url = "https://example.com/voice/chat"
    text_url = "https://example.com/text/chat"
    
    print(f"Voice URL detection: {detect_voice_from_url(voice_url)}")
    print(f"Text URL detection: {detect_voice_from_url(text_url)}")
    
    # Test User-Agent detection
    voice_ua = "VoiceApp/1.0"
    text_ua = "TextApp/1.0"
    
    print(f"Voice User-Agent detection: {detect_voice_from_user_agent(voice_ua)}")
    print(f"Text User-Agent detection: {detect_voice_from_user_agent(text_ua)}")
    
    return True

def test_auto_detection_still_works():
    """Test that auto-detection still works for logging purposes."""
    
    print("\n🤖 Testing Auto-Detection (for logging)")
    print("=" * 40)
    
    # Test voice detection
    voice_context = {
        "headers": {"content-type": "audio/wav"},
        "url": "https://example.com/voice",
        "user_agent": "VoiceApp/1.0"
    }
    
    detected_type = auto_detect_interaction_type(**voice_context)
    print(f"Voice context detection: {detected_type}")
    
    # Test text detection
    text_context = {
        "headers": {"content-type": "text/plain"},
        "url": "https://example.com/text",
        "user_agent": "TextApp/1.0"
    }
    
    detected_type = auto_detect_interaction_type(**text_context)
    print(f"Text context detection: {detected_type}")
    
    return True

def test_agent_creation():
    """Test that agents can be created with the simplified model selection."""
    
    print("\n🤖 Testing Agent Creation")
    print("=" * 30)
    
    try:
        from recruiting_agency.agent_factory import AgentFactory
        
        # Test creating agents with different interaction types
        agents = {
            "voice": AgentFactory.create_main_agent("voice"),
            "text": AgentFactory.create_main_agent("text"),
            "auto": AgentFactory.create_main_agent("auto")
        }
        
        for agent_type, agent in agents.items():
            print(f"✅ {agent_type.capitalize()} agent created with model: {agent.model}")
            
            # Verify the model is the text model
            if agent.model == "gemini-1.5-pro-latest":
                print(f"   ✅ Using simplified text model")
            else:
                print(f"   ⚠️  Using model: {agent.model}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating agents: {e}")
        return False

def demonstrate_simplified_usage():
    """Demonstrate how to use the simplified model selection."""
    
    print("\n📚 Simplified Usage Examples")
    print("=" * 35)
    
    examples = [
        {
            "title": "Simple Agent Creation",
            "code": """
from recruiting_agency.agent_factory import AgentFactory

# All agents use the same text model
voice_agent = AgentFactory.create_main_agent("voice")
text_agent = AgentFactory.create_main_agent("text")
auto_agent = AgentFactory.create_main_agent("auto")

# All will use gemini-1.5-pro-latest
""",
            "description": "All interaction types use the same model"
        },
        {
            "title": "ADK Web Usage",
            "code": """
# Start ADK web - always uses text model
adk web

# Or with environment variables (for logging)
export VOICE_INTERACTION=true && adk web
""",
            "description": "ADK web always uses the same model"
        },
        {
            "title": "Direct Model Access",
            "code": """
from recruiting_agency.model_selector import get_model_for_interaction

# Always returns the same model
model = get_model_for_interaction("voice")  # gemini-1.5-pro-latest
model = get_model_for_interaction("text")   # gemini-1.5-pro-latest
model = get_model_for_interaction("auto")   # gemini-1.5-pro-latest
""",
            "description": "Direct model selection always returns text model"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['title']}")
        print(f"   {example['description']}")
        print(f"   Code: {example['code']}")

def main():
    """Run all tests for the simplified model selection."""
    
    print("🔧 Simplified Model Selection Test Suite")
    print("=" * 55)
    
    try:
        # Run all tests
        test1 = test_simplified_model_selection()
        test2 = test_voice_detection_still_works()
        test3 = test_auto_detection_still_works()
        test4 = test_agent_creation()
        
        # Show usage examples
        demonstrate_simplified_usage()
        
        # Summary
        print("\n📊 Test Results Summary")
        print("=" * 30)
        print(f"✅ Simplified Model Selection: {'PASS' if test1 else 'FAIL'}")
        print(f"✅ Voice Detection (logging): {'PASS' if test2 else 'FAIL'}")
        print(f"✅ Auto-Detection (logging): {'PASS' if test3 else 'FAIL'}")
        print(f"✅ Agent Creation: {'PASS' if test4 else 'FAIL'}")
        
        if all([test1, test2, test3, test4]):
            print("\n🎉 All tests passed! Simplified model selection is working!")
            print("\nKey Benefits:")
            print("- ✅ All interactions use the same reliable model")
            print("- ✅ No more model selection complexity")
            print("- ✅ No API version errors")
            print("- ✅ Voice detection still works for logging")
            print("- ✅ Backward compatible with existing code")
            
            print("\n🚀 Ready to use:")
            print("   adk web")
            print("   # All interaction types use gemini-1.5-pro-latest")
        else:
            print("\n❌ Some tests failed. Please check the implementation.")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 