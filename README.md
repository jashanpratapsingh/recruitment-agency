# Recruiting Agency Agent

A comprehensive AI-driven recruiting solution that orchestrates specialized sub-agents to provide end-to-end hiring support, with enhanced blockchain company identification and personalized outreach capabilities.

## Overview

The RecruitingAgencyAgent is a master agent that delegates tasks to specialized sub-agents to provide comprehensive recruiting solutions. It takes high-level prompts like "Help me with hiring for a blockchain startup" and routes tasks to the appropriate specialized agents.

## Architecture

The agent follows a coordinator pattern with four specialized sub-agents:

### 1. BD Agent (Business Development) - Enhanced
- **Core Functions:**
  - `fetch_recent_funding_rounds()` - Identifies blockchain companies with recent funding
  - `filter_blockchain_companies()` - Filters companies based on criteria
  - `personalize_outreach()` - Creates personalized outreach strategies with LLM-generated messages
  - `send_personalized_emails()` - Sends personalized emails to target companies
  - `book_meeting()` - Develops meeting booking strategies
- **API Integration Placeholders:**
  - Crunchbase API for funding data
  - Dealroom API for European market data
  - Tracxn API for comprehensive startup data
  - PitchBook API for detailed financial information
- **Specialized Features:**
  - Blockchain ecosystem expertise
  - Funding round analysis
  - Target company identification
  - Personalized outreach automation
  - **LLM-powered message generation**
  - **Automated email sending**

### 2. Candidate Outreach Agent
- Develops comprehensive candidate outreach strategies
- Creates channel-specific engagement tactics
- Designs messaging frameworks and communication templates
- Optimizes candidate experience and relationship building

### 3. Marketing Content Agent
- Creates compelling job descriptions and promotional content
- Develops employer branding materials
- Designs social media and email marketing campaigns
- Crafts inclusive and engaging recruitment content

### 4. Backend Matching Agent
- Recommends optimal ATS (Applicant Tracking System) solutions
- Designs CRM integration strategies
- Provides analytics and reporting tool recommendations
- Creates workflow automation solutions

## Enhanced BD Agent Features

### Blockchain Company Identification
The BD Agent is specifically designed to identify and engage blockchain companies that have recently raised funding:

```python
from recruiting_agency.sub_agents.bd_agent.tools import (
    fetch_recent_funding_rounds,
    filter_blockchain_companies,
    personalize_outreach,
    send_personalized_emails,
    generate_personalized_message
)

# Fetch companies with recent funding
companies = fetch_recent_funding_rounds(
    sector="blockchain",
    min_funding_amount=10000000,
    timeframe_days=90
)

# Filter target companies
target_companies = filter_blockchain_companies(
    companies=companies,
    min_funding=20000000,
    target_stages=["Series A", "Series B"]
)

# Create personalized outreach with LLM-generated messages
outreach_strategies = personalize_outreach(
    target_companies=target_companies,
    message_types=["email", "linkedin"]
)

# Send personalized emails
email_results = send_personalized_emails(outreach_strategies, dry_run=True)
```

### Personalized Message Generation
The BD Agent uses LLM logic to generate custom messages for each company:

#### Email Template Features:
- Personalized greeting with key decision maker
- Congratulatory message referencing funding round
- Company-specific value proposition
- Call-to-action for meeting
- Professional signature

#### LinkedIn Template Features:
- Shorter, more casual tone
- Emoji usage for engagement
- Direct call-to-action
- Professional but approachable

### Automated Email Sending
The agent can send personalized emails on your behalf:

```python
# Generate personalized message for a specific company
company = {
    "company_name": "Chainlink Labs",
    "funding_amount": 225000000,
    "funding_round": "Series B",
    "description": "leading decentralized oracle networks",
    "hiring_plans": "aggressive hiring for engineering roles",
    "key_people": ["Sergey Nazarov", "Steve Ellis"]
}

# Generate email message
email_message = generate_personalized_message(company, "email")
print(f"Subject: {email_message['subject']}")
print(f"Body: {email_message['body']}")

# Send the email
send_email(
    to_email="contact@chainlinklabs.com",
    subject=email_message['subject'],
    body=email_message['body']
)
```

### API Integration
The BD Agent integrates with multiple funding data APIs to fetch real-time company and funding information:

- **Tracxn API**: Startup analytics and funding trends (prioritized)
- **Crunchbase API**: Comprehensive funding and company data
- **Dealroom API**: European market insights
- **PitchBook API**: Detailed financial information

