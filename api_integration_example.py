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

"""Example demonstrating API integration for funding data."""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from recruiting_agency.sub_agents.bd_agent.tools import (
    fetch_recent_funding_rounds,
    fetch_crunchbase_funding_data,
    fetch_dealroom_funding_data,
    fetch_tracxn_funding_data,
    fetch_pitchbook_funding_data
)


def demonstrate_api_integration():
    """Demonstrate the API integration functionality."""
    
    print("🔌 API Integration Demonstration")
    print("=" * 50)
    
    # Check which API keys are available
    api_keys = {
        "Crunchbase": os.getenv("CRUNCHBASE_API_KEY"),
        "Dealroom": os.getenv("DEALROOM_API_KEY"),
        "Tracxn": os.getenv("TRACXN_API_KEY"),
        "PitchBook": os.getenv("PITCHBOOK_API_KEY")
    }
    
    print("\n📋 API Key Status:")
    available_apis = []
    for api_name, api_key in api_keys.items():
        status = "✅ Available" if api_key else "❌ Not configured"
        if api_key:
            available_apis.append(api_name)
        print(f"   {api_name}: {status}")
    
    print(f"\n🎯 Available APIs: {', '.join(available_apis) if available_apis else 'None'}")
    
    # Test individual API functions
    print("\n🧪 Testing Individual API Functions:")
    
    # Test Crunchbase
    print("\n1. Testing Crunchbase API...")
    crunchbase_companies = fetch_crunchbase_funding_data(
        sector="blockchain",
        min_funding_amount=10000000,
        timeframe_days=90
    )
    print(f"   Found {len(crunchbase_companies)} companies from Crunchbase")
    
    # Test Dealroom
    print("\n2. Testing Dealroom API...")
    dealroom_companies = fetch_dealroom_funding_data(
        sector="blockchain",
        min_funding_amount=10000000,
        timeframe_days=90
    )
    print(f"   Found {len(dealroom_companies)} companies from Dealroom")
    
    # Test Tracxn
    print("\n3. Testing Tracxn API...")
    tracxn_companies = fetch_tracxn_funding_data(
        sector="blockchain",
        min_funding_amount=10000000,
        timeframe_days=90
    )
    print(f"   Found {len(tracxn_companies)} companies from Tracxn")
    
    # Test PitchBook
    print("\n4. Testing PitchBook API...")
    pitchbook_companies = fetch_pitchbook_funding_data(
        sector="blockchain",
        min_funding_amount=10000000,
        timeframe_days=90
    )
    print(f"   Found {len(pitchbook_companies)} companies from PitchBook")
    
    # Test combined function with Tracxn prioritization
    print("\n🔄 Testing Combined API Function (Tracxn Prioritized):")
    all_companies = fetch_recent_funding_rounds(
        sector="blockchain",
        min_funding_amount=10000000,
        timeframe_days=90
    )
    print(f"   Total unique companies found: {len(all_companies)}")
    
    # Show sample companies
    if all_companies:
        print("\n📊 Sample Companies Found:")
        for i, company in enumerate(all_companies[:5], 1):
            print(f"\n   {i}. {company['company_name']}")
            print(f"      Funding: ${company['funding_amount']:,} ({company['funding_round']})")
            print(f"      Location: {company.get('location', 'N/A')}")
            print(f"      Description: {company.get('description', 'N/A')[:100]}...")
    
    return all_companies


def demonstrate_api_configuration():
    """Demonstrate how to configure the APIs."""
    
    print("\n⚙️ API Configuration Guide")
    print("=" * 40)
    
    print("\n1. Crunchbase API Setup:")
    print("   - Visit: https://data.crunchbase.com/docs/using-the-api")
    print("   - Sign up for API access")
    print("   - Set environment variable:")
    print("     export CRUNCHBASE_API_KEY='your_api_key_here'")
    
    print("\n2. Dealroom API Setup:")
    print("   - Visit: https://dealroom.co/api")
    print("   - Request API access")
    print("   - Set environment variable:")
    print("     export DEALROOM_API_KEY='your_api_key_here'")
    
    print("\n3. Tracxn API Setup:")
    print("   - Visit: https://tracxn.com/api")
    print("   - Sign up for API access")
    print("   - Set environment variable:")
    print("     export TRACXN_API_KEY='your_api_key_here'")
    
    print("\n4. PitchBook API Setup:")
    print("   - Visit: https://pitchbook.com/api")
    print("   - Request API access")
    print("   - Set environment variable:")
    print("     export PITCHBOOK_API_KEY='your_api_key_here'")
    
    print("\n5. Complete Setup Example:")
    print("   ```bash")
    print("   # Set all API keys")
    print("   export CRUNCHBASE_API_KEY='your_crunchbase_key'")
    print("   export DEALROOM_API_KEY='your_dealroom_key'")
    print("   export TRACXN_API_KEY='your_tracxn_key'")
    print("   export PITCHBOOK_API_KEY='your_pitchbook_key'")
    print("   ")
    print("   # Test the integration")
    print("   python api_integration_example.py")
    print("   ```")


def demonstrate_error_handling():
    """Demonstrate error handling for API failures."""
    
    print("\n🛡️ Error Handling Demonstration")
    print("=" * 40)
    
    print("\nThe API integration includes robust error handling:")
    print("• Graceful degradation when APIs are unavailable")
    print("• Individual API failures don't stop the entire process")
    print("• Detailed logging for debugging")
    print("• Fallback to sample data when no APIs are configured")
    
    print("\nExample error scenarios handled:")
    print("• Missing API keys")
    print("• Network timeouts")
    print("• API rate limiting")
    print("• Invalid API responses")
    print("• Authentication failures")


def demonstrate_data_processing():
    """Demonstrate data processing features."""
    
    print("\n📊 Data Processing Features")
    print("=" * 35)
    
    print("\n1. Duplicate Removal:")
    print("   • Companies are deduplicated based on company name")
    print("   • Prevents duplicate entries from multiple APIs")
    
    print("\n2. Data Standardization:")
    print("   • Normalizes data from different API formats")
    print("   • Consistent field names across all sources")
    print("   • Standardized funding amounts and dates")
    
    print("\n3. Filtering Options:")
    print("   • Minimum funding amount filtering")
    print("   • Company stage filtering (Seed, Series A, B, C+)")
    print("   • Sector-specific filtering")
    print("   • Time-based filtering")
    
    print("\n4. Sorting and Ranking:")
    print("   • Companies sorted by funding amount (highest first)")
    print("   • Recent funding rounds prioritized")
    print("   • Quality scoring based on data completeness")


if __name__ == "__main__":
    print("🚀 API Integration Example")
    print("=" * 60)
    
    # Demonstrate API integration
    companies = demonstrate_api_integration()
    
    # Show configuration guide
    demonstrate_api_configuration()
    
    # Show error handling
    demonstrate_error_handling()
    
    # Show data processing
    demonstrate_data_processing()
    
    print("\n✅ API Integration demonstration completed!")
    print("\n💡 Next Steps:")
    print("1. Obtain API keys from the respective providers")
    print("2. Set environment variables for the APIs")
    print("3. Test with real data")
    print("4. Customize filtering criteria for your needs")
    print("5. Integrate with the full BD Agent workflow") 