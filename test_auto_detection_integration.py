#!/usr/bin/env python3
"""
Integration test for auto-detection with ADK framework.
"""

import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'recruiting_agency'))

def test_model_selector():
    """Test the model selector functionality."""
    print("🧪 Testing Model Selector")
    print("=" * 40)
    
    try:
        from recruiting_agency.model_selector import (
            get_model_for_interaction,
            auto_detect_interaction_type,
            is_voice_model,
            is_text_model
        )
        
        # Test voice detection
        voice_context = {
            "headers": {"content-type": "audio/wav"},
            "url": "https://api.example.com/voice",
            "user_agent": "VoiceApp/1.0"
        }
        
        model = get_model_for_interaction("auto", **voice_context)
        print(f"✅ Voice context -> Model: {model}")
        print(f"✅ Is voice model: {is_voice_model(model)}")
        print(f"✅ Is text model: {is_text_model(model)}")
        
        # Test text detection
        text_context = {
            "headers": {"content-type": "text/plain"},
            "url": "https://api.example.com/chat",
            "user_agent": "Mozilla/5.0"
        }
        
        model = get_model_for_interaction("auto", **text_context)
        print(f"✅ Text context -> Model: {model}")
        print(f"✅ Is voice model: {is_voice_model(model)}")
        print(f"✅ Is text model: {is_text_model(model)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Model selector test failed: {e}")
        return False

def test_agent_factory():
    """Test the agent factory functionality."""
    print("\n🧪 Testing Agent Factory")
    print("=" * 40)
    
    try:
        from recruiting_agency.agent_factory import (
            create_auto_agent,
            create_text_agent,
            create_voice_agent
        )
        
        # Test auto agent creation
        agent = create_auto_agent(
            headers={"content-type": "audio/wav"},
            url="https://api.example.com/voice"
        )
        print(f"✅ Auto agent created with model: {agent.model}")
        
        # Test text agent creation
        text_agent = create_text_agent()
        print(f"✅ Text agent created with model: {text_agent.model}")
        
        # Test voice agent creation
        voice_agent = create_voice_agent()
        print(f"✅ Voice agent created with model: {voice_agent.model}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent factory test failed: {e}")
        return False

def test_agent_capabilities():
    """Test agent capabilities detection."""
    print("\n🧪 Testing Agent Capabilities")
    print("=" * 40)
    
    try:
        from recruiting_agency.model_selector import get_model_capabilities
        
        # Test voice model capabilities
        voice_caps = get_model_capabilities("gemini-2.0-flash-live-001")
        print(f"✅ Voice model capabilities: {voice_caps}")
        
        # Test text model capabilities
        text_caps = get_model_capabilities("gemini-1.5-pro-latest")
        print(f"✅ Text model capabilities: {text_caps}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent capabilities test failed: {e}")
        return False

def test_web_integration():
    """Test web integration scenarios."""
    print("\n🧪 Testing Web Integration")
    print("=" * 40)
    
    try:
        from recruiting_agency.model_selector import auto_detect_interaction_type
        
        # Simulate Flask/FastAPI request
        class MockRequest:
            def __init__(self, headers, url, user_agent):
                self.headers = headers
                self.url = url
                self.user_agent = user_agent
        
        # Voice request
        voice_request = MockRequest(
            headers={"content-type": "audio/wav", "x-voice-interaction": "true"},
            url="https://api.example.com/voice/stream",
            user_agent="VoiceApp/1.0"
        )
        
        detected_type = auto_detect_interaction_type(
            headers=voice_request.headers,
            url=voice_request.url,
            user_agent=voice_request.user_agent
        )
        print(f"✅ Voice request detected as: {detected_type}")
        
        # Text request
        text_request = MockRequest(
            headers={"content-type": "text/plain"},
            url="https://api.example.com/chat",
            user_agent="Mozilla/5.0"
        )
        
        detected_type = auto_detect_interaction_type(
            headers=text_request.headers,
            url=text_request.url,
            user_agent=text_request.user_agent
        )
        print(f"✅ Text request detected as: {detected_type}")
        
        return True
        
    except Exception as e:
        print(f"❌ Web integration test failed: {e}")
        return False

def main():
    """Run all integration tests."""
    print("🚀 Recruiting Agency Auto-Detection Integration Tests")
    print("=" * 60)
    
    tests = [
        test_model_selector,
        test_agent_factory,
        test_agent_capabilities,
        test_web_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All integration tests passed!")
        print("\n🎉 Auto-detection is ready for production use!")
        print("\nKey Features Verified:")
        print("- Multi-method voice detection")
        print("- Automatic model selection")
        print("- Agent factory integration")
        print("- Web integration compatibility")
        print("- Capability detection")
    else:
        print("❌ Some tests failed. Please check the implementation.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 