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

"""Tests for the BD agent tools."""

import pytest
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from recruiting_agency.sub_agents.bd_agent.tools import (
    fetch_recent_funding_rounds,
    filter_blockchain_companies,
    personalize_outreach,
    book_meeting
)


def test_fetch_recent_funding_rounds():
    """Test the fetch_recent_funding_rounds function."""
    companies = fetch_recent_funding_rounds(
        sector="blockchain",
        min_funding_amount=10000000,
        timeframe_days=90
    )
    
    assert isinstance(companies, list)
    assert len(companies) > 0
    
    for company in companies:
        assert "company_name" in company
        assert "funding_amount" in company
        assert "funding_round" in company
        assert "sector" in company
        assert company["sector"] == "blockchain"


def test_filter_blockchain_companies():
    """Test the filter_blockchain_companies function."""
    # Create sample companies
    sample_companies = [
        {
            "company_name": "Test Company 1",
            "funding_amount": 25000000,
            "funding_round": "Series A",
            "location": "San Francisco, CA"
        },
        {
            "company_name": "Test Company 2", 
            "funding_amount": 5000000,
            "funding_round": "Seed",
            "location": "New York, NY"
        }
    ]
    
    filtered = filter_blockchain_companies(
        companies=sample_companies,
        min_funding=20000000,
        target_stages=["Series A"]
    )
    
    assert isinstance(filtered, list)
    assert len(filtered) == 1
    assert filtered[0]["company_name"] == "Test Company 1"


def test_personalize_outreach():
    """Test the personalize_outreach function."""
    target_companies = [
        {
            "company_name": "Test Blockchain Co",
            "funding_amount": 30000000,
            "funding_round": "Series B",
            "hiring_plans": "Expanding engineering team"
        }
    ]
    
    strategies = personalize_outreach(target_companies)
    
    assert isinstance(strategies, list)
    assert len(strategies) == 1
    
    strategy = strategies[0]
    assert "company_name" in strategy
    assert "personalized_message" in strategy
    assert "outreach_channels" in strategy
    assert "decision_makers" in strategy


def test_book_meeting():
    """Test the book_meeting function."""
    outreach_strategies = [
        {
            "company_name": "Test Company",
            "personalized_message": "Test message"
        }
    ]
    
    meeting_strategies = book_meeting(outreach_strategies)
    
    assert isinstance(meeting_strategies, list)
    assert len(meeting_strategies) == 1
    
    strategy = meeting_strategies[0]
    assert "company_name" in strategy
    assert "meeting_objective" in strategy
    assert "calendar_integration" in strategy
    assert "crm_integration" in strategy


def test_complete_workflow():
    """Test the complete BD Agent workflow."""
    # Step 1: Fetch companies
    companies = fetch_recent_funding_rounds()
    assert len(companies) > 0
    
    # Step 2: Filter companies
    target_companies = filter_blockchain_companies(companies)
    assert len(target_companies) <= len(companies)
    
    # Step 3: Create outreach
    outreach_strategies = personalize_outreach(target_companies)
    assert len(outreach_strategies) == len(target_companies)
    
    # Step 4: Book meetings
    meeting_strategies = book_meeting(outreach_strategies)
    assert len(meeting_strategies) == len(outreach_strategies)
    
    print(f"✅ Complete workflow test passed:")
    print(f"   - Fetched {len(companies)} companies")
    print(f"   - Filtered to {len(target_companies)} targets")
    print(f"   - Created {len(outreach_strategies)} outreach strategies")
    print(f"   - Developed {len(meeting_strategies)} meeting strategies")


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 