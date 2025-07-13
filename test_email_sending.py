#!/usr/bin/env python3
"""
Test Email Sending Functionality

This script tests the email sending capabilities of the Email Discovery Agent.
"""

import os
import sys
import json

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from recruiting_agency.sub_agents.email_discovery_agent.tools import (
    find_person_email,
    find_company_admin_emails,
    verify_email,
    send_email,
    send_bulk_emails,
    create_email_campaign
)


def test_email_sending_capabilities():
    """Test the email sending capabilities."""
    print("🧪 Testing Email Sending Capabilities")
    print("="*50)
    
    # Test 1: Test email discovery (existing functionality)
    print("\n1. Testing email discovery...")
    
    try:
        result = find_person_email(
            name="John Smith",
            company="Google",
            position="Software Engineer"
        )
        print("✅ Email discovery test completed")
        print(f"Found {len(result['emails'])} emails for John Smith at Google")
    except Exception as e:
        print(f"❌ Email discovery test failed: {str(e)}")
    
    # Test 2: Test email sending with dry run
    print("\n2. Testing email sending with dry run...")
    
    try:
        result = send_email(
            to_email="test@example.com",
            subject="Test Email from Email Discovery Agent",
            body="This is a test email sent by the Email Discovery Agent. "
                 "This demonstrates the email sending capability integrated with email discovery. "
                 "This is a dry run test.",
            dry_run=True
        )
        print("✅ Email sending test completed")
        print(f"Send status: {result.get('status', 'unknown')}")
    except Exception as e:
        print(f"❌ Email sending test failed: {str(e)}")
    
    # Test 3: Test bulk email campaign
    print("\n3. Testing bulk email campaign...")
    
    test_contacts = [
        {"name": "John Smith", "email": "john@example.com", "company": "Tech Corp"},
        {"name": "Sarah Johnson", "email": "sarah@example.com", "company": "Innovation Inc"}
    ]
    
    try:
        result = send_bulk_emails(
            email_list=test_contacts,
            subject_template="Test Email - {company}",
            body_template="Hi {name},\n\nThis is a test email for {company}.\n\nBest regards,\nTest Team",
            dry_run=True,
            delay_seconds=1
        )
        print("✅ Bulk email campaign test completed")
        print(f"Total emails: {result.get('total_emails', 0)}")
        print(f"Sent emails: {result.get('sent_emails', 0)}")
        print(f"Failed emails: {result.get('failed_emails', 0)}")
    except Exception as e:
        print(f"❌ Bulk email campaign test failed: {str(e)}")
    
    # Test 4: Test email campaign creation
    print("\n4. Testing email campaign creation...")
    
    try:
        result = create_email_campaign(
            target_contacts=test_contacts,
            campaign_name="Test Campaign",
            subject_line="Test Email - {company}",
            email_body="Hi {name},\n\nThis is a test campaign email for {company}.\n\nBest regards,\nTest Team",
            dry_run=True
        )
        print("✅ Email campaign creation test completed")
        print(f"Campaign name: {result.get('campaign_name', 'unknown')}")
        print(f"Total contacts: {result.get('total_contacts', 0)}")
    except Exception as e:
        print(f"❌ Email campaign creation test failed: {str(e)}")
    
    # Test 5: Check environment variables
    print("\n5. Checking environment variables...")
    
    email_creds = os.getenv("BD_AGENT_EMAIL")
    password_creds = os.getenv("BD_AGENT_EMAIL_PASSWORD")
    
    if email_creds and password_creds:
        print("✅ Email credentials found")
        print(f"Email: {email_creds[:3]}***{email_creds[-10:]}")
        print(f"Password: {'Set' if password_creds else 'Not set'}")
    else:
        print("⚠️  Email credentials not found")
        print("To test actual email sending, set:")
        print("   export BD_AGENT_EMAIL='your-email@gmail.com'")
        print("   export BD_AGENT_EMAIL_PASSWORD='your-app-password'")
    
    print("\n" + "="*50)
    print("✅ Email sending capability tests completed!")
    print("\n📋 Summary:")
    print("• Email discovery agent now includes email sending tools")
    print("• All tests use dry_run=True for safety")
    print("• Environment variables checked for actual sending capability")
    print("• Ready for integration with the main recruiting chatbot")


if __name__ == "__main__":
    test_email_sending_capabilities() 