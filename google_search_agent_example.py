#!/usr/bin/env python3
"""
Example script demonstrating the Google Search Agent functionality.
"""

import os
import sys
from typing import Dict, Any

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'recruiting_agency'))

from recruiting_agency.agent_factory import AgentFactory, create_auto_agent

def demonstrate_google_search_agent():
    """Demonstrate the Google Search Agent functionality."""
    
    print("🔍 Google Search Agent - Real-time Information Retrieval")
    print("=" * 60)
    
    # Create the google search agent
    try:
        search_agent = AgentFactory.create_google_search_agent()
        print(f"✅ Created Google Search Agent with model: {search_agent.model}")
        
        # Example queries that would benefit from real-time search
        example_queries = [
            "What are the latest salary trends for blockchain developers in 2024?",
            "Which ATS platforms are most popular for startups this year?",
            "What are the current hiring challenges in the tech industry?",
            "Find recent funding data for blockchain companies",
            "What are the best practices for remote hiring in 2024?"
        ]
        
        print(f"\n📋 Example queries for Google Search Agent:")
        for i, query in enumerate(example_queries, 1):
            print(f"  {i}. {query}")
        
        print(f"\n🎯 Use Cases:")
        print("  • When other agents need current market data")
        print("  • When users ask for recent trends or statistics")
        print("  • When fact verification is needed")
        print("  • When searching for latest tools and best practices")
        print("  • When real-time information is required")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating Google Search Agent: {e}")
        return False

def demonstrate_fallback_strategy():
    """Demonstrate how the google_search_agent serves as a fallback."""
    
    print("\n🔄 Fallback Strategy Demonstration")
    print("=" * 50)
    
    print("When other agents can't provide current information:")
    print("  1. BD Agent needs recent funding data → Google Search Agent")
    print("  2. Marketing Agent needs current trends → Google Search Agent")
    print("  3. Backend Agent needs latest tool info → Google Search Agent")
    print("  4. Outreach Agent needs market insights → Google Search Agent")
    
    print("\nExample scenarios:")
    print("  📊 'What are the current salary ranges for senior developers?'")
    print("  🏢 'Which ATS platforms are trending in 2024?'")
    print("  📈 'What are the latest hiring challenges post-pandemic?'")
    print("  💰 'Find recent funding rounds in the fintech space'")
    
    print("\nThe Google Search Agent will:")
    print("  ✅ Provide real-time, current information")
    print("  ✅ Cross-reference multiple sources")
    print("  ✅ Include source citations")
    print("  ✅ Give actionable insights")
    print("  ✅ Focus on recruiting-relevant data")

def demonstrate_integration():
    """Demonstrate integration with the main recruiting agency."""
    
    print("\n🔗 Integration with Main Recruiting Agency")
    print("=" * 50)
    
    try:
        # Create the main agent with google_search_agent included
        main_agent = create_auto_agent()
        print(f"✅ Main agent created with {len(main_agent.tools)} tools")
        
        # Check if google_search_agent is included
        agent_tools = [tool.agent.name for tool in main_agent.tools if hasattr(tool, 'agent')]
        print(f"📋 Available sub-agents: {', '.join(agent_tools)}")
        
        if 'google_search_agent' in agent_tools:
            print("✅ Google Search Agent successfully integrated!")
        else:
            print("❌ Google Search Agent not found in main agent tools")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing integration: {e}")
        return False

def demonstrate_use_cases():
    """Demonstrate specific use cases for the google_search_agent."""
    
    print("\n🎯 Specific Use Cases")
    print("=" * 40)
    
    use_cases = [
        {
            "scenario": "BD Agent needs current funding data",
            "query": "Find recent Series A funding rounds in blockchain startups",
            "benefit": "Provides real-time funding information when APIs are unavailable"
        },
        {
            "scenario": "Marketing Agent needs current trends",
            "query": "What are the latest employer branding trends in 2024?",
            "benefit": "Gets current best practices and industry insights"
        },
        {
            "scenario": "Backend Agent needs tool information",
            "query": "Compare the latest ATS platforms for small companies",
            "benefit": "Provides current tool comparisons and reviews"
        },
        {
            "scenario": "Outreach Agent needs market data",
            "query": "What are the current hiring challenges in tech?",
            "benefit": "Gets real-time market intelligence for strategy"
        }
    ]
    
    for i, case in enumerate(use_cases, 1):
        print(f"\n{i}. {case['scenario']}")
        print(f"   Query: '{case['query']}'")
        print(f"   Benefit: {case['benefit']}")

def main():
    """Run the Google Search Agent demonstration."""
    
    print("🚀 Google Search Agent Demo")
    print("=" * 60)
    
    try:
        # Test agent creation
        success1 = demonstrate_google_search_agent()
        
        # Test fallback strategy
        demonstrate_fallback_strategy()
        
        # Test integration
        success2 = demonstrate_integration()
        
        # Show use cases
        demonstrate_use_cases()
        
        if success1 and success2:
            print("\n✅ All demonstrations completed successfully!")
            print("\n🎉 Google Search Agent is ready for use!")
            print("\nKey Features:")
            print("- Real-time information retrieval")
            print("- Fallback for other agents")
            print("- Current market data and trends")
            print("- Fact verification and research")
            print("- Integration with main recruiting agency")
        else:
            print("\n❌ Some tests failed. Please check the implementation.")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 