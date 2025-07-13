"""Email Sender Agent Tools - Dedicated email sending functionality."""

import os
import smtplib
import datetime
import time
import logging
from typing import Dict, Any, List, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from google.adk.tools import FunctionTool

# Set up logging
logger = logging.getLogger(__name__)

def send_email(
    to_email: str,
    subject: str,
    body: str,
    from_email: Optional[str] = None,
    smtp_server: Optional[str] = None,
    smtp_port: int = 587,
    username: Optional[str] = None,
    password: Optional[str] = None,
    html_body: Optional[str] = None,
    attachments: Optional[List[str]] = None,
    dry_run: bool = True
) -> Dict[str, Any]:
    """
    Send a single email with optional HTML and attachments.
    
    Args:
        to_email: Recipient email address
        subject: Email subject line
        body: Email body text
        from_email: Sender email address
        smtp_server: SMTP server (defaults to Gmail)
        smtp_port: SMTP port (defaults to 587)
        username: SMTP username (uses EMAIL_SENDER_EMAIL if not provided)
        password: SMTP password (uses EMAIL_SENDER_PASSWORD if not provided)
        html_body: HTML version of email body (optional)
        attachments: List of file paths to attach (optional)
        dry_run: If True, only simulate sending (don't actually send)
    
    Returns:
        Dictionary with send status and details
    """
    # Default to Gmail SMTP if not specified
    if smtp_server is None:
        smtp_server = "smtp.gmail.com"
    
    if from_email is None:
        from_email = os.getenv("EMAIL_SENDER_EMAIL")
    
    if username is None:
        username = os.getenv("EMAIL_SENDER_EMAIL")
    
    if password is None:
        password = os.getenv("EMAIL_SENDER_PASSWORD")
    
    # Handle dry run
    if dry_run:
        logger.info(f"DRY RUN: Would send email to {to_email}")
        return {
            "status": "dry_run",
            "to_email": to_email,
            "subject": subject,
            "message": "Email would be sent in production",
            "timestamp": str(datetime.datetime.now())
        }
    
    # Validate required environment variables
    if not from_email or not username or not password:
        error_msg = "Email credentials not found. Please set EMAIL_SENDER_EMAIL and EMAIL_SENDER_PASSWORD environment variables."
        logger.error(error_msg)
        return {
            "status": "error",
            "to_email": to_email,
            "subject": subject,
            "error": error_msg,
            "timestamp": str(datetime.datetime.now())
        }
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add plain text body
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)
        
        # Add HTML body if provided
        if html_body:
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
        
        # Add attachments if provided
        if attachments:
            for attachment_path in attachments:
                if os.path.exists(attachment_path):
                    with open(attachment_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                    
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {os.path.basename(attachment_path)}'
                    )
                    msg.attach(part)
                else:
                    logger.warning(f"Attachment file not found: {attachment_path}")
        
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
            "message": "Email sent successfully",
            "timestamp": str(datetime.datetime.now())
        }
        
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        
        return {
            "status": "error",
            "to_email": to_email,
            "subject": subject,
            "error": str(e),
            "timestamp": str(datetime.datetime.now())
        }


