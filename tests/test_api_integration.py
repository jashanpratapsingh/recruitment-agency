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

"""Tests for the API integration functionality."""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from recruiting_agency.sub_agents.bd_agent.tools import (
    fetch_recent_funding_rounds,
    fetch_crunchbase_funding_data,
    fetch_dealroom_funding_data,
    fetch_tracxn_funding_data,
    fetch_pitchbook_funding_data
)


def test_fetch_crunchbase_funding_data_no_api_key():
    """Test Crunchbase function when API key is not available."""
    with patch.dict(os.environ, {}, clear=True):
        companies = fetch_crunchbase_funding_data()
        assert companies == []


def test_fetch_dealroom_funding_data_no_api_key():
    """Test Dealroom function when API key is not available."""
    with patch.dict(os.environ, {}, clear=True):
        companies = fetch_dealroom_funding_data()
        assert companies == []


def test_fetch_tracxn_funding_data_no_api_key():
    """Test Tracxn function when API key is not available."""
    with patch.dict(os.environ, {}, clear=True):
        companies = fetch_tracxn_funding_data()
        assert companies == []


def test_fetch_pitchbook_funding_data_no_api_key():
    """Test PitchBook function when API key is not available."""
    with patch.dict(os.environ, {}, clear=True):
        companies = fetch_pitchbook_funding_data()
        assert companies == []


@patch('requests.get')
def test_fetch_crunchbase_funding_data_success(mock_get):
    """Test successful Crunchbase API call."""
    # Mock successful API response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": {
            "items": [
                {
                    "name": "Test Blockchain Co",
                    "funding_rounds": [
                        {
                            "raised_amount_usd": 25000000,
                            "round_code": "Series A",
                            "announced_on": "2024-01-15",
                            "investors": [{"name": "Test Investor"}]
                        }
                    ],
                    "category_groups": ["blockchain"],
                    "employee_count": "50-100",
                    "short_description": "Blockchain infrastructure company",
                    "founders": [{"name": "John Doe"}],
                    "homepage_url": "https://test.com",
                    "linkedin_url": "https://linkedin.com/test"
                }
            ]
        }
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    with patch.dict(os.environ, {"CRUNCHBASE_API_KEY": "test_key"}):
        companies = fetch_crunchbase_funding_data()
        
        assert len(companies) == 1
        assert companies[0]["company_name"] == "Test Blockchain Co"
        assert companies[0]["funding_amount"] == 25000000
        assert companies[0]["funding_round"] == "Series A"


@patch('requests.get')
def test_fetch_dealroom_funding_data_success(mock_get):
    """Test successful Dealroom API call."""
    # Mock successful API response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "companies": [
            {
                "name": "Test DeFi Co",
                "latest_funding": {
                    "amount_usd": 30000000,
                    "round_type": "Series B",
                    "announced_date": "2024-02-01",
                    "investors": ["Test VC"]
                },
                "city": "San Francisco",
                "employee_count": "100-250",
                "description": "DeFi protocol company",
                "founders": ["Jane Smith"],
                "website": "https://testdefi.com",
                "linkedin_url": "https://linkedin.com/testdefi"
            }
        ]
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    with patch.dict(os.environ, {"DEALROOM_API_KEY": "test_key"}):
        companies = fetch_dealroom_funding_data()
        
        assert len(companies) == 1
        assert companies[0]["company_name"] == "Test DeFi Co"
        assert companies[0]["funding_amount"] == 30000000
        assert companies[0]["funding_round"] == "Series B"


