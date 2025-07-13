#!/usr/bin/env python3
"""
Email Discovery and Sending Example

This example demonstrates how to:
1. Find email addresses for individuals and companies
2. Verify email addresses
3. Send individual emails
4. Send bulk emails and campaigns
5. Create follow-up sequences

Usage:
    python email_discovery_and_sending_example.py
"""

import os
import sys
import json
from typing import List, Dict, Any

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from recruiting_agency.agent import recruiting_coordinator_agent
from recruiting_agency.sub_agents.email_discovery_agent.agent import email_discovery_agent


def setup_environment():
    """Set up environment variables for email sending."""
    print("🔧 Setting up environment...")
    
    # Check if email credentials are set
    if not os.getenv("BD_AGENT_EMAIL") or not os.getenv("BD_AGENT_EMAIL_PASSWORD"):
        print("⚠️  Email credentials not found!")
        print("Please set the following environment variables:")
        print("   export BD_AGENT_EMAIL='your-email@gmail.com'")
        print("   export BD_AGENT_EMAIL_PASSWORD='your-app-password'")
        print("\nNote: For Gmail, you need to use an App Password, not your regular password.")
        print("Learn more: https://support.google.com/accounts/answer/185833")
        return False
    
    print("✅ Email credentials found")
    return True


def example_1_find_and_verify_emails():
    """Example 1: Find and verify individual emails."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Find and Verify Individual Emails")
    print("="*60)
    
    # Test cases
    test_cases = [
        {
            "name": "John Smith",
            "company": "Google",
            "position": "Software Engineer"
        },
        {
            "name": "Sarah Johnson",
            "company": "Microsoft",
            "position": "Product Manager"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n🔍 Finding email for {case['name']} at {case['company']}...")
        
        # Find email
        response = email_discovery_agent.run(
            f"Find the email address for {case['name']} who works as {case['position']} at {case['company']}. "
            f"Provide confidence scores and verification status."
        )
        
        print(f"📧 Email Discovery Results:")
        print(json.dumps(response, indent=2))
        
        # If emails found, verify them
        if response.get("email_discovery_output"):
            emails = response["email_discovery_output"].get("emails", [])
            if emails:
                print(f"\n✅ Found {len(emails)} email(s). Verifying...")
                
                for email in emails[:2]:  # Verify first 2 emails
                    verify_response = email_discovery_agent.run(
                        f"Verify the email address: {email}"
                    )
                    print(f"🔍 Verification for {email}:")
                    print(json.dumps(verify_response, indent=2))


def example_2_find_company_admin_emails():
    """Example 2: Find company admin emails."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Find Company Admin Emails")
    print("="*60)
    
    companies = ["Tesla", "SpaceX", "Netflix"]
    
    for company in companies:
        print(f"\n🏢 Finding admin emails for {company}...")
        
        response = email_discovery_agent.run(
            f"Find admin and contact email addresses for {company}. "
            f"Include general contact emails and department-specific emails."
        )
        
        print(f"📧 Admin Email Results for {company}:")
        print(json.dumps(response, indent=2))


def example_3_send_individual_email():
    """Example 3: Send an individual email."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Send Individual Email")
    print("="*60)
    
    # Test email (use a real email for actual sending)
    test_email = "test@example.com"  # Replace with real email for testing
    
    print(f"📤 Sending test email to {test_email}...")
    
    response = email_discovery_agent.run(
        f"Send an email to {test_email} with the following details:\n"
        f"Subject: Test Email from Email Discovery Agent\n"
        f"Body: This is a test email sent by the Email Discovery Agent. "
        f"This demonstrates the email sending capability integrated with email discovery.\n"
        f"Use dry_run=True for safety."
    )
    
    print("📧 Email Send Results:")
    print(json.dumps(response, indent=2))


def example_4_bulk_email_campaign():
    """Example 4: Create and send a bulk email campaign."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Bulk Email Campaign")
    print("="*60)
    
    # Sample contact list (in real usage, these would be found emails)
    contacts = [
        {
            "name": "John Smith",
            "email": "john.smith@example.com",
            "company": "Tech Corp",
            "position": "CTO"
        },
        {
            "name": "Sarah Johnson",
            "email": "sarah.johnson@example.com",
            "company": "Innovation Inc",
            "position": "VP Engineering"
        },
        {
            "name": "Mike Davis",
            "email": "mike.davis@example.com",
            "company": "StartupXYZ",
            "position": "Founder"
        }
    ]
    
    print(f"📧 Creating email campaign for {len(contacts)} contacts...")
    
    campaign_response = email_discovery_agent.run(
        f"Create an email campaign with the following details:\n"
        f"Campaign Name: Recruiting Partnership Outreach\n"
        f"Contacts: {json.dumps(contacts)}\n"
        f"Subject Template: Partnership Opportunity - {{company}}\n"
        f"Body Template: Hi {{name}},\n\n"
        f"I hope this email finds you well. I came across {{company}} and was impressed by your work.\n\n"
        f"I'm reaching out to discuss potential recruiting partnership opportunities that could benefit {{company}}.\n\n"
        f"Would you be interested in a brief call to explore this further?\n\n"
        f"Best regards,\n"
        f"Recruiting Team\n\n"
        f"Use dry_run=True for safety and include a 2-second delay between emails."
    )
    
    print("📧 Campaign Results:")
    print(json.dumps(campaign_response, indent=2))


