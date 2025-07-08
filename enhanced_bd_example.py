# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Enhanced example demonstrating personalized message generation and email sending."""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from recruiting_agency.sub_agents.bd_agent.tools import (
    fetch_recent_funding_rounds,
    filter_blockchain_companies,
    personalize_outreach,
    send_personalized_emails,
    generate_personalized_message
)


def demonstrate_personalized_messages():
    """Demonstrate personalized message generation for individual companies."""
    
    print("🎯 Personalized Message Generation")
    print("=" * 50)
    
    # Get sample companies
    companies = fetch_recent_funding_rounds()
    
    # Generate personalized messages for each company
    for company in companies:
        print(f"\n📧 {company['company_name']}")
        print("-" * 30)
        
        # Generate email message
        email_message = generate_personalized_message(company, "email")
        print(f"Subject: {email_message['subject']}")
        print(f"Body Preview: {email_message['body'][:200]}...")
        
        # Generate LinkedIn message
        linkedin_message = generate_personalized_message(company, "linkedin")
        print(f"LinkedIn Preview: {linkedin_message['body'][:150]}...")
        
        print(f"Key People: {', '.join(company.get('key_people', []))}")


def demonstrate_email_sending():
    """Demonstrate email sending functionality."""
    
    print("\n📬 Email Sending Demonstration")
    print("=" * 50)
    
    # Get companies and create outreach strategies
    companies = fetch_recent_funding_rounds()
    target_companies = filter_blockchain_companies(companies, min_funding=20000000)
    outreach_strategies = personalize_outreach(target_companies)
    
    print(f"Generated {len(outreach_strategies)} outreach strategies")
    
    # Send emails (dry run by default)
    print("\n🚀 Sending Personalized Emails (Dry Run)")
    print("-" * 40)
    
    email_results = send_personalized_emails(
        outreach_strategies=outreach_strategies,
        dry_run=True  # Set to False to actually send emails
    )
    
    for result in email_results:
        status_icon = "✅" if result["status"] == "success" else "⚠️"
        print(f"{status_icon} {result['company_name']}: {result['message']}")
    
    # Show email configuration
    print("\n📧 Email Configuration")
    print("-" * 20)
    print("To enable actual email sending:")
    print("1. Set environment variables:")
    print("   export BD_AGENT_EMAIL='your-email@gmail.com'")
    print("   export BD_AGENT_EMAIL_PASSWORD='your-app-password'")
    print("2. Set dry_run=False in send_personalized_emails()")
    print("3. Configure SMTP settings if needed")


def demonstrate_complete_workflow():
    """Demonstrate the complete enhanced workflow."""
    
    print("\n🔄 Complete Enhanced BD Workflow")
    print("=" * 50)
    
    # Step 1: Fetch companies
    print("\n1️⃣ Fetching Recent Funding Rounds")
    companies = fetch_recent_funding_rounds(sector="blockchain", min_funding_amount=10000000)
    print(f"   Found {len(companies)} companies with recent funding")
    
    # Step 2: Filter companies
    print("\n2️⃣ Filtering Target Companies")
    target_companies = filter_blockchain_companies(
        companies=companies,
        min_funding=20000000,
        target_stages=["Series A", "Series B"]
    )
    print(f"   Filtered to {len(target_companies)} target companies")
    
    # Step 3: Generate personalized outreach
    print("\n3️⃣ Creating Personalized Outreach")
    outreach_strategies = personalize_outreach(
        target_companies=target_companies,
        message_types=["email", "linkedin"]
    )
    print(f"   Created {len(outreach_strategies)} personalized strategies")
    
    # Step 4: Send emails
    print("\n4️⃣ Sending Personalized Emails")
    email_results = send_personalized_emails(outreach_strategies, dry_run=True)
    successful_emails = sum(1 for result in email_results if result["status"] in ["success", "dry_run"])
    print(f"   Successfully processed {successful_emails}/{len(email_results)} emails")
    
    # Summary
    print("\n📊 Workflow Summary")
    print("-" * 20)
    print(f"• Companies identified: {len(companies)}")
    print(f"• Target companies: {len(target_companies)}")
    print(f"• Outreach strategies: {len(outreach_strategies)}")
    print(f"• Emails processed: {len(email_results)}")
    
    # Show sample personalized message
    if outreach_strategies:
        sample_strategy = outreach_strategies[0]
        sample_email = sample_strategy["generated_messages"]["email"]
        print(f"\n📝 Sample Personalized Email for {sample_strategy['company_name']}:")
        print(f"Subject: {sample_email['subject']}")
        print(f"Body: {sample_email['body'][:300]}...")


def show_email_templates():
    """Show the email templates and customization options."""
    
    print("\n📋 Email Templates and Customization")
    print("=" * 50)
    
    # Sample company for demonstration
    sample_company = {
        "company_name": "Example Blockchain Co",
        "funding_amount": 50000000,
        "funding_round": "Series B",
        "description": "leading DeFi protocol for decentralized lending",
        "hiring_plans": "scaling engineering team by 50%",
        "key_people": ["John Doe", "Jane Smith"]
    }
    
    print("\n🎯 Email Template Features:")
    print("• Personalized greeting with key decision maker")
    print("• Congratulatory message referencing funding round")
    print("• Company-specific value proposition")
    print("• Call-to-action for meeting")
    print("• Professional signature")
    
    print("\n🔧 LinkedIn Template Features:")
    print("• Shorter, more casual tone")
    print("• Emoji usage for engagement")
    print("• Direct call-to-action")
    print("• Professional but approachable")
    
    print("\n⚙️ Customization Options:")
    print("• Company-specific messaging")
    print("• Funding amount and round personalization")
    print("• Industry-specific value propositions")
    print("• Multiple outreach channels")
    print("• A/B testing capabilities")


if __name__ == "__main__":
    print("🚀 Enhanced BD Agent - Personalized Outreach Demo")
    print("=" * 60)
    
    demonstrate_personalized_messages()
    demonstrate_email_sending()
    demonstrate_complete_workflow()
    show_email_templates()
    
    print("\n✅ Enhanced BD Agent demonstration completed!")
    print("\n💡 Next Steps:")
    print("1. Configure email credentials for production use")
    print("2. Customize message templates for your brand")
    print("3. Integrate with real funding data APIs")
    print("4. Set up CRM integration for tracking") 