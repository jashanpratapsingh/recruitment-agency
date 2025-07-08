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

"""Example demonstrating BD Agent with only Tracxn API."""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from recruiting_agency.sub_agents.bd_agent.tools import (
    fetch_recent_funding_rounds,
    fetch_tracxn_funding_data,
    filter_blockchain_companies,
    personalize_outreach,
    send_personalized_emails
)


def demonstrate_tracxn_only_workflow():
    """Demonstrate the complete BD Agent workflow using only Tracxn API."""
    
    print("🚀 BD Agent with Tracxn API Only")
    print("=" * 50)
    
    # Check if Tracxn API key is available
    tracxn_api_key = os.getenv("TRACXN_API_KEY")
    if not tracxn_api_key:
        print("❌ TRACXN_API_KEY not found!")
        print("Please set your Tracxn API key:")
        print("export TRACXN_API_KEY='your_tracxn_api_key'")
        return
    
    print("✅ Tracxn API key found!")
    
    # Step 1: Fetch funding data from Tracxn
    print("\n📊 Step 1: Fetching funding data from Tracxn...")
    companies = fetch_recent_funding_rounds(
        sector="blockchain",
        min_funding_amount=10000000,  # $10M minimum
        timeframe_days=90,
        company_stage="Series A"  # Focus on Series A companies
    )
    
    print(f"Found {len(companies)} companies with recent funding")
    
    # Step 2: Filter companies based on criteria
    print("\n🎯 Step 2: Filtering companies...")
    target_companies = filter_blockchain_companies(
        companies=companies,
        min_funding=20000000,  # $20M minimum
        target_stages=["Series A", "Series B"],
        locations=["San Francisco", "New York", "London", "Singapore"],
        remote_friendly=True
    )
    
    print(f"Filtered to {len(target_companies)} target companies")
    
    # Step 3: Create personalized outreach
    print("\n✉️ Step 3: Creating personalized outreach...")
    outreach_strategies = personalize_outreach(
        target_companies=target_companies,
        message_types=["email", "linkedin"]
    )
    
    print(f"Created {len(outreach_strategies)} outreach strategies")
    
    # Step 4: Send personalized emails (dry run)
    print("\n📧 Step 4: Sending personalized emails (dry run)...")
    email_results = send_personalized_emails(
        outreach_strategies=outreach_strategies,
        dry_run=True  # Set to False to actually send emails
    )
    
    # Display results
    print("\n📈 Results Summary:")
    print(f"• Total companies found: {len(companies)}")
    print(f"• Target companies after filtering: {len(target_companies)}")
    print(f"• Outreach strategies created: {len(outreach_strategies)}")
    print(f"• Emails processed: {len(email_results)}")
    
    # Show sample companies
    if target_companies:
        print("\n🎯 Top Target Companies:")
        for i, company in enumerate(target_companies[:3], 1):
            print(f"\n   {i}. {company['company_name']}")
            print(f"      Funding: ${company['funding_amount']:,} ({company['funding_round']})")
            print(f"      Location: {company.get('location', 'N/A')}")
            print(f"      Hiring Plans: {company.get('hiring_plans', 'N/A')}")
    
    # Show sample outreach strategy
    if outreach_strategies:
        print("\n✉️ Sample Outreach Strategy:")
        strategy = outreach_strategies[0]
        print(f"   Company: {strategy['company_name']}")
        print(f"   Funding Info: {strategy['funding_info']}")
        print(f"   Value Proposition: {strategy['value_proposition']}")
        print(f"   Outreach Channels: {', '.join(strategy['outreach_channels'])}")
        
        # Show sample email
        email_message = strategy['generated_messages'].get('email', {})
        if email_message:
            print(f"\n   Sample Email Subject: {email_message['subject']}")
            print(f"   Sample Email Body: {email_message['body'][:200]}...")
    
    return {
        "companies": companies,
        "target_companies": target_companies,
        "outreach_strategies": outreach_strategies,
        "email_results": email_results
    }


def demonstrate_tracxn_api_features():
    """Demonstrate specific Tracxn API features."""
    
    print("\n🔧 Tracxn API Features")
    print("=" * 30)
    
    print("\n1. **Sector-Specific Filtering:**")
    print("   • Blockchain companies")
    print("   • DeFi protocols")
    print("   • Web3 infrastructure")
    print("   • NFT platforms")
    
    print("\n2. **Funding Stage Filtering:**")
    print("   • Seed rounds")
    print("   • Series A, B, C+")
    print("   • Growth equity")
    print("   • IPO preparation")
    
    print("\n3. **Geographic Coverage:**")
    print("   • Global startup ecosystem")
    print("   • Regional market insights")
    print("   • Emerging markets data")
    
    print("\n4. **Data Quality:**")
    print("   • Real-time funding data")
    print("   • Investor information")
    print("   • Company metrics")
    print("   • Market trends")


def demonstrate_configuration():
    """Show how to configure for Tracxn-only usage."""
    
    print("\n⚙️ Configuration for Tracxn-Only Usage")
    print("=" * 45)
    
    print("\n1. **Environment Variables:**")
    print("   ```bash")
    print("   # Required")
    print("   export TRACXN_API_KEY='your_tracxn_api_key'")
    print("   ")
    print("   # Optional (for email sending)")
    print("   export BD_AGENT_EMAIL='your-email@gmail.com'")
    print("   export BD_AGENT_EMAIL_PASSWORD='your-app-password'")
    print("   ```")
    
    print("\n2. **API Key Setup:**")
    print("   • Visit: https://tracxn.com/api")
    print("   • Sign up for API access")
    print("   • Generate API key in dashboard")
    print("   • Set environment variable")
    
    print("\n3. **Usage Example:**")
    print("   ```python")
    print("   from recruiting_agency.sub_agents.bd_agent.tools import fetch_recent_funding_rounds")
    print("   ")
    print("   # Fetch blockchain companies with recent funding")
    print("   companies = fetch_recent_funding_rounds(")
    print("       sector='blockchain',")
    print("       min_funding_amount=10000000,")
    print("       timeframe_days=90")
    print("   )")
    print("   ```")


if __name__ == "__main__":
    print("🎯 Tracxn-Only BD Agent Example")
    print("=" * 60)
    
    # Demonstrate the workflow
    results = demonstrate_tracxn_only_workflow()
    
    # Show API features
    demonstrate_tracxn_api_features()
    
    # Show configuration
    demonstrate_configuration()
    
    print("\n✅ Tracxn-only workflow completed!")
    print("\n💡 Next Steps:")
    print("1. Set your TRACXN_API_KEY environment variable")
    print("2. Run this example to test with real data")
    print("3. Customize filtering criteria for your needs")
    print("4. Set dry_run=False to actually send emails")
    print("5. Integrate with the full BD Agent workflow") 