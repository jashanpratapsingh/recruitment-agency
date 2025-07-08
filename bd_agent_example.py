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

"""Example usage of the enhanced BD Agent for blockchain company identification."""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from recruiting_agency.sub_agents.bd_agent.tools import (
    fetch_recent_funding_rounds,
    filter_blockchain_companies,
    personalize_outreach,
    book_meeting
)


def demonstrate_bd_agent_workflow():
    """Demonstrate the complete BD Agent workflow for blockchain companies."""
    
    print("🚀 BD Agent - Blockchain Company Identification Workflow")
    print("=" * 60)
    
    # Step 1: Fetch recent funding rounds
    print("\n📊 Step 1: Fetching Recent Funding Rounds")
    print("-" * 40)
    
    companies = fetch_recent_funding_rounds(
        sector="blockchain",
        min_funding_amount=10000000,
        timeframe_days=90,
        company_stage="Series A"
    )
    
    print(f"Found {len(companies)} companies with recent funding:")
    for company in companies:
        print(f"  • {company['company_name']} - ${company['funding_amount']:,} ({company['funding_round']})")
    
    # Step 2: Filter blockchain companies
    print("\n🎯 Step 2: Filtering Target Companies")
    print("-" * 40)
    
    target_companies = filter_blockchain_companies(
        companies=companies,
        min_funding=20000000,  # $20M minimum
        target_stages=["Series A", "Series B"],
        locations=["San Francisco", "New York", "Remote"],
        remote_friendly=True
    )
    
    print(f"Filtered to {len(target_companies)} target companies:")
    for company in target_companies:
        print(f"  • {company['company_name']} - {company['location']} - {company['hiring_plans']}")
    
    # Step 3: Personalize outreach
    print("\n💬 Step 3: Creating Personalized Outreach")
    print("-" * 40)
    
    outreach_strategies = personalize_outreach(
        target_companies=target_companies,
        recruiting_services=[
            "Technical Recruiting",
            "Executive Search",
            "Employer Branding"
        ]
    )
    
    print(f"Created {len(outreach_strategies)} personalized outreach strategies:")
    for strategy in outreach_strategies:
        print(f"\n  📧 {strategy['company_name']}:")
        print(f"     Message: {strategy['personalized_message'][:100]}...")
        print(f"     Channels: {', '.join(strategy['outreach_channels'])}")
        print(f"     Decision Makers: {', '.join(strategy['decision_makers'])}")
    
    # Step 4: Book meetings
    print("\n📅 Step 4: Meeting Booking Strategies")
    print("-" * 40)
    
    meeting_strategies = book_meeting(
        outreach_strategies=outreach_strategies,
        calendar_integration=True,
        crm_integration=True
    )
    
    print(f"Created {len(meeting_strategies)} meeting strategies:")
    for strategy in meeting_strategies:
        print(f"\n  📅 {strategy['company_name']}:")
        print(f"     Objective: {strategy['meeting_objective']}")
        print(f"     Calendar: {', '.join(strategy['calendar_integration']['platforms'])}")
        print(f"     CRM: {', '.join(strategy['crm_integration']['platforms'])}")
    
    # Summary
    print("\n🎉 Workflow Summary")
    print("-" * 40)
    print(f"• Identified {len(companies)} companies with recent funding")
    print(f"• Filtered to {len(target_companies)} target companies")
    print(f"• Created {len(outreach_strategies)} personalized outreach strategies")
    print(f"• Developed {len(meeting_strategies)} meeting booking strategies")
    
    print("\n✅ BD Agent workflow completed successfully!")


def demonstrate_api_integration_placeholders():
    """Demonstrate the API integration placeholders."""
    
    print("\n🔌 API Integration Placeholders")
    print("=" * 40)
    
    print("The following API integrations are ready for implementation:")
    print("\n1. Crunchbase API:")
    print("   - Endpoint: https://api.crunchbase.com/v3.1/organizations")
    print("   - Use case: Fetch funding data and company information")
    print("   - Environment variable: CRUNCHBASE_API_KEY")
    
    print("\n2. Dealroom API:")
    print("   - Endpoint: https://api.dealroom.co/v1/companies")
    print("   - Use case: European market data and funding insights")
    print("   - Environment variable: DEALROOM_API_KEY")
    
    print("\n3. Tracxn API:")
    print("   - Endpoint: https://api.tracxn.com/api/1.0/companies")
    print("   - Use case: Comprehensive startup data and analytics")
    print("   - Environment variable: TRACXN_API_KEY")
    
    print("\n4. PitchBook API:")
    print("   - Endpoint: https://api.pitchbook.com/v1/companies")
    print("   - Use case: Detailed financial information and valuations")
    print("   - Environment variable: PITCHBOOK_API_KEY")
    
    print("\nTo implement these APIs:")
    print("1. Obtain API keys from respective providers")
    print("2. Set environment variables")
    print("3. Uncomment and configure API calls in tools.py")
    print("4. Add error handling and rate limiting")
    print("5. Test with real data")


if __name__ == "__main__":
    demonstrate_bd_agent_workflow()
    demonstrate_api_integration_placeholders() 