#!/usr/bin/env python3
"""
Example script demonstrating the BD Agent workflow for blockchain company identification.
"""

import os
import sys
from typing import List, Dict, Any

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'recruiting_agency'))

from recruiting_agency.sub_agents.bd_agent.tools import (
    fetch_recent_funding_rounds,
    filter_blockchain_companies,
    personalize_outreach,
    send_personalized_emails,
    generate_personalized_message
)

def demonstrate_bd_agent_workflow():
    """Demonstrate the complete BD Agent workflow."""
    
    print("🚀 BD Agent - Blockchain Company Identification Workflow")
    print("=" * 60)
    
    # Step 1: Fetch recent funding rounds
    print("\n📊 Step 1: Fetching Recent Funding Rounds")
    print("-" * 40)
    
    companies = fetch_recent_funding_rounds(
        sector="blockchain",
        min_funding_amount=10000000,  # $10M minimum
        timeframe_days=90
    )
    
    print(f"Found {len(companies)} companies with recent funding:")
    for company in companies:
        print(f"  • {company['company_name']} - ${company['funding_amount']:,} ({company['funding_round']})")
    
    # Step 2: Filter target companies
    print("\n🎯 Step 2: Filtering Target Companies")
    print("-" * 40)
    
    target_companies = filter_blockchain_companies(
        companies=companies,
        min_funding=20000000,  # $20M minimum
        target_stages=["Series A", "Series B", "Series C"]
    )
    
    print(f"Filtered to {len(target_companies)} target companies:")
    for company in target_companies:
        print(f"  • {company['company_name']} - {company['location']} - {company.get('hiring_plans', 'Aggressive hiring for engineering and product roles')}")
    
    # Step 3: Create personalized outreach
    print("\n💬 Step 3: Creating Personalized Outreach")
    print("-" * 40)
    
    outreach_strategies = personalize_outreach(
        target_companies=target_companies,
        message_types=["email", "linkedin"]
    )
    
    print(f"Created {len(outreach_strategies)} personalized outreach strategies:")
    
    for strategy in outreach_strategies:
        print(f"\n  📧 {strategy['company_name']}:")
        print(f"     Funding: {strategy['funding_info']}")
        print(f"     Value Prop: {strategy['value_proposition']}")
        
        # Show email message preview
        if 'email' in strategy['generated_messages']:
            email_msg = strategy['generated_messages']['email']
            print(f"     Subject: {email_msg['subject']}")
            print(f"     Message: {email_msg['body'][:100]}...")
        
        # Show LinkedIn message preview
        if 'linkedin' in strategy['generated_messages']:
            linkedin_msg = strategy['generated_messages']['linkedin']
            print(f"     LinkedIn: {linkedin_msg['body'][:100]}...")
    
    # Step 4: Send personalized emails (dry run)
    print("\n📧 Step 4: Sending Personalized Emails (Dry Run)")
    print("-" * 40)
    
    email_results = send_personalized_emails(
        outreach_strategies=outreach_strategies,
        dry_run=True  # Don't actually send emails
    )
    
    print(f"Email results for {len(email_results)} companies:")
    for result in email_results:
        status_icon = "✅" if result['status'] == 'dry_run' else "❌"
        print(f"  {status_icon} {result['company_name']}: {result['status']}")
    
    # Step 5: Generate sample personalized message
    print("\n✉️  Step 5: Sample Personalized Message")
    print("-" * 40)
    
    if target_companies:
        sample_company = target_companies[0]
        email_message = generate_personalized_message(sample_company, "email")
        
        print(f"Sample email for {sample_company['company_name']}:")
        print(f"Subject: {email_message['subject']}")
        print(f"Body: {email_message['body']}")
    
    print("\n✅ BD Agent workflow completed successfully!")
    print("\nKey Features Demonstrated:")
    print("- Real-time funding data fetching (with API fallbacks)")
    print("- Intelligent company filtering based on criteria")
    print("- LLM-powered personalized message generation")
    print("- Multi-channel outreach strategies (email + LinkedIn)")
    print("- Automated email sending capabilities")
    print("- Comprehensive error handling and logging")

def demonstrate_api_integration():
    """Demonstrate API integration capabilities."""
    
    print("\n🔌 API Integration Demo")
    print("=" * 40)
    
    # Check available APIs
    api_keys = {
        "TRACXN_API_KEY": os.getenv("TRACXN_API_KEY"),
        "CRUNCHBASE_API_KEY": os.getenv("CRUNCHBASE_API_KEY"),
        "DEALROOM_API_KEY": os.getenv("DEALROOM_API_KEY"),
        "PITCHBOOK_API_KEY": os.getenv("PITCHBOOK_API_KEY")
    }
    
    print("API Key Status:")
    for api_name, key in api_keys.items():
        status = "✅ Available" if key else "❌ Not configured"
        print(f"  {api_name}: {status}")
    
    if not any(api_keys.values()):
        print("\n💡 To enable real API data:")
        print("  1. Get API keys from the respective providers")
        print("  2. Set environment variables:")
        print("     export TRACXN_API_KEY='your_key'")
        print("     export CRUNCHBASE_API_KEY='your_key'")
        print("     export DEALROOM_API_KEY='your_key'")
        print("     export PITCHBOOK_API_KEY='your_key'")

def main():
    """Run the BD Agent demonstration."""
    
    try:
        demonstrate_bd_agent_workflow()
        demonstrate_api_integration()
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 