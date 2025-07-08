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

"""Tools for the BD agent to identify and engage blockchain companies."""

import logging
import smtplib
import os
import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.adk.tools import FunctionTool
from google.adk import Agent

logger = logging.getLogger(__name__)


def fetch_crunchbase_funding_data(
    sector: str = "blockchain",
    min_funding_amount: Optional[float] = None,
    timeframe_days: int = 90
) -> List[Dict[str, Any]]:
    """
    Fetch funding data from Crunchbase API.
    
    Args:
        sector: Target sector
        min_funding_amount: Minimum funding amount in USD
        timeframe_days: Number of days to look back
    
    Returns:
        List of companies with funding data
    """
    api_key = os.getenv("CRUNCHBASE_API_KEY")
    if not api_key:
        logger.warning("CRUNCHBASE_API_KEY not found, skipping Crunchbase data")
        return []
    
    try:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=timeframe_days)
        
        # Crunchbase API endpoint for organizations
        url = "https://api.crunchbase.com/v3.1/organizations"
        
        params = {
            "user_key": api_key,
            "organization_types": "company",
            "updated_since": start_date.strftime("%Y-%m-%d"),
            "order": "updated_at DESC",
            "limit": 100
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        companies = []
        
        for org in data.get("data", {}).get("items", []):
            # Extract funding information
            funding_rounds = org.get("funding_rounds", [])
            if not funding_rounds:
                continue
            
            # Get the most recent funding round
            latest_round = max(funding_rounds, key=lambda x: x.get("announced_on", ""))
            
            funding_amount = latest_round.get("raised_amount_usd", 0)
            if min_funding_amount and funding_amount < min_funding_amount:
                continue
            
            # Check if company is in blockchain sector
            categories = org.get("category_groups", [])
            if sector.lower() not in [cat.lower() for cat in categories]:
                continue
            
            company = {
                "company_name": org.get("name", ""),
                "funding_amount": funding_amount,
                "funding_round": latest_round.get("round_code", ""),
                "funding_date": latest_round.get("announced_on", ""),
                "investors": [inv.get("name", "") for inv in latest_round.get("investors", [])],
                "sector": sector,
                "location": org.get("homepage_url", ""),
                "company_size": org.get("employee_count", ""),
                "description": org.get("short_description", ""),
                "key_people": [person.get("name", "") for person in org.get("founders", [])],
                "website": org.get("homepage_url", ""),
                "linkedin": org.get("linkedin_url", "")
            }
            
            companies.append(company)
        
        logger.info(f"Fetched {len(companies)} companies from Crunchbase")
        return companies
        
    except Exception as e:
        logger.error(f"Error fetching Crunchbase data: {str(e)}")
        return []


def fetch_dealroom_funding_data(
    sector: str = "blockchain",
    min_funding_amount: Optional[float] = None,
    timeframe_days: int = 90
) -> List[Dict[str, Any]]:
    """
    Fetch funding data from Dealroom API.
    
    Args:
        sector: Target sector
        min_funding_amount: Minimum funding amount in USD
        timeframe_days: Number of days to look back
    
    Returns:
        List of companies with funding data
    """
    api_key = os.getenv("DEALROOM_API_KEY")
    if not api_key:
        logger.warning("DEALROOM_API_KEY not found, skipping Dealroom data")
        return []
    
    try:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=timeframe_days)
        
        # Dealroom API endpoint
        url = "https://api.dealroom.co/v1/companies"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        params = {
            "sector": sector,
            "funding_date_from": start_date.strftime("%Y-%m-%d"),
            "funding_date_to": end_date.strftime("%Y-%m-%d"),
            "min_funding_amount": min_funding_amount or 0,
            "limit": 100
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        companies = []
        
        for company_data in data.get("companies", []):
            funding_info = company_data.get("latest_funding", {})
            
            company = {
                "company_name": company_data.get("name", ""),
                "funding_amount": funding_info.get("amount_usd", 0),
                "funding_round": funding_info.get("round_type", ""),
                "funding_date": funding_info.get("announced_date", ""),
                "investors": funding_info.get("investors", []),
                "sector": sector,
                "location": company_data.get("city", ""),
                "company_size": company_data.get("employee_count", ""),
                "description": company_data.get("description", ""),
                "key_people": company_data.get("founders", []),
                "website": company_data.get("website", ""),
                "linkedin": company_data.get("linkedin_url", "")
            }
            
            companies.append(company)
        
        logger.info(f"Fetched {len(companies)} companies from Dealroom")
        return companies
        
    except Exception as e:
        logger.error(f"Error fetching Dealroom data: {str(e)}")
        return []


def fetch_tracxn_funding_data(
    sector: str = "blockchain",
    min_funding_amount: Optional[float] = None,
    timeframe_days: int = 90
) -> List[Dict[str, Any]]:
    """
    Fetch funding data from Tracxn API.
    
    Args:
        sector: Target sector
        min_funding_amount: Minimum funding amount in USD
        timeframe_days: Number of days to look back
    
    Returns:
        List of companies with funding data
    """
    api_key = os.getenv("TRACXN_API_KEY")
    if not api_key:
        logger.warning("TRACXN_API_KEY not found, skipping Tracxn data")
        return []
    
    try:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=timeframe_days)
        
        # Tracxn API endpoint
        url = "https://api.tracxn.com/api/1.0/companies"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        params = {
            "sector": sector,
            "funding_date_from": start_date.strftime("%Y-%m-%d"),
            "funding_date_to": end_date.strftime("%Y-%m-%d"),
            "min_funding_amount": min_funding_amount or 0,
            "limit": 100
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        companies = []
        
        for company_data in data.get("companies", []):
            funding_rounds = company_data.get("funding_rounds", [])
            if not funding_rounds:
                continue
            
            # Get the most recent funding round
            latest_round = max(funding_rounds, key=lambda x: x.get("date", ""))
            
            company = {
                "company_name": company_data.get("name", ""),
                "funding_amount": latest_round.get("amount_usd", 0),
                "funding_round": latest_round.get("round_type", ""),
                "funding_date": latest_round.get("date", ""),
                "investors": latest_round.get("investors", []),
                "sector": sector,
                "location": company_data.get("location", ""),
                "company_size": company_data.get("employee_count", ""),
                "description": company_data.get("description", ""),
                "key_people": company_data.get("founders", []),
                "website": company_data.get("website", ""),
                "linkedin": company_data.get("linkedin_url", "")
            }
            
            companies.append(company)
        
        logger.info(f"Fetched {len(companies)} companies from Tracxn")
        return companies
        
    except Exception as e:
        logger.error(f"Error fetching Tracxn data: {str(e)}")
        return []


def fetch_pitchbook_funding_data(
    sector: str = "blockchain",
    min_funding_amount: Optional[float] = None,
    timeframe_days: int = 90
) -> List[Dict[str, Any]]:
    """
    Fetch funding data from PitchBook API.
    
    Args:
        sector: Target sector
        min_funding_amount: Minimum funding amount in USD
        timeframe_days: Number of days to look back
    
    Returns:
        List of companies with funding data
    """
    api_key = os.getenv("PITCHBOOK_API_KEY")
    if not api_key:
        logger.warning("PITCHBOOK_API_KEY not found, skipping PitchBook data")
        return []
    
    try:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=timeframe_days)
        
        # PitchBook API endpoint
        url = "https://api.pitchbook.com/v1/companies"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        params = {
            "sector": sector,
            "funding_date_from": start_date.strftime("%Y-%m-%d"),
            "funding_date_to": end_date.strftime("%Y-%m-%d"),
            "min_funding_amount": min_funding_amount or 0,
            "limit": 100
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        companies = []
        
        for company_data in data.get("companies", []):
            funding_rounds = company_data.get("funding_rounds", [])
            if not funding_rounds:
                continue
            
            # Get the most recent funding round
            latest_round = max(funding_rounds, key=lambda x: x.get("date", ""))
            
            company = {
                "company_name": company_data.get("name", ""),
                "funding_amount": latest_round.get("amount_usd", 0),
                "funding_round": latest_round.get("round_type", ""),
                "funding_date": latest_round.get("date", ""),
                "investors": latest_round.get("investors", []),
                "sector": sector,
                "location": company_data.get("location", ""),
                "company_size": company_data.get("employee_count", ""),
                "description": company_data.get("description", ""),
                "key_people": company_data.get("founders", []),
                "website": company_data.get("website", ""),
                "linkedin": company_data.get("linkedin_url", "")
            }
            
            companies.append(company)
        
        logger.info(f"Fetched {len(companies)} companies from PitchBook")
        return companies
        
    except Exception as e:
        logger.error(f"Error fetching PitchBook data: {str(e)}")
        return []


def fetch_recent_funding_rounds(
    sector: str = "blockchain",
    min_funding_amount: Optional[float] = None,
    timeframe_days: int = 90,
    company_stage: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Fetch recent funding rounds for blockchain companies using available APIs.
    Prioritizes Tracxn API when available, with fallback to other APIs and sample data.
    
    Args:
        sector: Target sector (default: blockchain)
        min_funding_amount: Minimum funding amount in USD
        timeframe_days: Number of days to look back
        company_stage: Company stage filter (Seed, Series A, B, C+)
    
    Returns:
        List of companies with recent funding rounds
    """
    logger.info(f"Fetching recent funding rounds for {sector} companies")
    
    all_companies = []
    available_apis = []
    
    # Check which APIs are available and prioritize Tracxn
    api_checks = [
        ("Tracxn", fetch_tracxn_funding_data, os.getenv("TRACXN_API_KEY")),
        ("Crunchbase", fetch_crunchbase_funding_data, os.getenv("CRUNCHBASE_API_KEY")),
        ("Dealroom", fetch_dealroom_funding_data, os.getenv("DEALROOM_API_KEY")),
        ("PitchBook", fetch_pitchbook_funding_data, os.getenv("PITCHBOOK_API_KEY"))
    ]
    
    # Log available APIs
    for api_name, _, api_key in api_checks:
        if api_key:
            available_apis.append(api_name)
            logger.info(f"✅ {api_name} API key found")
        else:
            logger.info(f"❌ {api_name} API key not configured")
    
    if not available_apis:
        logger.warning("No API keys configured, using sample data")
        return _get_sample_companies()
    
    # Fetch data from available APIs, prioritizing Tracxn
    for api_name, api_function, api_key in api_checks:
        if not api_key:
            continue
            
        try:
            logger.info(f"Fetching data from {api_name}...")
            companies = api_function(
                sector=sector,
                min_funding_amount=min_funding_amount,
                timeframe_days=timeframe_days
            )
            all_companies.extend(companies)
            logger.info(f"✅ Successfully fetched {len(companies)} companies from {api_name}")
        except Exception as e:
            logger.error(f"❌ Failed to fetch data from {api_name}: {str(e)}")
    
    # Remove duplicates based on company name
    seen_companies = set()
    unique_companies = []
    
    for company in all_companies:
        company_name = company.get("company_name", "").lower()
        if company_name and company_name not in seen_companies:
            seen_companies.add(company_name)
            unique_companies.append(company)
    
    # Apply company stage filter if specified
    if company_stage:
        unique_companies = [
            company for company in unique_companies
            if company.get("funding_round", "").lower() == company_stage.lower()
        ]
    
    # Sort by funding amount (highest first)
    unique_companies.sort(key=lambda x: x.get("funding_amount", 0), reverse=True)
    
    logger.info(f"📊 Total unique companies found: {len(unique_companies)}")
    
    # If no companies found from APIs, return sample data
    if not unique_companies:
        logger.warning("No companies found from APIs, returning sample data")
        return _get_sample_companies()
    
    return unique_companies


def _get_sample_companies() -> List[Dict[str, Any]]:
    """Return sample companies for demonstration purposes."""
    return [
        {
            "company_name": "Chainlink Labs",
            "funding_amount": 225000000,
            "funding_round": "Series B",
            "funding_date": "2024-01-15",
            "investors": ["Andreessen Horowitz", "Sequoia Capital"],
            "sector": "blockchain",
            "location": "San Francisco, CA",
            "company_size": "100-250 employees",
            "hiring_plans": "Aggressive hiring for engineering and product roles",
            "description": "Leading provider of decentralized oracle networks for smart contracts",
            "key_people": ["Sergey Nazarov", "Steve Ellis"],
            "website": "https://chainlinklabs.com",
            "linkedin": "https://linkedin.com/company/chainlink-labs"
        },
        {
            "company_name": "Polygon",
            "funding_amount": 450000000,
            "funding_round": "Series C",
            "funding_date": "2024-02-01",
            "investors": ["SoftBank", "Tiger Global"],
            "sector": "blockchain",
            "location": "Mumbai, India",
            "company_size": "250-500 employees",
            "hiring_plans": "Expanding global team across engineering and business development",
            "description": "Ethereum scaling solution providing faster and cheaper transactions",
            "key_people": ["Sandeep Nailwal", "Jaynti Kanani"],
            "website": "https://polygon.technology",
            "linkedin": "https://linkedin.com/company/polygon-technology"
        },
        {
            "company_name": "Avalanche",
            "funding_amount": 350000000,
            "funding_round": "Series C",
            "funding_date": "2024-03-01",
            "investors": ["Polychain Capital", "Three Arrows Capital"],
            "sector": "blockchain",
            "location": "Singapore",
            "company_size": "100-250 employees",
            "hiring_plans": "Scaling engineering and research teams",
            "description": "High-performance blockchain platform for decentralized applications",
            "key_people": ["Emin Gün Sirer", "Kevin Sekniqi"],
            "website": "https://avax.network",
            "linkedin": "https://linkedin.com/company/avalanche-avax"
        }
    ]


def filter_blockchain_companies(
    companies: List[Dict[str, Any]],
    min_funding: float = 10000000,
    target_stages: List[str] = None,
    locations: List[str] = None,
    remote_friendly: bool = True
) -> List[Dict[str, Any]]:
    """
    Filter blockchain companies based on specific criteria.
    
    Args:
        companies: List of companies from fetch_recent_funding_rounds
        min_funding: Minimum funding amount in USD
        target_stages: List of target company stages
        locations: Preferred geographic locations
        remote_friendly: Whether to prioritize remote-friendly companies
    
    Returns:
        Filtered list of target companies
    """
    if target_stages is None:
        target_stages = ["Series A", "Series B", "Series C"]
    
    logger.info(f"Filtering {len(companies)} companies with criteria: min_funding=${min_funding}, stages={target_stages}")
    
    filtered_companies = []
    
    for company in companies:
        # Apply funding filter
        if company.get("funding_amount", 0) < min_funding:
            continue
            
        # Apply stage filter
        if company.get("funding_round") not in target_stages:
            continue
            
        # Apply location filter if specified
        if locations and not any(loc in company.get("location", "") for loc in locations):
            continue
            
        filtered_companies.append(company)
    
    # Sort by funding amount (highest first)
    filtered_companies.sort(key=lambda x: x.get("funding_amount", 0), reverse=True)
    
    return filtered_companies


def generate_personalized_message(company: Dict[str, Any], message_type: str = "email") -> Dict[str, Any]:
    """
    Generate a personalized message for a specific company using LLM logic.
    
    Args:
        company: Company information dictionary
        message_type: Type of message ("email" or "linkedin")
    
    Returns:
        Dictionary containing personalized message and metadata
    """
    # LLM-based message generation logic
    company_name = company.get("company_name", "")
    funding_amount = company.get("funding_amount", 0)
    funding_round = company.get("funding_round", "")
    description = company.get("description", "")
    hiring_plans = company.get("hiring_plans", "")
    key_people = company.get("key_people", [])
    
    # Template-based message generation with LLM-style personalization
    if message_type == "email":
        subject = f"Congratulations on your {funding_round} funding - Let's discuss your hiring plans"
        
        body = f"""
Dear {key_people[0] if key_people else "Team"},

Congratulations on {company_name}'s recent {funding_round} funding round of ${funding_amount:,}! 

I've been following {company_name}'s impressive work in {description.lower()}. With your aggressive hiring plans for {hiring_plans}, I believe we could be a valuable partner in scaling your talent acquisition efforts.

Our specialized blockchain recruiting expertise has helped companies like yours hire top engineering and product talent 40% faster than traditional methods. We understand the unique challenges of building teams in the blockchain space and can help you:

• Source and screen specialized blockchain developers
• Build compelling employer branding for crypto talent
• Optimize your recruitment process for rapid scaling
• Provide executive search for key leadership roles

Would you be interested in a 15-minute call to discuss how we can support your hiring goals? I'm available this week and next.

Best regards,
[Your Name]
[Your Title]
[Your Company]
[Your Phone]
        """.strip()
        
    else:  # LinkedIn message
        subject = f"Congratulations on the {funding_round} funding!"
        
        body = f"""
Hi {key_people[0] if key_people else "there"},

Congratulations on {company_name}'s recent {funding_round} funding round! 🎉

I've been impressed by your work in {description.lower()}. With your plans to {hiring_plans}, I'd love to discuss how our specialized blockchain recruiting services could help you scale your team efficiently.

We've helped similar companies hire top talent 40% faster. Would you be open to a quick call this week?

Best,
[Your Name]
        """.strip()
    
    return {
        "company_name": company_name,
        "message_type": message_type,
        "subject": subject,
        "body": body,
        "recipients": key_people,
        "company_info": {
            "funding_amount": funding_amount,
            "funding_round": funding_round,
            "description": description,
            "hiring_plans": hiring_plans
        }
    }


def personalize_outreach(
    target_companies: List[Dict[str, Any]],
    recruiting_services: List[str] = None,
    message_types: List[str] = None
) -> List[Dict[str, Any]]:
    """
    Create personalized outreach strategies for target companies using LLM-generated messages.
    
    Args:
        target_companies: List of filtered target companies
        recruiting_services: List of services to offer
        message_types: Types of messages to generate ("email", "linkedin")
    
    Returns:
        List of personalized outreach strategies with generated messages
    """
    if recruiting_services is None:
        recruiting_services = [
            "Technical Recruiting",
            "Executive Search", 
            "Employer Branding",
            "Recruitment Process Optimization"
        ]
    
    if message_types is None:
        message_types = ["email", "linkedin"]
    
    logger.info(f"Creating personalized outreach for {len(target_companies)} companies")
    
    outreach_strategies = []
    
    for company in target_companies:
        strategy = {
            "company_name": company["company_name"],
            "funding_info": f"Recently raised ${company['funding_amount']:,} in {company['funding_round']}",
            "value_proposition": f"Specialized blockchain recruiting expertise to help you hire top talent quickly and efficiently",
            "outreach_channels": ["LinkedIn", "Email", "Direct Call"],
            "decision_makers": ["CTO", "VP Engineering", "Head of People"],
            "follow_up_sequence": [
                "Initial outreach",
                "Follow-up email (3 days)",
                "LinkedIn connection",
                "Phone call attempt",
                "Final follow-up"
            ],
            "generated_messages": {}
        }
        
        # Generate personalized messages for each message type
        for message_type in message_types:
            message = generate_personalized_message(company, message_type)
            strategy["generated_messages"][message_type] = message
        
        outreach_strategies.append(strategy)
    
    return outreach_strategies


def send_email(
    to_email: str,
    subject: str,
    body: str,
    from_email: str = None,
    smtp_server: str = None,
    smtp_port: int = 587,
    username: str = None,
    password: str = None
) -> Dict[str, Any]:
    """
    Send an email using SMTP.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Email body
        from_email: Sender email address
        smtp_server: SMTP server (default: Gmail)
        smtp_port: SMTP port
        username: SMTP username
        password: SMTP password
    
    Returns:
        Dictionary with send status and details
    """
    # Default to Gmail SMTP if not specified
    if smtp_server is None:
        smtp_server = "smtp.gmail.com"
    
    if from_email is None:
        from_email = os.getenv("BD_AGENT_EMAIL")
    
    if username is None:
        username = os.getenv("BD_AGENT_EMAIL")
    
    if password is None:
        password = os.getenv("BD_AGENT_EMAIL_PASSWORD")
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'plain'))
        
        # Create SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        
        # Login to server
        server.login(username, password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        
        logger.info(f"Email sent successfully to {to_email}")
        
        return {
            "status": "success",
            "to_email": to_email,
            "subject": subject,
            "message": "Email sent successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        
        return {
            "status": "error",
            "to_email": to_email,
            "subject": subject,
            "error": str(e)
        }


def send_personalized_emails(
    outreach_strategies: List[Dict[str, Any]],
    from_email: str = None,
    smtp_server: str = None,
    smtp_port: int = 587,
    username: str = None,
    password: str = None,
    dry_run: bool = True
) -> List[Dict[str, Any]]:
    """
    Send personalized emails to target companies.
    
    Args:
        outreach_strategies: List of outreach strategies with generated messages
        from_email: Sender email address
        smtp_server: SMTP server
        smtp_port: SMTP port
        username: SMTP username
        password: SMTP password
        dry_run: If True, only simulate sending (don't actually send)
    
    Returns:
        List of email send results
    """
    logger.info(f"Sending personalized emails to {len(outreach_strategies)} companies (dry_run={dry_run})")
    
    email_results = []
    
    for strategy in outreach_strategies:
        company_name = strategy["company_name"]
        email_message = strategy["generated_messages"].get("email", {})
        
        if not email_message:
            logger.warning(f"No email message found for {company_name}")
            continue
        
        subject = email_message["subject"]
        body = email_message["body"]
        
        # For demo purposes, use a placeholder email
        # In production, you would extract real email addresses from company data
        to_email = f"contact@{company_name.lower().replace(' ', '')}.com"
        
        if dry_run:
            logger.info(f"DRY RUN: Would send email to {to_email}")
            result = {
                "status": "dry_run",
                "company_name": company_name,
                "to_email": to_email,
                "subject": subject,
                "message": "Email would be sent in production"
            }
        else:
            result = send_email(
                to_email=to_email,
                subject=subject,
                body=body,
                from_email=from_email,
                smtp_server=smtp_server,
                smtp_port=smtp_port,
                username=username,
                password=password
            )
            result["company_name"] = company_name
        
        email_results.append(result)
    
    return email_results


def book_meeting(
    outreach_strategies: List[Dict[str, Any]],
    calendar_integration: bool = True,
    crm_integration: bool = True
) -> List[Dict[str, Any]]:
    """
    Develop meeting booking strategies and processes.
    
    Args:
        outreach_strategies: List of personalized outreach strategies
        calendar_integration: Whether to integrate with calendar systems
        crm_integration: Whether to integrate with CRM systems
    
    Returns:
        List of meeting booking strategies
    """
    logger.info(f"Creating meeting booking strategies for {len(outreach_strategies)} companies")
    
    meeting_strategies = []
    
    for strategy in outreach_strategies:
        meeting_strategy = {
            "company_name": strategy["company_name"],
            "meeting_objective": "Discuss recruiting partnership opportunities",
            "proposed_agenda": [
                "Company overview and recent funding success",
                "Current hiring challenges and timeline",
                "Our specialized blockchain recruiting services",
                "Success stories and case studies",
                "Next steps and proposal timeline"
            ],
            "calendar_integration": {
                "enabled": calendar_integration,
                "platforms": ["Calendly", "Google Calendar", "Outlook"],
                "availability": "Monday-Friday, 9 AM - 6 PM EST"
            },
            "crm_integration": {
                "enabled": crm_integration,
                "platforms": ["Salesforce", "HubSpot", "Pipedrive"],
                "pipeline_stage": "Qualification"
            },
            "follow_up_plan": [
                "Send meeting confirmation with agenda",
                "Pre-meeting research on company and key decision makers",
                "Post-meeting summary and next steps",
                "Proposal delivery within 48 hours",
                "Follow-up call to address questions"
            ]
        }
        
        meeting_strategies.append(meeting_strategy)
    
    return meeting_strategies


# Create FunctionTool objects for ADK integration
fetch_recent_funding_rounds_tool = FunctionTool(
    func=fetch_recent_funding_rounds
)

filter_blockchain_companies_tool = FunctionTool(
    func=filter_blockchain_companies
)

personalize_outreach_tool = FunctionTool(
    func=personalize_outreach
)

send_personalized_emails_tool = FunctionTool(
    func=send_personalized_emails
)

book_meeting_tool = FunctionTool(
    func=book_meeting
) 