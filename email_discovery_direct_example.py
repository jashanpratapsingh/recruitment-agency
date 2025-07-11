#!/usr/bin/env python3
"""
Direct Email Discovery Agent Example

This script shows how to use the email discovery agent directly.
"""

import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from recruiting_agency.sub_agents.email_discovery_agent import email_discovery_agent
from recruiting_agency.sub_agents.email_discovery_agent.tools import (
    find_person_email,
    find_company_admin_emails,
    verify_email
)

def demonstrate_direct_usage():
    """Demonstrate using the email discovery agent directly."""
    print("🔍 Direct Email Discovery Agent Usage")
    print("=" * 50)
    
    # Example 1: Find individual email
    print("\n1️⃣ Finding email for John Smith at Google")
    result = find_person_email(
        name="John Smith",
        company="Google",
        position="Software Engineer"
    )
    
    print(f"   Found {len(result['emails'])} potential emails:")
    for i, email in enumerate(result['emails'][:3], 1):
        print(f"   {i}. {email}")
    
    # Example 2: Find company admin emails
    print("\n2️⃣ Finding admin emails for Microsoft")
    admin_result = find_company_admin_emails(
        company="Microsoft",
        include_departments=True
    )
    
    print(f"   General emails: {len(admin_result['general_emails'])}")
    print(f"   Department emails: {len(admin_result['department_emails'])}")
    
    # Show some examples
    print("   Sample general emails:")
    for email in admin_result['general_emails'][:3]:
        print(f"     • {email}")
    
    print("   Sample department emails:")
    for email in admin_result['department_emails'][:3]:
        print(f"     • {email}")
    
    # Example 3: Verify an email
    print("\n3️⃣ Verifying an email address")
    test_email = "john.doe@google.com"
    verify_result = verify_email(test_email)
    
    print(f"   Email: {test_email}")
    print(f"   Format valid: {verify_result['is_valid_format']}")
    print(f"   Confidence: {verify_result['confidence_score']}%")
    print(f"   Methods: {', '.join(verify_result['verification_methods'])}")

def demonstrate_agent_usage():
    """Demonstrate using the agent directly."""
    print("\n🤖 Using Email Discovery Agent Directly")
    print("=" * 50)
    
    print(f"Agent name: {email_discovery_agent.name}")
    print(f"Agent model: {email_discovery_agent.model}")
    print(f"Number of tools: {len(email_discovery_agent.tools)}")
    
    # Show available tools
    print("\nAvailable tools:")
    for i, tool in enumerate(email_discovery_agent.tools, 1):
        print(f"   {i}. {tool.func.__name__}")
    
    print("\n✅ Email discovery agent is ready to use!")

def main():
    """Main demonstration function."""
    print("🚀 Direct Email Discovery Agent Example")
    print("=" * 60)
    
    try:
        demonstrate_direct_usage()
        demonstrate_agent_usage()
        
        print("\n✅ All demonstrations completed successfully!")
        print("\n💡 You can now use the email discovery agent directly or through the main agent.")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 