def example_5_find_and_send_workflow():
    """Example 5: Complete workflow - find emails and send outreach."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Complete Workflow - Find and Send")
    print("="*60)
    
    # Step 1: Find emails for target companies
    target_companies = ["Tesla", "SpaceX"]
    
    all_contacts = []
    
    for company in target_companies:
        print(f"\n🔍 Finding contacts for {company}...")
        
        # Find admin emails
        admin_response = email_discovery_agent.run(
            f"Find admin and contact email addresses for {company}. "
            f"Focus on HR, recruiting, and general contact emails."
        )
        
        # Find individual emails for key positions
        individual_response = email_discovery_agent.run(
            f"Find email addresses for people with these positions at {company}:\n"
            f"- HR Director\n"
            f"- Head of Talent Acquisition\n"
            f"- VP of Engineering\n"
            f"- CTO"
        )
        
        # Combine results (simplified for example)
        contacts = []
        if admin_response.get("email_discovery_output"):
            admin_emails = admin_response["email_discovery_output"].get("admin_emails", [])
            for email in admin_emails[:2]:  # Take first 2 admin emails
                contacts.append({
                    "name": f"Contact at {company}",
                    "email": email,
                    "company": company,
                    "position": "Admin Contact"
                })
        
        if individual_response.get("email_discovery_output"):
            individual_emails = individual_response["email_discovery_output"].get("emails", [])
            for email in individual_emails[:2]:  # Take first 2 individual emails
                contacts.append({
                    "name": f"Professional at {company}",
                    "email": email,
                    "company": company,
                    "position": "Key Position"
                })
        
        all_contacts.extend(contacts)
        print(f"✅ Found {len(contacts)} contacts for {company}")
    
    # Step 2: Send personalized outreach
    if all_contacts:
        print(f"\n📤 Sending personalized outreach to {len(all_contacts)} contacts...")
        
        outreach_response = email_discovery_agent.run(
            f"Send personalized outreach emails to these contacts:\n"
            f"{json.dumps(all_contacts, indent=2)}\n\n"
            f"Use this template:\n"
            f"Subject: Partnership Opportunity - {{company}}\n"
            f"Body: Hi {{name}},\n\n"
            f"I hope this email finds you well. I've been following {{company}}'s impressive work and wanted to reach out.\n\n"
            f"We specialize in connecting top talent with innovative companies like yours. "
            f"Would you be interested in discussing potential partnership opportunities?\n\n"
            f"Best regards,\n"
            f"Recruiting Team\n\n"
            f"Use dry_run=True for safety."
        )
        
        print("📧 Outreach Results:")
        print(json.dumps(outreach_response, indent=2))
    else:
        print("❌ No contacts found for outreach")


def example_6_email_verification_batch():
    """Example 6: Batch email verification."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Batch Email Verification")
    print("="*60)
    
    # Sample emails to verify
    test_emails = [
        "john.doe@gmail.com",
        "contact@tesla.com",
        "hr@spacex.com",
        "invalid-email-format",
        "test@nonexistentdomain12345.com"
    ]
    
    print(f"🔍 Verifying {len(test_emails)} email addresses...")
    
    for email in test_emails:
        print(f"\n🔍 Verifying: {email}")
        
        response = email_discovery_agent.run(
            f"Verify the email address: {email}. "
            f"Provide detailed verification results including format validation, "
            f"domain validation, and deliverability status."
        )
        
        print(f"✅ Verification Results:")
        print(json.dumps(response, indent=2))


def main():
    """Run all examples."""
    print("🚀 Email Discovery and Sending Examples")
    print("="*60)
    
    # Check environment setup
    if not setup_environment():
        print("\n❌ Environment not properly configured. Please set up email credentials.")
        return
    
    try:
        # Run examples
        example_1_find_and_verify_emails()
        example_2_find_company_admin_emails()
        example_3_send_individual_email()
        example_4_bulk_email_campaign()
        example_5_find_and_send_workflow()
        example_6_email_verification_batch()
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("="*60)
        
        print("\n📋 Summary of Capabilities Demonstrated:")
        print("• Individual email discovery and verification")
        print("• Company admin email finding")
        print("• Individual email sending")
        print("• Bulk email campaigns")
        print("• Complete find-and-send workflows")
        print("• Batch email verification")
        
        print("\n💡 Tips for Production Use:")
        print("• Always use dry_run=True for testing")
        print("• Verify email addresses before sending")
        print("• Include delays between bulk emails")
        print("• Use personalized content with template variables")
        print("• Monitor email sending limits and rates")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 