@patch('requests.get')
def test_fetch_tracxn_funding_data_success(mock_get):
    """Test successful Tracxn API call."""
    # Mock successful API response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "companies": [
            {
                "name": "Test Web3 Co",
                "funding_rounds": [
                    {
                        "amount_usd": 40000000,
                        "round_type": "Series C",
                        "date": "2024-03-01",
                        "investors": ["Web3 VC"]
                    }
                ],
                "location": "New York",
                "employee_count": "250-500",
                "description": "Web3 infrastructure company",
                "founders": ["Bob Johnson"],
                "website": "https://testweb3.com",
                "linkedin_url": "https://linkedin.com/testweb3"
            }
        ]
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    with patch.dict(os.environ, {"TRACXN_API_KEY": "test_key"}):
        companies = fetch_tracxn_funding_data()
        
        assert len(companies) == 1
        assert companies[0]["company_name"] == "Test Web3 Co"
        assert companies[0]["funding_amount"] == 40000000
        assert companies[0]["funding_round"] == "Series C"


@patch('requests.get')
def test_fetch_pitchbook_funding_data_success(mock_get):
    """Test successful PitchBook API call."""
    # Mock successful API response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "companies": [
            {
                "name": "Test Crypto Co",
                "funding_rounds": [
                    {
                        "amount_usd": 50000000,
                        "round_type": "Series D",
                        "date": "2024-04-01",
                        "investors": ["Crypto VC"]
                    }
                ],
                "location": "Miami",
                "employee_count": "500+",
                "description": "Cryptocurrency platform company",
                "founders": ["Alice Brown"],
                "website": "https://testcrypto.com",
                "linkedin_url": "https://linkedin.com/testcrypto"
            }
        ]
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    with patch.dict(os.environ, {"PITCHBOOK_API_KEY": "test_key"}):
        companies = fetch_pitchbook_funding_data()
        
        assert len(companies) == 1
        assert companies[0]["company_name"] == "Test Crypto Co"
        assert companies[0]["funding_amount"] == 50000000
        assert companies[0]["funding_round"] == "Series D"


def test_fetch_recent_funding_rounds_no_apis():
    """Test the main function when no APIs are available."""
    with patch.dict(os.environ, {}, clear=True):
        companies = fetch_recent_funding_rounds()
        
        # Should return sample data when no APIs are available
        assert len(companies) > 0
        assert all("company_name" in company for company in companies)
        assert all("funding_amount" in company for company in companies)


def test_fetch_recent_funding_rounds_with_filtering():
    """Test the main function with filtering options."""
    with patch.dict(os.environ, {}, clear=True):
        companies = fetch_recent_funding_rounds(
            sector="blockchain",
            min_funding_amount=20000000,
            timeframe_days=90,
            company_stage="Series B"
        )
        
        # Should return companies matching the criteria
        assert len(companies) > 0
        for company in companies:
            assert company.get("funding_amount", 0) >= 20000000
            assert company.get("funding_round") == "Series B"


def test_duplicate_removal():
    """Test that duplicate companies are removed."""
    # Mock API responses with duplicate companies
    with patch('recruiting_agency.sub_agents.bd_agent.tools.fetch_crunchbase_funding_data') as mock_crunchbase:
        with patch('recruiting_agency.sub_agents.bd_agent.tools.fetch_dealroom_funding_data') as mock_dealroom:
            mock_crunchbase.return_value = [
                {"company_name": "Test Co", "funding_amount": 25000000, "funding_round": "Series A"}
            ]
            mock_dealroom.return_value = [
                {"company_name": "Test Co", "funding_amount": 25000000, "funding_round": "Series A"}
            ]
            
            with patch.dict(os.environ, {"CRUNCHBASE_API_KEY": "test", "DEALROOM_API_KEY": "test"}):
                companies = fetch_recent_funding_rounds()
                
                # Should have only one instance of "Test Co"
                company_names = [company["company_name"] for company in companies]
                assert company_names.count("Test Co") == 1


def test_sorting_by_funding_amount():
    """Test that companies are sorted by funding amount."""
    with patch.dict(os.environ, {}, clear=True):
        companies = fetch_recent_funding_rounds()
        
        # Should be sorted by funding amount (highest first)
        funding_amounts = [company.get("funding_amount", 0) for company in companies]
        assert funding_amounts == sorted(funding_amounts, reverse=True)


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 