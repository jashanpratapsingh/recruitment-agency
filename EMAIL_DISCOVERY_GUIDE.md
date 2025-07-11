# Email Discovery System Guide

This guide explains how to use the Email Discovery System to find email addresses for both individuals and companies.

## Overview

The Email Discovery System provides comprehensive email finding capabilities:

- **Individual Email Finding**: Find personal email addresses based on name and company
- **Company Admin Email Finding**: Find admin/contact emails for companies and institutions
- **Email Verification**: Verify email validity and deliverability
- **Bulk Processing**: Process multiple contacts efficiently
- **Contact Enrichment**: Add additional contact information

## Features

### 🔍 Individual Email Finding

Find email addresses for specific people at companies:

```python
from recruiting_agency.sub_agents.email_discovery_agent.tools import find_person_email

# Find email for a person at a company
result = find_person_email(
    name="John Smith",
    company="Google",
    position="Software Engineer",
    location="Mountain View, CA"
)

print(f"Found {len(result['emails'])} potential emails:")
for email, confidence, source, verification in zip(
    result['emails'], 
    result['confidence_scores'], 
    result['sources'], 
    result['verification_status']
):
    print(f"  {email} (Confidence: {confidence}%, Source: {source})")
```

**Methods Used:**
1. **Pattern Generation**: Common email patterns (firstname.lastname@domain.com)
2. **Hunter.io API**: Professional email finding service
3. **Clearbit API**: Contact enrichment and verification
4. **Web Scraping**: Public contact information

### 🏢 Company Admin Email Finding

Find admin and contact emails for companies:

```python
from recruiting_agency.sub_agents.email_discovery_agent.tools import find_company_admin_emails

# Find admin emails for a company
result = find_company_admin_emails(
    company="Microsoft",
    include_departments=True,
    include_general=True
)

print(f"General emails: {result['general_emails']}")
print(f"Department emails: {result['department_emails']}")
```

**Email Types Found:**
- **General**: admin@, contact@, info@, hello@, support@
- **Departments**: hr@, sales@, marketing@, legal@, finance@, etc.

### ✅ Email Verification

Verify email addresses are valid and deliverable:

```python
from recruiting_agency.sub_agents.email_discovery_agent.tools import verify_email

# Verify an email address
result = verify_email("john.doe@google.com")

print(f"Format valid: {result['is_valid_format']}")
print(f"Deliverable: {result['is_deliverable']}")
print(f"Confidence: {result['confidence_score']}%")
```

**Verification Methods:**
1. **Format Validation**: Regex pattern matching
2. **Domain Validation**: DNS MX record checking
3. **SMTP Verification**: Server connectivity testing
4. **Disposable Email Detection**: Filter out temporary emails

### 📦 Bulk Email Finding

Process multiple contacts efficiently:

```python
from recruiting_agency.sub_agents.email_discovery_agent.tools import bulk_email_finder

# Process multiple contacts
contacts = [
    {"name": "Alice Johnson", "company": "Google", "position": "Engineer"},
    {"name": "Bob Smith", "company": "Microsoft", "position": "Manager"},
    {"name": "Carol Davis", "company": "Stripe", "position": "Designer"}
]

result = bulk_email_finder(
    contacts=contacts,
    include_verification=True,
    max_requests=50
)

print(f"Processed: {result['processed_contacts']}")
print(f"Successful finds: {result['successful_finds']}")
print(f"Verified emails: {result['verified_emails']}")
```

### 🔍 Contact Enrichment

Add additional information to contacts:

```python
from recruiting_agency.sub_agents.email_discovery_agent.tools import enrich_contact_data

# Enrich contact data
contact = {
    "name": "Emily Chen",
    "company": "Netflix",
    "position": "Product Manager",
    "email": "emily.chen@netflix.com"
}

result = enrich_contact_data(
    contact=contact,
    include_social_media=True,
    include_company_info=True
)

print(f"Social media profiles: {len(result['social_media'])}")
print(f"Company info fields: {len(result['company_info'])}")
```

## API Configuration

To enable enhanced functionality, configure these environment variables:

### Required APIs

```bash
# Hunter.io API (for email finding)
export HUNTER_API_KEY='your-hunter-api-key'

# Clearbit API (for contact enrichment)
export CLEARBIT_API_KEY='your-clearbit-api-key'
```

