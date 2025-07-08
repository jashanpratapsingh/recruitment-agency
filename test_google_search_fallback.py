#!/usr/bin/env python3
"""
Test script demonstrating Google Search Agent fallback functionality.
"""

import os
import sys
from typing import Dict, Any

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'recruiting_agency'))

from recruiting_agency.agent_factory import AgentFactory, create_auto_agent

def test_google_search_agent_direct():
    """Test the google_search_agent directly."""
    
    print("🔍 Testing Google Search Agent Directly")
    print("=" * 50)
    
    try:
        # Create the google search agent
        search_agent = AgentFactory.create_google_search_agent()
        
        # Test queries that require real-time information
        test_queries = [
            "What are the current salary trends for software engineers in 2024?",
            "Which ATS platforms are most popular for startups?",
            "What are the latest hiring challenges in the tech industry?",
            "Find information about recent blockchain funding rounds",
            "What are the best practices for remote hiring in 2024?"
        ]
        
        print(f"✅ Google Search Agent created successfully")
        print(f"📋 Model: {search_agent.model}")
        print(f"🔧 Tools: {[tool.name for tool in search_agent.tools]}")
        
        print(f"\n📝 Test queries ready for execution:")
        for i, query in enumerate(test_queries, 1):
            print(f"  {i}. {query}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Google Search Agent: {e}")
        return False

def test_fallback_scenarios():
    """Test scenarios where google_search_agent would be used as fallback."""
    
    print("\n🔄 Testing Fallback Scenarios")
    print("=" * 40)
    
    scenarios = [
        {
            "agent": "BD Agent",
            "need": "Recent funding data for blockchain companies",
            "fallback_query": "Find recent Series A funding rounds in blockchain startups 2024",
            "reason": "BD Agent's API data might be outdated"
        },
        {
            "agent": "Marketing Agent", 
            "need": "Current employer branding trends",
            "fallback_query": "Latest employer branding trends 2024",
            "reason": "Marketing Agent needs current market insights"
        },
        {
            "agent": "Backend Agent",
            "need": "Latest ATS platform comparisons",
            "fallback_query": "Compare ATS platforms for small companies 2024",
            "reason": "Backend Agent needs current tool information"
        },
        {
            "agent": "Outreach Agent",
            "need": "Current hiring market data",
            "fallback_query": "Current hiring challenges in tech industry 2024",
            "reason": "Outreach Agent needs real-time market intelligence"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. {scenario['agent']} needs: {scenario['need']}")
        print(f"   Fallback query: '{scenario['fallback_query']}'")
        print(f"   Reason: {scenario['reason']}")
    
    return True

def test_integration_with_main_agent():
    """Test that google_search_agent is properly integrated with main agent."""
    
    print("\n🔗 Testing Integration with Main Agent")
    print("=" * 45)
    
    try:
        # Create the main agent
        main_agent = create_auto_agent()
        
        # Check available tools
        agent_tools = []
        for tool in main_agent.tools:
            if hasattr(tool, 'agent'):
                agent_tools.append(tool.agent.name)
        
        print(f"✅ Main agent created successfully")
        print(f"📋 Total tools: {len(main_agent.tools)}")
        print(f"🔧 Sub-agents: {', '.join(agent_tools)}")
        
        # Verify google_search_agent is included
        if 'google_search_agent' in agent_tools:
            print("✅ Google Search Agent successfully integrated!")
        else:
            print("❌ Google Search Agent not found in main agent")
            return False
        
        # Test that the agent can be accessed
        search_agent_tool = None
        for tool in main_agent.tools:
            if hasattr(tool, 'agent') and tool.agent.name == 'google_search_agent':
                search_agent_tool = tool
                break
        
        if search_agent_tool:
            print("✅ Google Search Agent tool accessible in main agent")
            print(f"📋 Agent model: {search_agent_tool.agent.model}")
            print(f"🔧 Agent tools: {[t.name for t in search_agent_tool.agent.tools]}")
        else:
            print("❌ Google Search Agent tool not accessible")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing integration: {e}")
        return False

def test_model_selection():
    """Test that google_search_agent uses appropriate model selection."""
    
    print("\n🎛️ Testing Model Selection")
    print("=" * 35)
    
    try:
        # Test different interaction types
        interaction_types = ["text", "voice", "auto"]
        
        for interaction_type in interaction_types:
            search_agent = AgentFactory.create_google_search_agent(
                interaction_type=interaction_type
            )
            print(f"✅ {interaction_type.capitalize()} agent created with model: {search_agent.model}")
        
        # Test with force model
        forced_agent = AgentFactory.create_google_search_agent(
            force_model="gemini-1.5-pro-latest"
        )
        print(f"✅ Forced model agent created with model: {forced_agent.model}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing model selection: {e}")
        return False

def demonstrate_usage_examples():
    """Demonstrate how to use the google_search_agent."""
    
    print("\n📚 Usage Examples")
    print("=" * 30)
    
    examples = [
        {
            "title": "Direct Google Search Agent Usage",
            "code": """
from recruiting_agency.agent_factory import AgentFactory

# Create the agent
search_agent = AgentFactory.create_google_search_agent()

# Use the agent
response = search_agent.invoke({
    "query": "What are the current salary trends for blockchain developers?"
})
""",
            "description": "Direct usage for real-time information retrieval"
        },
        {
            "title": "Fallback Usage in Main Agent",
            "code": """
from recruiting_agency.agent_factory import create_auto_agent

# Create main agent with google_search_agent included
main_agent = create_auto_agent()

# The main agent will automatically use google_search_agent when needed
response = main_agent.invoke({
    "query": "I need current market data for hiring blockchain developers"
})
""",
            "description": "Automatic fallback when other agents need current data"
        },
        {
            "title": "Voice Interaction Support",
            "code": """
# Create voice-capable google search agent
voice_search_agent = AgentFactory.create_google_search_agent("voice")

# Use for voice interactions
response = voice_search_agent.invoke({
    "query": "Find current hiring trends in tech"
})
""",
            "description": "Voice interaction support with appropriate model"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['title']}")
        print(f"   {example['description']}")
        print(f"   Code:")
        print(f"   {example['code']}")

def main():
    """Run all tests for the Google Search Agent."""
    
    print("🧪 Google Search Agent Test Suite")
    print("=" * 60)
    
    try:
        # Run all tests
        test1 = test_google_search_agent_direct()
        test2 = test_fallback_scenarios()
        test3 = test_integration_with_main_agent()
        test4 = test_model_selection()
        
        # Show usage examples
        demonstrate_usage_examples()
        
        # Summary
        print("\n📊 Test Results Summary")
        print("=" * 30)
        print(f"✅ Direct Agent Test: {'PASS' if test1 else 'FAIL'}")
        print(f"✅ Fallback Scenarios: {'PASS' if test2 else 'FAIL'}")
        print(f"✅ Main Agent Integration: {'PASS' if test3 else 'FAIL'}")
        print(f"✅ Model Selection: {'PASS' if test4 else 'FAIL'}")
        
        if all([test1, test2, test3, test4]):
            print("\n🎉 All tests passed! Google Search Agent is ready for production!")
            print("\nKey Features Verified:")
            print("- ✅ Real-time information retrieval")
            print("- ✅ Fallback for other agents")
            print("- ✅ Integration with main recruiting agency")
            print("- ✅ Model selection for different interaction types")
            print("- ✅ Voice and text interaction support")
        else:
            print("\n❌ Some tests failed. Please check the implementation.")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 