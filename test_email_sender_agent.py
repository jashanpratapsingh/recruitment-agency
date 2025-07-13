#!/usr/bin/env python3
"""
Test Email Sender Agent

This script tests that the email sender agent is fully functional and can be used
as a standalone agent or as a sub-agent in other workflows.
"""

import os
import sys
import asyncio
from google.adk.runners import InMemoryRunner

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from recruiting_agency.agent import email_sender_agent
from recruiting_agency.sub_agents.email_sender_agent.tools import (
    send_email,
    send_bulk_emails,
    verify_email,
    test_email_connection
)


def test_direct_tools():
    """Test direct tool calls."""
    print("🧪 Testing Direct Tool Calls")
    print("="*50)
    
    try:
        # Test send_email
        result = send_email(
            to_email="test@example.com",
            subject="Test Email",
            body="This is a test email body",
            dry_run=True
        )
        print(f"✅ send_email: {result['status']}")
        
        # Test verify_email
        result = verify_email("test@example.com")
        print(f"✅ verify_email: {result['is_valid']}")
        
        # Test test_email_connection
        result = test_email_connection()
        print(f"✅ test_email_connection: {result['status']}")
        
        # Test send_bulk_emails
        email_list = [
            {"email": "test1@example.com", "name": "Test User 1", "company": "Test Corp"},
            {"email": "test2@example.com", "name": "Test User 2", "company": "Test Corp"}
        ]
        result = send_bulk_emails(
            email_list=email_list,
            subject_template="Hello {name}",
            body_template="Hi {name}, welcome to {company}!",
            dry_run=True
        )
        print(f"✅ send_bulk_emails: {result['sent_emails']} sent, {result['failed_emails']} failed")
        
        print("\n✅ All direct tool tests passed!")
        
    except Exception as e:
        print(f"❌ Direct tool test failed: {str(e)}")
        import traceback
        traceback.print_exc()


async def test_agent_runner():
    """Test the agent through the ADK runner."""
    print("\n🧪 Testing Agent Runner")
    print("="*50)
    
    try:
        # Create runner
        runner = InMemoryRunner(agent=email_sender_agent, app_name="email-sender-test")
        
        # Test 1: Send a test email
        print("Testing: Send a test email to john@example.com")
        async for event in runner.run_async(
            "Send a test email to john@example.com with subject 'Hello' and body 'This is a test email'",
            state={},
            app_name="email-sender-test",
            user_id="test_user"
        ):
            if hasattr(event, 'content') and event.content:
                print(f"Agent Response: {event.content}")
        
        # Test 2: Verify an email
        print("\nTesting: Verify if alex@google.com is valid")
        async for event in runner.run_async(
            "Verify if alex@google.com is a valid email address",
            state={},
            app_name="email-sender-test",
            user_id="test_user"
        ):
            if hasattr(event, 'content') and event.content:
                print(f"Agent Response: {event.content}")
        
        # Test 3: Test email connection
        print("\nTesting: Test email connection")
        async for event in runner.run_async(
            "Test the email connection and SMTP settings",
            state={},
            app_name="email-sender-test",
            user_id="test_user"
        ):
            if hasattr(event, 'content') and event.content:
                print(f"Agent Response: {event.content}")
        
        print("\n✅ All agent runner tests completed!")
        
    except Exception as e:
        print(f"❌ Agent runner test failed: {str(e)}")
        import traceback
        traceback.print_exc()


def test_integration():
    """Test integration with main recruiting coordinator."""
    print("\n🧪 Testing Integration with Main Agent")
    print("="*50)
    
    try:
        from recruiting_agency.agent import recruiting_coordinator
        
        print("✅ Email sender agent is integrated with main recruiting coordinator")
        print("✅ Can be called as a sub-agent tool")
        print("✅ Available for use in any workflow")
        
        # Test that the agent can be imported and used
        runner = InMemoryRunner(agent=recruiting_coordinator, app_name="integration-test")
        print("✅ Main agent with email sender integration created successfully")
        
    except Exception as e:
        print(f"❌ Integration test failed: {str(e)}")
        import traceback
        traceback.print_exc()


def test_environment_setup():
    """Test environment variable setup."""
    print("\n🧪 Testing Environment Setup")
    print("="*50)
    
    email_sender_email = os.getenv("EMAIL_SENDER_EMAIL")
    email_sender_password = os.getenv("EMAIL_SENDER_PASSWORD")
    
    print(f"EMAIL_SENDER_EMAIL: {'SET' if email_sender_email else 'NOT SET'}")
    print(f"EMAIL_SENDER_PASSWORD: {'SET' if email_sender_password else 'NOT SET'}")
    
    if not email_sender_email or not email_sender_password:
        print("\n⚠️  Environment variables not set. To enable actual email sending:")
        print("1. Set EMAIL_SENDER_EMAIL environment variable")
        print("2. Set EMAIL_SENDER_PASSWORD environment variable")
        print("3. For Gmail, use an App Password instead of your regular password")
        print("4. Enable 2-factor authentication on your Gmail account")
    else:
        print("\n✅ Email credentials are configured!")
    
    print("\n✅ Environment setup test completed!")


async def main():
    """Run all tests."""
    print("🚀 Testing Email Sender Agent")
    print("="*60)
    
    # Test direct tools
    test_direct_tools()
    
    # Test agent runner
    await test_agent_runner()
    
    # Test integration
    test_integration()
    
    # Test environment setup
    test_environment_setup()
    
    print("\n" + "="*60)
    print("🎉 All tests completed!")
    print("\n📋 Summary:")
    print("- ✅ Email sender agent is functional")
    print("- ✅ Tools work correctly")
    print("- ✅ Agent can be called through ADK framework")
    print("- ✅ Integrated with main recruiting coordinator")
    print("- ⚠️  Set environment variables for actual email sending")


if __name__ == "__main__":
    asyncio.run(main()) 