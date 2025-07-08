# Model Selection and Auto-Detection

This document explains how the Recruiting Agency handles model selection between voice and text interactions, including automatic detection capabilities.

## Overview

The Recruiting Agency supports both voice and text interactions with intelligent auto-detection that chooses the appropriate model based on multiple factors:

- **Voice Model**: `gemini-2.0-flash-live-001` (supports real-time voice interactions)
- **Text Model**: `gemini-1.5-pro-latest` (optimized for text-based interactions)

## Auto-Detection Methods

The system uses multiple detection methods to determine if an interaction should use voice or text models:

### 1. HTTP Headers Detection
Checks for voice-specific headers:
```python
# Voice indicators
headers = {
    "content-type": "audio/wav",
    "x-voice-interaction": "true",
    "x-webrtc": "enabled",
    "x-voice-api": "active"
}
```

### 2. Environment Variables
Checks for voice-related environment variables:
```bash
# Voice mode indicators
export VOICE_INTERACTION=true
export AUDIO_INPUT=true
export SPEECH_RECOGNITION=true
export RECRUITING_AGENCY_VOICE_MODE=true
```

### 3. Input Format Detection
Analyzes input data format:
```python
# Audio file extensions
audio_files = [".wav", ".mp3", ".m4a", ".ogg", ".flac", ".aac"]

# Binary data detection
if isinstance(input_data, bytes):
    # Check if it's audio vs text data
```

### 4. URL Pattern Detection
Checks URL patterns for voice endpoints:
```python
# Voice URL patterns
voice_patterns = [
    '/voice', '/audio', '/speech', '/call', '/phone',
    '/webrtc', '/stream', '/live', '/conversation'
]
```

### 5. User-Agent Detection
Analyzes User-Agent strings for voice applications:
```python
# Voice app indicators
voice_apps = [
    'voice', 'audio', 'speech', 'call', 'phone',
    'webrtc', 'stream', 'live', 'conversation'
]
```

## Usage Examples

### Basic Auto-Detection
```python
from recruiting_agency.model_selector import get_model_for_interaction

# Auto-detect based on context
model = get_model_for_interaction(
    interaction_type="auto",
    headers={"content-type": "audio/wav"},
    url="https://api.example.com/voice/stream",
    user_agent="VoiceApp/1.0"
)
```

### Manual Override
```python
# Force voice model
model = get_model_for_interaction(
    interaction_type="auto",
    force_model="gemini-2.0-flash-live-001"
)

# Force text model
model = get_model_for_interaction(
    interaction_type="auto",
    force_model="gemini-1.5-pro-latest"
)
```

### Agent Factory Usage
```python
from recruiting_agency.agent_factory import AgentFactory

# Create agents with auto-detection
agents = AgentFactory.create_all_agents(
    interaction_type="auto",
    headers={"content-type": "audio/wav"},
    url="https://api.example.com/voice",
    user_agent="VoiceApp/1.0"
)

# Access individual agents
main_agent = agents["main_agent"]
bd_agent = agents["bd_agent"]
```

## Web Integration

For web applications, the auto-detection works seamlessly with request contexts:

```python
# Flask/FastAPI integration
def handle_request(request):
    model = get_model_for_interaction(
        interaction_type="auto",
        headers=request.headers,
        url=request.url,
        user_agent=request.headers.get("user-agent"),
        input_data=request.data
    )
    
    # Create agent with detected model
    agent = AgentFactory.create_main_agent(
        interaction_type="auto",
        headers=request.headers,
        url=request.url,
        user_agent=request.headers.get("user-agent"),
        input_data=request.data
    )
```

## Model Capabilities

### Voice Model (`gemini-2.0-flash-live-001`)
- ✅ Real-time voice interactions
- ✅ Streaming responses
- ✅ Turn detection
- ✅ Audio input/output
- ✅ Text input/output

### Text Model (`gemini-1.5-pro-latest`)
- ✅ Text interactions
- ✅ High-quality responses
- ✅ Cost-effective
- ❌ No voice capabilities
- ❌ No streaming

## Configuration

### Environment Variables
```bash
# Enable voice mode
export VOICE_INTERACTION=true

# Force specific model
export RECRUITING_AGENCY_MODEL=gemini-2.0-flash-live-001

# Disable auto-detection
export RECRUITING_AGENCY_INTERACTION_TYPE=text
```

### Headers for Voice Detection
```http
Content-Type: audio/wav
X-Voice-Interaction: true
X-WebRTC: enabled
X-Voice-API: active
```

## Testing Auto-Detection

Run the auto-detection demo:
```bash
cd python/agents/recruiting-agency
python auto_detection_example.py
```

This will demonstrate:
- All detection methods
- Auto-detection scenarios
- Agent creation with auto-detection
- Manual override capabilities
- Web integration examples

## Migration Guide

### From Manual Model Selection
```python
# Old way
agent = RecruitingAgencyAgent(model="gemini-1.5-pro-latest")

# New way with auto-detection
agent = AgentFactory.create_main_agent(interaction_type="auto")
```

### From Fixed Interaction Type
```python
# Old way
agent = RecruitingAgencyAgent(model="gemini-2.0-flash-live-001")

# New way with context
agent = AgentFactory.create_main_agent(
    interaction_type="auto",
    headers={"content-type": "audio/wav"}
)
```

## Best Practices

1. **Default to Auto**: Use `interaction_type="auto"` for maximum flexibility
2. **Provide Context**: Pass headers, URL, and user-agent for better detection
3. **Test Both Modes**: Verify your application works with both voice and text
4. **Fallback Gracefully**: Handle cases where auto-detection defaults to text
5. **Monitor Usage**: Track which models are being used in production

## Troubleshooting

### Auto-Detection Always Returns Text
- Check if voice indicators are present in headers/URL
- Verify environment variables are set correctly
- Ensure input data format is recognized as audio

### Voice Model Not Available
- Verify you have access to `gemini-2.0-flash-live-001`
- Check API quotas and permissions
- Consider falling back to text model

### Performance Issues
- Voice models may have higher latency
- Consider caching model selection decisions
- Monitor response times for both models 