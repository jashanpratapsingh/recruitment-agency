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

"""Tests for the email functionality in the BD agent."""

import pytest
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from recruiting_agency.sub_agents.bd_agent.tools import (
    generate_personalized_message,
    send_personalized_emails,
    personalize_outreach
)


def test_generate_personalized_message_email():
    """Test email message generation."""
    company = {
        "company_name": "Test Blockchain Co",
        "funding_amount": 30000000,
        "funding_round": "Series B",
        "description": "leading DeFi protocol",
        "hiring_plans": "scaling engineering team",
        "key_people": ["John Doe", "Jane Smith"]
    }
    
    message = generate_personalized_message(company, "email")
    
    assert message["message_type"] == "email"
    assert "Test Blockchain Co" in message["subject"]
    assert "Series B" in message["subject"]
    assert "John Doe" in message["body"]
    assert "30000000" in message["body"]
    assert "DeFi protocol" in message["body"]


def test_generate_personalized_message_linkedin():
    """Test LinkedIn message generation."""
    company = {
        "company_name": "Test Blockchain Co",
        "funding_amount": 30000000,
        "funding_round": "Series B",
        "description": "leading DeFi protocol",
        "hiring_plans": "scaling engineering team",
        "key_people": ["John Doe"]
    }
    
    message = generate_personalized_message(company, "linkedin")
    
    assert message["message_type"] == "linkedin"
    assert "Test Blockchain Co" in message["subject"]
    assert "🎉" in message["body"]  # LinkedIn uses emojis
    assert "John Doe" in message["body"]


def test_personalize_outreach_with_messages():
    """Test personalized outreach with message generation."""
    target_companies = [
        {
            "company_name": "Test Company 1",
            "funding_amount": 25000000,
            "funding_round": "Series A",
            "description": "blockchain infrastructure",
            "hiring_plans": "hiring developers",
            "key_people": ["CEO"]
        },
        {
            "company_name": "Test Company 2",
            "funding_amount": 50000000,
            "funding_round": "Series B",
            "description": "DeFi platform",
            "hiring_plans": "scaling team",
            "key_people": ["CTO"]
        }
    ]
    
    strategies = personalize_outreach(
        target_companies=target_companies,
        message_types=["email", "linkedin"]
    )
    
    assert len(strategies) == 2
    
    for strategy in strategies:
        assert "generated_messages" in strategy
        assert "email" in strategy["generated_messages"]
        assert "linkedin" in strategy["generated_messages"]
        
        email_msg = strategy["generated_messages"]["email"]
        linkedin_msg = strategy["generated_messages"]["linkedin"]
        
        assert email_msg["message_type"] == "email"
        assert linkedin_msg["message_type"] == "linkedin"


def test_send_personalized_emails_dry_run():
    """Test email sending in dry run mode."""
    outreach_strategies = [
        {
            "company_name": "Test Company",
            "generated_messages": {
                "email": {
                    "subject": "Test Subject",
                    "body": "Test body content"
                }
            }
        }
    ]
    
    results = send_personalized_emails(
        outreach_strategies=outreach_strategies,
        dry_run=True
    )
    
    assert len(results) == 1
    assert results[0]["status"] == "dry_run"
    assert results[0]["company_name"] == "Test Company"


def test_email_message_structure():
    """Test that generated email messages have the correct structure."""
    company = {
        "company_name": "Test Co",
        "funding_amount": 20000000,
        "funding_round": "Series A",
        "description": "blockchain solution",
        "hiring_plans": "expanding team",
        "key_people": ["John Doe"]
    }
    
    email_message = generate_personalized_message(company, "email")
    
    # Check required fields
    required_fields = ["company_name", "message_type", "subject", "body", "recipients", "company_info"]
    for field in required_fields:
        assert field in email_message
    
    # Check content
    assert email_message["message_type"] == "email"
    assert "Test Co" in email_message["subject"]
    assert "Series A" in email_message["subject"]
    assert "John Doe" in email_message["body"]
    assert "20000000" in email_message["body"]


def test_linkedin_message_structure():
    """Test that generated LinkedIn messages have the correct structure."""
    company = {
        "company_name": "Test Co",
        "funding_amount": 20000000,
        "funding_round": "Series A",
        "description": "blockchain solution",
        "hiring_plans": "expanding team",
        "key_people": ["John Doe"]
    }
    
    linkedin_message = generate_personalized_message(company, "linkedin")
    
    # Check required fields
    required_fields = ["company_name", "message_type", "subject", "body", "recipients", "company_info"]
    for field in required_fields:
        assert field in linkedin_message
    
    # Check content
    assert linkedin_message["message_type"] == "linkedin"
    assert "Test Co" in linkedin_message["subject"]
    assert "🎉" in linkedin_message["body"]  # LinkedIn uses emojis


def test_multiple_message_types():
    """Test generating multiple message types for the same company."""
    company = {
        "company_name": "Multi Test Co",
        "funding_amount": 40000000,
        "funding_round": "Series C",
        "description": "enterprise blockchain",
        "hiring_plans": "hiring executives",
        "key_people": ["CEO", "CTO"]
    }
    
    email_msg = generate_personalized_message(company, "email")
    linkedin_msg = generate_personalized_message(company, "linkedin")
    
    # Both should reference the same company but have different tones
    assert "Multi Test Co" in email_msg["subject"]
    assert "Multi Test Co" in linkedin_msg["subject"]
    
    # Email should be more formal
    assert "Dear" in email_msg["body"]
    
    # LinkedIn should be more casual
    assert "Hi" in linkedin_msg["body"]
    assert "🎉" in linkedin_msg["body"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 