#### API Features
- **Tracxn-first approach**: Prioritizes Tracxn API when available for optimal blockchain data
- **Multi-source data aggregation**: Combines data from all available APIs
- **Duplicate removal**: Automatically removes duplicate companies across sources
- **Data standardization**: Normalizes data from different API formats
- **Error handling**: Graceful degradation when APIs are unavailable
- **Fallback data**: Returns sample data when no APIs are configured
- **Filtering options**: Filter by funding amount, company stage, sector, timeframe
- **Sorting**: Companies sorted by funding amount (highest first)

## Usage

### Basic Usage

```python
from recruiting_agency import root_agent

# Start a conversation with the recruiting coordinator
response = root_agent.chat("Help me with hiring for a blockchain startup")
```

### Enhanced BD Agent Usage

```python
# Run the complete BD Agent workflow
python bd_agent_example.py

# Run the enhanced workflow with email sending
python enhanced_bd_example.py
```

### Example Interaction

```
User: "Help me with hiring for a blockchain startup"

Agent: "Hello! I'm your Recruiting Agency Coordinator, here to help you navigate the complex world of hiring and talent acquisition..."

[Agent then guides through the 4-step process:
1. Business Development Analysis (Enhanced with blockchain focus and email sending)
2. Candidate Outreach Strategy  
3. Marketing Content Creation
4. Backend Matching and Integration]
```

## Features

- **Comprehensive Analysis**: Each sub-agent provides detailed, research-backed insights
- **Blockchain Expertise**: Specialized knowledge of blockchain ecosystem and funding trends
- **Multi-Channel Strategy**: Covers all aspects of modern recruiting
- **Data-Driven Recommendations**: Uses current market research and best practices
- **API Integration Ready**: Placeholders for major funding data providers
- **LLM-Powered Personalization**: Custom message generation for each company
- **Automated Email Sending**: Send personalized emails on your behalf
- **Scalable Solutions**: Adapts to different company sizes and industries
- **Integration Focus**: Recommends technical solutions and automation

## Installation

```bash
cd python/agents/recruiting-agency
pip install -e .
```

## Dependencies

- google-adk
- google-genai
- pydantic
- python-dotenv

## Email Configuration

To enable email sending functionality:

1. **Set Environment Variables:**
   ```bash
   export BD_AGENT_EMAIL='your-email@gmail.com'
   export BD_AGENT_EMAIL_PASSWORD='your-app-password'
   ```

2. **Configure SMTP Settings (Optional):**
   ```python
   send_personalized_emails(
       outreach_strategies=strategies,
       smtp_server="smtp.gmail.com",
       smtp_port=587,
       dry_run=False  # Set to False to actually send emails
   )
   ```

3. **Gmail App Password Setup:**
   - Enable 2-factor authentication
   - Generate app password for the BD agent
   - Use app password instead of regular password

## API Integration Setup

The BD Agent now includes full API integration for real-time funding data:

### 1. API Configuration

Set the following environment variables to enable API integration:

```bash
export CRUNCHBASE_API_KEY="your_crunchbase_api_key"
export DEALROOM_API_KEY="your_dealroom_api_key"
export TRACXN_API_KEY="your_tracxn_api_key"
export PITCHBOOK_API_KEY="your_pitchbook_api_key"
```

### 2. API Setup Instructions

**Crunchbase API:**
- Visit: https://data.crunchbase.com/docs/using-the-api
- Sign up for API access
- Set environment variable: `CRUNCHBASE_API_KEY`

**Dealroom API:**
- Visit: https://dealroom.co/api
- Request API access
- Set environment variable: `DEALROOM_API_KEY`

**Tracxn API:**
- Visit: https://tracxn.com/api
- Sign up for API access
- Set environment variable: `TRACXN_API_KEY`

**PitchBook API:**
- Visit: https://pitchbook.com/api
- Request API access
- Set environment variable: `PITCHBOOK_API_KEY`

### 3. Testing API Integration

```bash
# Test the API integration
python api_integration_example.py

# Test Tracxn-only workflow
python tracxn_only_example.py

# Run tests for API functionality
python -m pytest tests/test_api_integration.py -v
```

### 4. API Features

- **Automatic data aggregation** from all available APIs
- **Duplicate removal** across multiple data sources
- **Error handling** with graceful degradation
- **Fallback to sample data** when APIs are unavailable
- **Configurable filtering** by funding amount, stage, sector, timeframe
- **Data standardization** across different API formats

## Testing

Run the comprehensive test suite:

```bash
# Test BD Agent tools
python -m pytest tests/test_bd_agent_tools.py -v

# Test email functionality
python -m pytest tests/test_email_functionality.py -v

# Test API integration
python -m pytest tests/test_api_integration.py -v

# Run enhanced example
python enhanced_bd_example.py

# Test API integration example
python api_integration_example.py
```

## License

Apache License 2.0

## Disclaimer

This tool is for educational and informational purposes only. The information provided does not constitute professional recruiting advice, and users should consult with qualified professionals before making hiring decisions. 