### Optional Configuration

```bash
# Enable SMTP verification (optional)
export ENABLE_SMTP_VERIFICATION='true'

# Email sending configuration (for outreach)
export BD_AGENT_EMAIL='your-email@gmail.com'
export BD_AGENT_EMAIL_PASSWORD='your-app-password'
```

## Usage Examples

### Example 1: Find Individual Email

```python
# Find email for a specific person
result = find_person_email(
    name="Sarah Johnson",
    company="Stripe",
    position="Product Manager"
)

if result['emails']:
    best_email = result['emails'][0]  # Highest confidence
    print(f"Best email for Sarah: {best_email}")
else:
    print("No email found")
```

### Example 2: Find Company Admin Emails

```python
# Find admin emails for outreach
result = find_company_admin_emails(
    company="Airbnb",
    include_departments=True
)

# Get HR email for recruiting
hr_emails = [email for email in result['department_emails'] 
             if 'hr' in email or 'recruiting' in email]
print(f"HR emails: {hr_emails}")
```

### Example 3: Verify and Use Email

```python
# Find and verify email
email_result = find_person_email("John Doe", "Google")
if email_result['emails']:
    email = email_result['emails'][0]
    verify_result = verify_email(email)
    
    if verify_result['is_deliverable']:
        print(f"Verified email: {email}")
        # Use email for outreach
    else:
        print(f"Email not deliverable: {email}")
```

### Example 4: Bulk Processing

```python
# Process a list of contacts
contacts = [
    {"name": "Alice", "company": "Google"},
    {"name": "Bob", "company": "Microsoft"},
    {"name": "Carol", "company": "Stripe"}
]

bulk_result = bulk_email_finder(contacts, include_verification=True)

# Use results for outreach
for contact_result in bulk_result['contacts_with_emails']:
    contact = contact_result['contact']
    emails = contact_result['email_results']['emails']
    print(f"{contact['name']}: {emails}")
```

## Integration with Recruiting Agency

The Email Discovery System is integrated into the main recruiting agency:

```python
from recruiting_agency.agent_factory import AgentFactory

# Create agent with email discovery capabilities
agent = AgentFactory.create_main_agent()

# The agent can now use email discovery tools
response = agent.run("Find the email for John Smith at Google")
```

## Best Practices

### 1. Privacy and Compliance
- Always respect privacy laws and terms of service
- Use data responsibly and ethically
- Verify consent before using found emails

### 2. Data Quality
- Prioritize accuracy over quantity
- Verify emails when possible
- Use multiple data sources for better results

### 3. Rate Limiting
- Respect API rate limits
- Use bulk processing for efficiency
- Implement proper error handling

### 4. Verification
- Always verify emails before outreach
- Check for disposable email domains
- Validate domain and format

## Error Handling

The system includes comprehensive error handling:

```python
try:
    result = find_person_email("John Doe", "Google")
    if result['emails']:
        print(f"Found: {result['emails'][0]}")
    else:
        print("No email found")
except Exception as e:
    print(f"Error: {str(e)}")
    # Handle gracefully
```

## Performance Considerations

- **API Limits**: Respect rate limits for external APIs
- **Caching**: Consider caching results for repeated queries
- **Bulk Processing**: Use bulk operations for efficiency
- **Verification**: Balance accuracy vs. speed

## Troubleshooting

### Common Issues

1. **No emails found**
   - Check company name spelling
   - Try different name variations
   - Verify API keys are configured

2. **Low confidence scores**
   - Use more specific company information
   - Try different name formats
   - Enable additional data sources

3. **API errors**
   - Check API key validity
   - Verify rate limits
   - Check network connectivity

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Advanced Usage

### Custom Email Patterns

You can extend the system with custom patterns:

```python
def custom_email_patterns(name, domain):
    # Add your custom patterns here
    patterns = []
    # ... custom logic
    return patterns
```

### Integration with CRM

```python
# Integrate with your CRM system
def sync_to_crm(contact_data, email_results):
    # Add CRM integration logic
    pass
```

## Support

For issues or questions:
1. Check the example scripts
2. Review the API documentation
3. Test with the demo script: `python email_discovery_example.py`

## License

This system is part of the Pyxis project and follows the same licensing terms. 