def send_bulk_emails(
    email_list: List[Dict[str, Any]],
    subject_template: str,
    body_template: str,
    from_email: Optional[str] = None,
    smtp_server: Optional[str] = None,
    smtp_port: int = 587,
    username: Optional[str] = None,
    password: Optional[str] = None,
    html_template: Optional[str] = None,
    dry_run: bool = True,
    delay_seconds: int = 1
) -> Dict[str, Any]:
    """
    Send bulk emails to a list of recipients.
    
    Args:
        email_list: List of dictionaries with recipient info (email, name, company, etc.)
        subject_template: Email subject template (use {name}, {company}, etc. for variables)
        body_template: Email body template (use {name}, {company}, etc. for variables)
        from_email: Sender email address
        smtp_server: SMTP server
        smtp_port: SMTP port
        username: SMTP username
        password: SMTP password
        html_template: HTML version of email body template (optional)
        dry_run: If True, only simulate sending (don't actually send)
        delay_seconds: Delay between emails to avoid rate limiting
    
    Returns:
        Dictionary with bulk email results
    """
    logger.info(f"Sending bulk emails to {len(email_list)} recipients (dry_run={dry_run})")
    
    results = {
        "total_emails": len(email_list),
        "sent_emails": 0,
        "failed_emails": 0,
        "email_results": [],
        "dry_run": dry_run
    }
    
    for i, recipient in enumerate(email_list):
        try:
            # Extract recipient info
            to_email = recipient.get("email")
            name = recipient.get("name", "")
            company = recipient.get("company", "")
            
            if not to_email:
                logger.warning(f"Missing email address for recipient {i}")
                results["failed_emails"] += 1
                continue
            
            # Personalize templates
            template_context = {
                "name": name,
                "company": company,
                "email": to_email,
                "position": recipient.get("position", ""),
                "location": recipient.get("location", ""),
                "domain": recipient.get("domain", ""),
                **{k: v for k, v in recipient.items() if k not in ["name", "company", "email", "position", "location", "domain"]}
            }
            
            try:
                subject = subject_template.format(**template_context)
            except KeyError as e:
                logger.warning(f"Missing template variable in subject: {e}")
                subject = subject_template
            
            try:
                body = body_template.format(**template_context)
            except KeyError as e:
                logger.warning(f"Missing template variable in body: {e}")
                body = body_template
            
            html_body = None
            if html_template:
                try:
                    html_body = html_template.format(**template_context)
                except KeyError as e:
                    logger.warning(f"Missing template variable in HTML body: {e}")
                    html_body = html_template
            
            if dry_run:
                logger.info(f"DRY RUN: Would send email to {to_email}")
                result = {
                    "status": "dry_run",
                    "to_email": to_email,
                    "subject": subject,
                    "message": "Email would be sent in production"
                }
                results["sent_emails"] += 1
            else:
                result = send_email(
                    to_email=to_email,
                    subject=subject,
                    body=body,
                    html_body=html_body,
                    from_email=from_email,
                    smtp_server=smtp_server,
                    smtp_port=smtp_port,
                    username=username,
                    password=password,
                    dry_run=False
                )
                
                if result["status"] == "success":
                    results["sent_emails"] += 1
                else:
                    results["failed_emails"] += 1
                
                # Add delay between emails to avoid rate limiting
                if i < len(email_list) - 1 and delay_seconds > 0:
                    time.sleep(delay_seconds)
            
            result["recipient_info"] = recipient
            results["email_results"].append(result)
            
        except Exception as e:
            logger.error(f"Error sending email to recipient {i}: {str(e)}")
            results["failed_emails"] += 1
            results["email_results"].append({
                "status": "error",
                "to_email": recipient.get("email", "unknown"),
                "error": str(e),
                "recipient_info": recipient
            })
    
    logger.info(f"Bulk email sending complete: {results['sent_emails']} sent, {results['failed_emails']} failed")
    return results


