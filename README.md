# Recruiting Agency Agent

A comprehensive AI-powered recruiting agency that orchestrates specialized sub-agents for business development, candidate outreach, marketing content, backend matching, and real-time research to provide end-to-end hiring solutions.

## 🏗️ Architecture

The recruiting agency consists of a main coordinator agent that orchestrates specialized sub-agents:

- **Recruiting Coordinator**: Main orchestrator agent
- **BD Agent**: Business development and market analysis
- **Candidate Outreach Agent**: Engagement and communication strategies
- **Marketing Content Agent**: Job descriptions and promotional materials
- **Backend Matching Agent**: ATS, CRM, and automation recommendations
- **Google Search Agent**: Real-time information and research fallback

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Basic Usage

```python
from recruiting_agency.agent_factory import create_auto_agent

# Create the main agent
agent = create_auto_agent()

# Use the agent
response = agent.invoke({
    "query": "I need help hiring blockchain developers for my startup"
})
```

## 🔧 Sub-Agents

### BD Agent (Business Development)

Specializes in identifying blockchain companies with recent funding and business development activities.

**Features:**
- Fetch recent funding rounds from multiple APIs
- Filter blockchain companies by criteria
- Personalize outreach messages
- Send emails and book meetings

**Example:**
```python
from recruiting_agency.agent_factory import AgentFactory

bd_agent = AgentFactory.create_bd_agent()
response = bd_agent.invoke({
    "query": "Find blockchain companies with recent Series A funding"
})
```

### Candidate Outreach Agent

Handles candidate engagement and communication strategies.

**Features:**
- Personalized messaging
- Multi-channel outreach
- Follow-up strategies
- Engagement tracking

### Marketing Content Agent

Creates job descriptions and promotional materials.

**Features:**
- Job description generation
- Employer branding content
- Social media campaigns
- A/B testing strategies

### Backend Matching Agent

Recommends ATS, CRM, and automation solutions.

**Features:**
- Platform comparisons
- Integration recommendations
- Automation workflows
- Analytics setup

### Google Search Agent

Provides real-time information and research when other agents need current data.

**Features:**
- Real-time information retrieval
- Current market data and trends
- Fact verification
- Research support for other agents
- Fallback for outdated information

**Example:**
```python
from recruiting_agency.agent_factory import AgentFactory

search_agent = AgentFactory.create_google_search_agent()
response = search_agent.invoke({
    "query": "What are the current salary trends for blockchain developers?"
})
```

## 🔄 Fallback Strategy

The Google Search Agent serves as a fallback when other agents cannot provide current or accurate information:

- **BD Agent** needs recent funding data → Google Search Agent
- **Marketing Agent** needs current trends → Google Search Agent  
- **Backend Agent** needs latest tool info → Google Search Agent
- **Outreach Agent** needs market insights → Google Search Agent

## 🎛️ Model Selection

The system uses a simplified model selection that ensures reliability:

### Single Model Approach
```python
# All interaction types use the same reliable model
voice_agent = AgentFactory.create_main_agent("voice")
text_agent = AgentFactory.create_main_agent("text")
auto_agent = AgentFactory.create_main_agent("auto")

# All use gemini-1.5-pro-latest
```

### Benefits
- ✅ **No API errors** - Uses only supported models
- ✅ **Consistent performance** - Same model for all interactions
- ✅ **Simple configuration** - No complex model selection logic
- ✅ **Reliable deployment** - Works across all environments

## 📊 API Integration

### BD Agent APIs

The BD Agent integrates with multiple funding data APIs:

- **Crunchbase API**: Company and funding data
- **Dealroom API**: European startup ecosystem
- **Tracxn API**: Global startup intelligence
- **PitchBook API**: Private market data

### Environment Setup

Create a `.env` file with your API keys:

```bash
# Crunchbase API
CRUNCHBASE_API_KEY=your_crunchbase_key

# Dealroom API  
DEALROOM_API_KEY=your_dealroom_key

# Tracxn API
TRACXN_API_KEY=your_tracxn_key

# PitchBook API
PITCHBOOK_API_KEY=your_pitchbook_key

# Email Configuration (for outreach)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

### API Key Setup

#### Crunchbase API
1. Visit [Crunchbase API](https://data.crunchbase.com/docs/using-the-api)
2. Sign up for an account
3. Request API access
4. Get your API key from the dashboard

#### Dealroom API
1. Visit [Dealroom](https://dealroom.co/)
2. Sign up for an account
3. Contact support for API access
4. Receive API credentials

#### Tracxn API
1. Visit [Tracxn](https://tracxn.com/)
2. Sign up for an account
3. Request API access
4. Get API key from your account

#### PitchBook API
1. Visit [PitchBook](https://pitchbook.com/)
2. Sign up for an account
3. Contact sales for API access
4. Receive API credentials

## 🧪 Testing

### Run Tests
```bash
# Run all tests
poetry run pytest

# Run specific test
poetry run pytest tests/test_bd_agent.py
```

### Example Scripts

```bash
# Test BD Agent
python3 bd_agent_example.py

# Test Google Search Agent
python3 google_search_agent_example.py

# Test fallback functionality
python3 test_google_search_fallback.py

# Test API integration
python3 api_integration_example.py

# Test Tracxn-only mode
python3 tracxn_only_example.py

# Test simplified model selection
python3 test_simplified_model.py
```

## 🚀 Deployment

### Render Deployment

The agent is configured for deployment on Render with Poetry:

```yaml
# render.yaml
services:
  - type: web
    name: recruiting-agency
    env: python
    buildCommand: poetry install
    startCommand: python start_render.py
```

### Local Development

```bash
# Start the web interface
adk web

# Or use the wrapper script
python start_render.py
```

## 📁 Project Structure

```
recruiting-agency/
├── recruiting_agency/
│   ├── __init__.py
│   ├── agent.py
│   ├── agent_factory.py
│   ├── model_selector.py
│   ├── prompt.py
│   └── sub_agents/
│       ├── bd_agent/
│       ├── candidate_outreach_agent/
│       ├── marketing_content_agent/
│       ├── backend_matching_agent/
│       └── google_search_agent/
├── tests/
├── deployment/
├── eval/
├── pyproject.toml
└── README.md
```

## 🔍 Key Features

- **Multi-Agent Architecture**: Specialized sub-agents for different recruiting tasks
- **Real-time Data**: Google Search Agent for current information
- **API Integration**: Multiple funding data sources
- **Simplified Model Selection**: Reliable single-model approach
- **Fallback Strategy**: Automatic redirection to Google Search Agent
- **Deployment Ready**: Configured for Render deployment

## 📚 Documentation

- [Model Selection Guide](MODEL_SELECTION.md)
- [Auto-Detection Summary](AUTO_DETECTION_SUMMARY.md)
- [Interaction Examples](interaction_examples.py)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the Apache License 2.0. 