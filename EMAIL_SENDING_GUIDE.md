# Email Sending Guide

This guide explains how to use the email sending capabilities integrated with the Email Discovery Agent in the Recruiting Agency chatbot.

## Overview

The Email Discovery Agent now includes comprehensive email sending functionality that allows you to:

- Send individual emails with HTML content and attachments
- Send bulk personalized emails to multiple recipients
- Create and execute email campaigns
- Send follow-up emails with delays
- Integrate email discovery with email sending workflows

## Setup

### 1. Environment Variables

Set up your email credentials in environment variables:

```bash
export BD_AGENT_EMAIL='your-email@gmail.com'
export BD_AGENT_EMAIL_PASSWORD='your-app-password'
```

**Important Notes:**
- For Gmail, you must use an **App Password**, not your regular password
- Enable 2-factor authentication on your Google account
- Generate an App Password: https://support.google.com/accounts/answer/185833
- The App Password is a 16-character code that looks like: `abcd efgh ijkl mnop`

### 2. Gmail Setup

1. Go to your Google Account settings
2. Enable 2-Step Verification
3. Go to Security → App passwords
4. Generate a new app password for "Mail"
5. Use this password in `BD_AGENT_EMAIL_PASSWORD`

### 3. Alternative Email Providers

The system defaults to Gmail but supports other SMTP providers:

```bash
# For Outlook/Hotmail
export SMTP_SERVER='smtp-mail.outlook.com'
export SMTP_PORT='587'

# For Yahoo
export SMTP_SERVER='smtp.mail.yahoo.com'
export SMTP_PORT='587'

# For custom SMTP
export SMTP_SERVER='your-smtp-server.com'
export SMTP_PORT='587'
```

## Email Sending Tools

### 1. Send Individual Email

Send a single email with optional HTML content and attachments.

**Function:** `send_email`

**Parameters:**
- `to_email`: Recipient email address
- `subject`: Email subject line
- `body`: Plain text email body
- `html_body`: HTML version of email body (optional)
- `attachments`: List of file paths to attach (optional)
- `from_email`: Sender email (uses BD_AGENT_EMAIL if not provided)
- `smtp_server`: SMTP server (defaults to Gmail)
- `smtp_port`: SMTP port (defaults to 587)
- `username`: SMTP username (uses BD_AGENT_EMAIL if not provided)
- `password`: SMTP password (uses BD_AGENT_EMAIL_PASSWORD if not provided)

**Example:**
```python
response = email_discovery_agent.run(
    "Send an email to john@example.com with subject 'Test Email' "
    "and body 'This is a test email from the Email Discovery Agent'. "
    "Use dry_run=True for safety."
)
```

### 2. Send Bulk Emails

Send personalized emails to multiple recipients with template variables.

**Function:** `send_bulk_emails`

**Parameters:**
- `email_list`: List of dictionaries with recipient info
- `subject_template`: Email subject template with variables
- `body_template`: Email body template with variables
- `html_template`: HTML version of email body template (optional)
- `dry_run`: If True, only simulate sending (recommended for testing)
- `delay_seconds`: Delay between emails to avoid rate limiting

**Template Variables:**
- `{name}`: Recipient's name
- `{company}`: Company name
- `{position}`: Job position/title
- Any other fields from the contact data

**Example:**
```python
contacts = [
    {"name": "John Smith", "email": "john@example.com", "company": "Tech Corp"},
    {"name": "Sarah Johnson", "email": "sarah@example.com", "company": "Innovation Inc"}
]

response = email_discovery_agent.run(
    f"Send bulk emails to these contacts: {json.dumps(contacts)}\n"
    f"Subject Template: Partnership Opportunity - {{company}}\n"
    f"Body Template: Hi {{name}},\n\nI'm reaching out about {{company}}...\n\n"
    f"Use dry_run=True and include a 2-second delay between emails."
)
```

### 3. Create Email Campaign

Create and execute a complete email campaign.

**Function:** `create_email_campaign`

**Parameters:**
- `target_contacts`: List of contacts to email
- `campaign_name`: Name of the campaign
- `subject_line`: Email subject line
- `email_body`: Email body text
- `html_body`: HTML version of email body (optional)
- `schedule_time`: When to send the campaign (ISO format, optional)
- `dry_run`: If True, only simulate sending

**Example:**
```python
response = email_discovery_agent.run(
    f"Create an email campaign with these details:\n"
    f"Campaign Name: Recruiting Partnership Outreach\n"
    f"Contacts: {json.dumps(contacts)}\n"
    f"Subject: Partnership Opportunity - {{company}}\n"
    f"Body: Hi {{name}},\n\nI'm reaching out about {{company}}...\n\n"
    f"Use dry_run=True for safety."
)
```

### 4. Send Follow-up Email

Send a follow-up email after a specified delay.

**Function:** `send_follow_up_email`

**Parameters:**
- `original_email_data`: Data from the original email sent
- `follow_up_subject`: Subject for the follow-up email
- `follow_up_body`: Body for the follow-up email
- `days_delay`: Number of days to wait before sending follow-up

**Example:**
```python
response = email_discovery_agent.run(
    f"Send a follow-up email to {original_email} with subject 'Follow-up' "
    f"and body 'Just following up on our previous conversation...' "
    f"Use dry_run=True for safety."
)
```

## Complete Workflow Examples

### Example 1: Find and Send Individual Emails