def send_follow_up_email(
    original_email_data: Dict[str, Any],
    follow_up_subject: str,
    follow_up_body: str,
    days_delay: int = 3,
    from_email: Optional[str] = None,
    smtp_server: Optional[str] = None,
    smtp_port: int = 587,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Send a follow-up email after a specified delay.
    
    Args:
        original_email_data: Data from the original email sent
        follow_up_subject: Subject for the follow-up email
        follow_up_body: Body for the follow-up email
        days_delay: Number of days to wait before sending follow-up
        from_email: Sender email address
        smtp_server: SMTP server
        smtp_port: SMTP port
        username: SMTP username
        password: SMTP password
    
    Returns:
        Dictionary with follow-up email results
    """
    logger.info(f"Scheduling follow-up email for {original_email_data.get('to_email', 'unknown')}")
    
    # For now, send immediately. In production, you'd use a task queue like Celery
    # to schedule the email for later delivery
    
    return send_email(
        to_email=original_email_data.get("to_email"),
        subject=follow_up_subject,
        body=follow_up_body,
        from_email=from_email,
        smtp_server=smtp_server,
        smtp_port=smtp_port,
        username=username,
        password=password
    )


def create_email_campaign(
    target_contacts: List[Dict[str, Any]],
    campaign_name: str,
    subject_line: str,
    email_body: str,
    html_body: Optional[str] = None,
    from_email: Optional[str] = None,
    smtp_server: Optional[str] = None,
    smtp_port: int = 587,
    username: Optional[str] = None,
    password: Optional[str] = None,
    schedule_time: Optional[str] = None,
    dry_run: bool = True
) -> Dict[str, Any]:
    """
    Create and execute an email campaign.
    
    Args:
        target_contacts: List of contacts to email
        campaign_name: Name of the campaign
        subject_line: Email subject line
        email_body: Email body text
        html_body: HTML version of email body (optional)
        from_email: Sender email address
        smtp_server: SMTP server
        smtp_port: SMTP port
        username: SMTP username
        password: SMTP password
        schedule_time: When to send the campaign (ISO format, optional)
        dry_run: If True, only simulate sending
    
    Returns:
        Dictionary with campaign results
    """
    logger.info(f"Creating email campaign '{campaign_name}' for {len(target_contacts)} contacts")
    
    campaign_results = {
        "campaign_name": campaign_name,
        "total_contacts": len(target_contacts),
        "subject_line": subject_line,
        "schedule_time": schedule_time,
        "dry_run": dry_run,
        "email_results": []
    }
    
    # Prepare email list
    email_list = []
    for contact in target_contacts:
        clean_contact = {
            "email": contact.get("email"),
            "name": contact.get("name", ""),
            "company": contact.get("company", ""),
            "position": contact.get("position", ""),
            "location": contact.get("location", ""),
            "domain": contact.get("domain", "")
        }
        # Add any additional fields that don't conflict
        for key, value in contact.items():
            if key not in clean_contact:
                clean_contact[key] = value
        email_list.append(clean_contact)
    
    # Send bulk emails
    bulk_results = send_bulk_emails(
        email_list=email_list,
        subject_template=subject_line,
        body_template=email_body,
        html_template=html_body,
        from_email=from_email,
        smtp_server=smtp_server,
        smtp_port=smtp_port,
        username=username,
        password=password,
        dry_run=dry_run
    )
    
    campaign_results.update(bulk_results)
    
    logger.info(f"Email campaign '{campaign_name}' completed")
    return campaign_results


def verify_email(email: str) -> Dict[str, Any]:
    """
    Verify if an email address is valid and deliverable.
    
    Args:
        email: Email address to verify
    
    Returns:
        Dictionary with verification results
    """
    import re
    
    # Basic email format validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return {
            "email": email,
            "is_valid": False,
            "confidence_score": 0,
            "error": "Invalid email format"
        }
    
    # Extract domain
    domain = email.split('@')[1]
    
    # Check for disposable email domains
    disposable_domains = [
        "10minutemail.com", "guerrillamail.com", "mailinator.com",
        "tempmail.org", "throwaway.email", "temp-mail.org"
    ]
    
    if domain.lower() in disposable_domains:
        return {
            "email": email,
            "is_valid": False,
            "confidence_score": 10,
            "error": "Disposable email domain detected"
        }
    
    # For now, return basic validation
    # In production, you'd integrate with email verification services
    return {
        "email": email,
        "is_valid": True,
        "confidence_score": 70,
        "message": "Email format is valid",
        "domain": domain
    }


def test_email_connection(
    smtp_server: Optional[str] = None,
    smtp_port: int = 587,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Test SMTP connection and credentials.
    
    Args:
        smtp_server: SMTP server to test
        smtp_port: SMTP port
        username: SMTP username
        password: SMTP password
    
    Returns:
        Dictionary with connection test results
    """
    if smtp_server is None:
        smtp_server = "smtp.gmail.com"
    
    if username is None:
        username = os.getenv("EMAIL_SENDER_EMAIL")
    
    if password is None:
        password = os.getenv("EMAIL_SENDER_PASSWORD")
    
    if not username or not password:
        return {
            "status": "error",
            "error": "Email credentials not found. Please set EMAIL_SENDER_EMAIL and EMAIL_SENDER_PASSWORD environment variables.",
            "setup_instructions": [
                "1. Set EMAIL_SENDER_EMAIL environment variable",
                "2. Set EMAIL_SENDER_PASSWORD environment variable",
                "3. For Gmail, use an App Password instead of your regular password",
                "4. Enable 2-factor authentication on your Gmail account"
            ]
        }
    
    try:
        # Test SMTP connection
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        
        # Test login
        server.login(username, password)
        server.quit()
        
        return {
            "status": "success",
            "message": f"Successfully connected to {smtp_server}:{smtp_port}",
            "username": username,
            "server": smtp_server,
            "port": smtp_port
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "server": smtp_server,
            "port": smtp_port,
            "username": username,
            "troubleshooting": [
                "Check if SMTP server and port are correct",
                "Verify username and password",
                "For Gmail, ensure you're using an App Password",
                "Check if 2-factor authentication is enabled"
            ]
        }


# Create FunctionTool instances
send_email_tool = FunctionTool(
    func=send_email
)

send_bulk_emails_tool = FunctionTool(
    func=send_bulk_emails
)

send_follow_up_email_tool = FunctionTool(
    func=send_follow_up_email
)

create_email_campaign_tool = FunctionTool(
    func=create_email_campaign
)

verify_email_tool = FunctionTool(
    func=verify_email
)

test_email_connection_tool = FunctionTool(
    func=test_email_connection
) 