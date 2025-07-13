#!/usr/bin/env python3
"""
Email Sending Workflow Example

This example demonstrates how the main recruiting coordinator agent should handle
email sending requests by coordinating between email discovery and email sender agents.
"""

import os
import sys
import asyncio
from google.adk.runners import InMemoryRunner

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from recruiting_agency.agent import recruiting_coordinator
from recruiting_agency.sub_agents.email_discovery_agent.tools import find_person_email, verify_email
from recruiting_agency.sub_agents.email_sender_agent.tools import send_email, send_bulk_emails


def demonstrate_email_workflow():
    """Demonstrate the complete email sending workflow."""
    print("🚀 Email Sending Workflow Demonstration")
    print("="*60)
    
    # Step 1: Find email addresses
    print("\n📧 Step 1: Email Discovery")
    print("-" * 30)
    
    # Find email for Alex Sandu at Google
    print("Finding email for Alex Sandu at Google...")
    email_result = find_person_email("Alex Sandu", "Google")
    
    if email_result["emails"]:
        email = email_result["emails"][0]
        confidence = email_result["confidence_scores"][0]
        print(f"✅ Found email: {email} (confidence: {confidence}%)")
        
        # Step 2: Verify email
        print("\n🔍 Step 2: Email Verification")
        print("-" * 30)
        verify_result = verify_email(email)
        print(f"Email verification: {verify_result.get('is_valid', False)}")
        
        if verify_result.get("is_valid", False):
            # Step 3: Send email
            print("\n📤 Step 3: Send Email")
            print("-" * 30)
            
            # Send a test email
            send_result = send_email(
                to_email=email,
                subject="Hello from Recruiting Agency",
                body=f"""Hi Alex,

I hope this email finds you well. I'm reaching out from our recruiting agency to discuss potential opportunities.

We've been impressed with your work at Google and would love to connect with you about exciting opportunities in the tech industry.

Would you be interested in a brief conversation about your career goals and potential opportunities?

Best regards,
Recruiting Team""",
                dry_run=True  # Set to False to actually send
            )
            
            print(f"Email send status: {send_result['status']}")
            print(f"Subject: {send_result['subject']}")
            print(f"To: {send_result['to_email']}")
            
        else:
            print("❌ Email verification failed, cannot send email")
    else:
        print("❌ No email found for Alex Sandu at Google")


def demonstrate_bulk_email_workflow():
    """Demonstrate bulk email sending workflow."""
    print("\n\n📧 Bulk Email Workflow Demonstration")
    print("="*60)
    
    # Step 1: Find multiple email addresses
    print("\n📧 Step 1: Bulk Email Discovery")
    print("-" * 30)
    
    contacts = [
        {"name": "Alex Sandu", "company": "Google"},
        {"name": "Sarah Johnson", "company": "Microsoft"},
        {"name": "Mike Chen", "company": "Apple"}
    ]
    
    email_list = []
    for contact in contacts:
        print(f"Finding email for {contact['name']} at {contact['company']}...")
        result = find_person_email(contact["name"], contact["company"])
        
        if result["emails"]:
            email = result["emails"][0]
            confidence = result["confidence_scores"][0]
            print(f"✅ Found: {email} (confidence: {confidence}%)")
            
            email_list.append({
                "email": email,
                "name": contact["name"],
                "company": contact["company"]
            })
        else:
            print(f"❌ No email found for {contact['name']}")
    
    # Step 2: Send bulk emails
    if email_list:
        print(f"\n📤 Step 2: Send Bulk Emails ({len(email_list)} recipients)")
        print("-" * 30)
        
        bulk_result = send_bulk_emails(
            email_list=email_list,
            subject_template="Exciting Opportunity at {company}",
            body_template="""Hi {name},

I hope you're doing well! I'm reaching out from our recruiting agency because we have some exciting opportunities that might interest you.

We've been following your work at {company} and believe you could be a great fit for some of our client companies.

Would you be interested in a brief conversation about potential opportunities?

Best regards,
Recruiting Team""",
            dry_run=True  # Set to False to actually send
        )
        
        print(f"Bulk email results:")
        print(f"- Total emails: {bulk_result['total_emails']}")
        print(f"- Sent: {bulk_result['sent_emails']}")
        print(f"- Failed: {bulk_result['failed_emails']}")
        
        for i, result in enumerate(bulk_result['email_results']):
            print(f"  {i+1}. {result['to_email']}: {result['status']}")
    else:
        print("❌ No valid emails found for bulk sending")


def demonstrate_agent_coordination():
    """Demonstrate how the main agent should coordinate email operations."""
    print("\n\n🤖 Agent Coordination Demonstration")
    print("="*60)
    
    print("""
The main recruiting coordinator agent should handle email requests like this:

User: "Send an email to Alex Sandu at Google about a job opportunity"

Agent Response:
1. "I'll help you send an email to Alex Sandu at Google. Let me first find his email address."
2. [Calls email_discovery_agent to find email]
3. "I found Alex's email: alex@google.com (confidence: 85%)"
4. "Now let me verify this email address is valid."
5. [Calls email_discovery_agent to verify email]
6. "Email verification successful. Now I'll send the email."
7. [Calls email_sender_agent to send email]
8. "Email sent successfully to alex@google.com with subject 'Job Opportunity'"

This demonstrates proper coordination between:
- email_discovery_agent (for finding and verifying emails)
- email_sender_agent (for sending emails)
- Main coordinator (for orchestrating the workflow)
""")


def main():
    """Run all demonstrations."""
    print("🎯 Email Sending Workflow Examples")
    print("="*60)
    
    # Demonstrate individual email workflow
    demonstrate_email_workflow()
    
    # Demonstrate bulk email workflow
    demonstrate_bulk_email_workflow()
    
    # Demonstrate agent coordination
    demonstrate_agent_coordination()
    
    print("\n" + "="*60)
    print("✅ All demonstrations completed!")
    print("\n📋 Key Points:")
    print("- The main agent should coordinate between email_discovery_agent and email_sender_agent")
    print("- Always verify emails before sending")
    print("- Use dry_run=True for testing")
    print("- Provide clear status updates to users")
    print("- Handle errors gracefully")


if __name__ == "__main__":
    main() 