```python
# Step 1: Find email for a person
response = email_discovery_agent.run(
    "Find the email address for John Smith at Google"
)

# Step 2: Extract found email
if response.get("email_discovery_output"):
    emails = response["email_discovery_output"].get("emails", [])
    if emails:
        target_email = emails[0]
        
        # Step 3: Send email
        send_response = email_discovery_agent.run(
            f"Send an email to {target_email} with subject 'Partnership Opportunity' "
            f"and body 'Hi John, I'm reaching out about potential partnership...' "
            f"Use dry_run=True for safety."
        )
```

### Example 2: Bulk Outreach Campaign

```python
# Step 1: Find emails for multiple companies
companies = ["Tesla", "SpaceX", "Netflix"]
all_contacts = []

for company in companies:
    # Find admin emails
    admin_response = email_discovery_agent.run(
        f"Find admin and contact email addresses for {company}"
    )
    
    # Find individual emails for key positions
    individual_response = email_discovery_agent.run(
        f"Find email addresses for HR Director and CTO at {company}"
    )
    
    # Combine results
    contacts = []
    # ... process and combine results ...
    all_contacts.extend(contacts)

# Step 2: Send bulk campaign
if all_contacts:
    campaign_response = email_discovery_agent.run(
        f"Create an email campaign for these contacts: {json.dumps(all_contacts)}\n"
        f"Campaign Name: Recruiting Partnership Outreach\n"
        f"Subject: Partnership Opportunity - {{company}}\n"
        f"Body: Hi {{name}},\n\nI'm reaching out about {{company}}...\n\n"
        f"Use dry_run=True for safety."
    )
```

### Example 3: Email Verification Before Sending

```python
# Step 1: Find email
response = email_discovery_agent.run(
    "Find the email for Sarah Johnson at Microsoft"
)

# Step 2: Verify email
if response.get("email_discovery_output"):
    emails = response["email_discovery_output"].get("emails", [])
    if emails:
        email_to_verify = emails[0]
        
        verify_response = email_discovery_agent.run(
            f"Verify the email address: {email_to_verify}"
        )
        
        # Step 3: Send only if verified
        if verify_response.get("email_discovery_output", {}).get("is_deliverable"):
            send_response = email_discovery_agent.run(
                f"Send an email to {email_to_verify} with subject 'Verified Contact' "
                f"and body 'Hi Sarah, I verified your email and would like to connect...' "
                f"Use dry_run=True for safety."
            )
```

## Best Practices

### 1. Safety First
- **Always use `dry_run=True` for testing**
- Verify email addresses before sending
- Test with small batches first
- Monitor email sending limits

### 2. Personalization
- Use template variables for personalization
- Include recipient's name and company
- Reference specific details about their company
- Keep content relevant and professional

### 3. Rate Limiting
- Add delays between bulk emails (1-3 seconds)
- Respect email provider limits
- Monitor bounce rates and spam complaints
- Use proper email authentication

### 4. Content Quality
- Write clear, professional subject lines
- Keep emails concise and focused
- Include clear call-to-action
- Proofread before sending

### 5. Compliance
- Respect CAN-SPAM laws
- Include unsubscribe options
- Honor opt-out requests
- Maintain proper sender identification

## Error Handling

### Common Issues

1. **Authentication Errors**
   ```
   Error: Email credentials not found
   Solution: Set BD_AGENT_EMAIL and BD_AGENT_EMAIL_PASSWORD
   ```

2. **SMTP Connection Errors**
   ```
   Error: Failed to connect to SMTP server
   Solution: Check internet connection and SMTP settings
   ```

3. **Rate Limiting**
   ```
   Error: Too many emails sent
   Solution: Add delays between emails and respect limits
   ```

4. **Invalid Email Format**
   ```
   Error: Invalid email address
   Solution: Verify email format before sending
   ```

### Debugging Tips

1. **Enable Logging**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Test with Dry Run**
   ```python
   # Always test with dry_run=True first
   response = email_discovery_agent.run(
       "Send email with dry_run=True"
   )
   ```

3. **Verify Environment Variables**
   ```python
   import os
   print(f"Email: {os.getenv('BD_AGENT_EMAIL')}")
   print(f"Password set: {'Yes' if os.getenv('BD_AGENT_EMAIL_PASSWORD') else 'No'}")
   ```

## Integration with Chatbot

The email sending functionality is fully integrated with the recruiting agency chatbot. You can use it directly in conversations:

```
User: "Find the email for John Smith at Google and send him a partnership proposal"

Agent: I'll help you find John Smith's email and send a partnership proposal. Let me start by searching for his email address...

[Agent finds email and sends proposal with dry_run=True for safety]
```

## Security Considerations

1. **Environment Variables**: Never hardcode email credentials
2. **App Passwords**: Use app passwords instead of regular passwords
3. **Rate Limiting**: Respect email provider limits
4. **Content Filtering**: Avoid spam trigger words
5. **Authentication**: Use proper SMTP authentication

## Monitoring and Analytics

Track your email campaigns:

1. **Send Status**: Monitor success/failure rates
2. **Delivery Rates**: Track email delivery success
3. **Response Rates**: Monitor recipient engagement
4. **Bounce Rates**: Track invalid email addresses
5. **Spam Complaints**: Monitor reputation

## Support

For issues with email sending:

1. Check environment variables are set correctly
2. Verify Gmail App Password is working
3. Test with dry_run=True first
4. Check SMTP server settings
5. Monitor error logs for specific issues

## Example Scripts

See the following example files for complete working examples:

- `email_discovery_and_sending_example.py`: Comprehensive examples
- `email_discovery_example.py`: Basic email discovery
- `enhanced_bd_example.py`: Business development integration

Run examples with:
```bash
python email_discovery_and_sending_example.py
```

This guide covers all aspects of the email sending functionality. The system is designed to be safe, efficient, and compliant with email best practices. 