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

"""Email discovery tools for finding emails of people and companies."""

import logging
import os
import re
import requests
import json
import dns.resolver
import smtplib
from typing import List, Dict, Any, Optional, Tuple
from urllib.parse import urlparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from google.adk.tools import FunctionTool
import datetime

logger = logging.getLogger(__name__)


def find_person_email(
    name: str,
    company: str,
    domain: Optional[str] = None,
    position: Optional[str] = None,
    location: Optional[str] = None
) -> Dict[str, Any]:
    """
    Find email address for a specific person at a company.
    
    Args:
        name: Full name of the person
        company: Company name
        domain: Company domain (optional, will be auto-detected)
        position: Job position/title (optional)
        location: Location (optional)
    
    Returns:
        Dictionary with email discovery results
    """
    # Input validation
    if not name or not name.strip():
        logger.error("Name is required and cannot be empty")
        return {
            "name": name,
            "company": company,
            "domain": domain,
            "position": position,
            "location": location,
            "emails": [],
            "confidence_scores": [],
            "sources": [],
            "verification_status": [],
            "error": "Name is required and cannot be empty"
        }
    
    if not company or not company.strip():
        logger.error("Company is required and cannot be empty")
        return {
            "name": name,
            "company": company,
            "domain": domain,
            "position": position,
            "location": location,
            "emails": [],
            "confidence_scores": [],
            "sources": [],
            "verification_status": [],
            "error": "Company is required and cannot be empty"
        }
    
    # Clean and normalize inputs
    name = name.strip()
    company = company.strip()
    
    logger.info(f"Searching for email: {name} at {company}")
    
    # Auto-detect domain if not provided
    if not domain:
        domain = _extract_domain_from_company(company)
    
    results = {
        "name": name,
        "company": company,
        "domain": domain,
        "position": position,
        "location": location,
        "emails": [],
        "confidence_scores": [],
        "sources": [],
        "verification_status": []
    }
    
    # Method 1: Common email patterns
    pattern_emails = _generate_email_patterns(name, domain)
    for email, pattern in pattern_emails:
        confidence = _calculate_pattern_confidence(pattern, name, company)
        results["emails"].append(email)
        results["confidence_scores"].append(confidence)
        results["sources"].append("pattern_generation")
        results["verification_status"].append("unverified")
    
    # Method 2: Hunter.io API (if available)
    hunter_results = _search_hunter_api(name, domain, company)
    if hunter_results:
        results["emails"].extend(hunter_results["emails"])
        results["confidence_scores"].extend(hunter_results["confidence_scores"])
        results["sources"].extend(hunter_results["sources"])
        results["verification_status"].extend(hunter_results["verification_status"])
    
    # Method 3: Clearbit API (if available)
    clearbit_results = _search_clearbit_api(name, domain, company)
    if clearbit_results:
        results["emails"].extend(clearbit_results["emails"])
        results["confidence_scores"].extend(clearbit_results["confidence_scores"])
        results["sources"].extend(clearbit_results["sources"])
        results["verification_status"].extend(clearbit_results["verification_status"])
    
    # Method 4: Web scraping (basic)
    web_results = _search_web_sources(name, company, domain)
    if web_results:
        results["emails"].extend(web_results["emails"])
        results["confidence_scores"].extend(web_results["confidence_scores"])
        results["sources"].extend(web_results["sources"])
        results["verification_status"].extend(web_results["verification_status"])
    
    # Remove duplicates and sort by confidence
    unique_results = _deduplicate_and_sort_results(results)
    
    logger.info(f"Found {len(unique_results['emails'])} potential emails for {name}")
    return unique_results


def find_company_admin_emails(
    company: str,
    domain: Optional[str] = None,
    include_departments: bool = True,
    include_general: bool = True
) -> Dict[str, Any]:
    """
    Find admin and contact emails for a company.
    
    Args:
        company: Company name
        domain: Company domain (optional, will be auto-detected)
        include_departments: Include department-specific emails
        include_general: Include general contact emails
    
    Returns:
        Dictionary with company admin email results
    """
    logger.info(f"Searching for admin emails: {company}")
    
    # Auto-detect domain if not provided
    if not domain:
        domain = _extract_domain_from_company(company)
    
    results = {
        "company": company,
        "domain": domain,
        "admin_emails": [],
        "department_emails": [],
        "general_emails": [],
        "confidence_scores": [],
        "sources": [],
        "verification_status": []
    }
    
    # Generate common admin email patterns
    admin_patterns = [
        "admin@",
        "contact@",
        "info@",
        "hello@",
        "support@",
        "help@",
        "team@",
        "office@",
        "main@"
    ]
    
    department_patterns = [
        "hr@",
        "human.resources@",
        "recruiting@",
        "talent@",
        "careers@",
        "jobs@",
        "sales@",
        "marketing@",
        "business@",
        "partnerships@",
        "legal@",
        "finance@",
        "accounting@",
        "billing@",
        "support@",
        "help@",
        "customer.service@",
        "press@",
        "media@",
        "pr@",
        "communications@"
    ]
    
    # Generate admin emails
    if include_general:
        for pattern in admin_patterns:
            email = pattern + domain
            results["general_emails"].append(email)
            results["confidence_scores"].append(70)  # High confidence for common patterns
            results["sources"].append("pattern_generation")
            results["verification_status"].append("unverified")
    
    # Generate department emails
    if include_departments:
        for pattern in department_patterns:
            email = pattern + domain
            results["department_emails"].append(email)
            results["confidence_scores"].append(60)  # Medium confidence for department patterns
            results["sources"].append("pattern_generation")
            results["verification_status"].append("unverified")
    
    # Method 2: Web scraping for contact pages
    web_results = _scrape_company_contact_page(company, domain)
    if web_results:
        results["general_emails"].extend(web_results["general_emails"])
        results["department_emails"].extend(web_results["department_emails"])
        results["confidence_scores"].extend(web_results["confidence_scores"])
        results["sources"].extend(web_results["sources"])
        results["verification_status"].extend(web_results["verification_status"])
    
    # Method 3: LinkedIn company page scraping
    linkedin_results = _scrape_linkedin_company_page(company)
    if linkedin_results:
        results["general_emails"].extend(linkedin_results["general_emails"])
        results["department_emails"].extend(linkedin_results["department_emails"])
        results["confidence_scores"].extend(linkedin_results["confidence_scores"])
        results["sources"].extend(linkedin_results["sources"])
        results["verification_status"].extend(linkedin_results["verification_status"])
    
    # Combine all emails
    all_emails = results["general_emails"] + results["department_emails"]
    results["admin_emails"] = list(set(all_emails))  # Remove duplicates
    
    logger.info(f"Found {len(results['admin_emails'])} admin emails for {company}")
    return results


def verify_email(email: str) -> Dict[str, Any]:
    """
    Verify if an email address is valid and deliverable.
    
    Args:
        email: Email address to verify
    
    Returns:
        Dictionary with verification results
    """
    logger.info(f"Verifying email: {email}")
    
    results = {
        "email": email,
        "is_valid_format": False,
        "is_deliverable": False,
        "confidence_score": 0,
        "verification_methods": [],
        "errors": []
    }
    
    # Method 1: Format validation
    if _validate_email_format(email):
        results["is_valid_format"] = True
        results["confidence_score"] += 20
        results["verification_methods"].append("format_validation")
    else:
        results["errors"].append("Invalid email format")
        return results
    
    # Method 2: Domain validation
    domain = email.split("@")[1]
    if _validate_domain(domain):
        results["confidence_score"] += 30
        results["verification_methods"].append("domain_validation")
    else:
        results["errors"].append("Invalid domain")
        return results
    
    # Method 3: SMTP validation (if enabled)
    smtp_enabled = os.getenv("ENABLE_SMTP_VERIFICATION", "false").lower() == "true"
    if smtp_enabled:
        smtp_result = _verify_smtp(email, domain)
        if smtp_result["is_deliverable"]:
            results["is_deliverable"] = True
            results["confidence_score"] += 50
            results["verification_methods"].append("smtp_verification")
        else:
            results["errors"].append(smtp_result.get("error", "SMTP verification failed"))
    
    # Method 4: Disposable email check
    if _is_disposable_email(domain):
        results["confidence_score"] -= 30
        results["verification_methods"].append("disposable_email_check")
        results["errors"].append("Disposable email domain detected")
    
    # Cap confidence score at 100
    results["confidence_score"] = min(100, max(0, results["confidence_score"]))
    
    logger.info(f"Email verification complete: {email} - Score: {results['confidence_score']}")
    return results


def bulk_email_finder(
    contacts: List[Dict[str, Any]],
    include_verification: bool = True,
    max_requests: int = 50
) -> Dict[str, Any]:
    """
    Find emails for multiple contacts in bulk.
    
    Args:
        contacts: List of contact dictionaries with name, company, etc.
        include_verification: Whether to verify found emails
        max_requests: Maximum number of API requests to make
    
    Returns:
        Dictionary with bulk email finding results
    """
    logger.info(f"Starting bulk email finder for {len(contacts)} contacts")
    
    results = {
        "total_contacts": len(contacts),
        "processed_contacts": 0,
        "successful_finds": 0,
        "verified_emails": 0,
        "contacts_with_emails": [],
        "contacts_without_emails": [],
        "errors": []
    }
    
    for i, contact in enumerate(contacts[:max_requests]):
        try:
            # Find email for this contact
            email_result = find_person_email(
                name=contact.get("name", ""),
                company=contact.get("company", ""),
                domain=contact.get("domain"),
                position=contact.get("position"),
                location=contact.get("location")
            )
            
            # Add verification if requested
            if include_verification and email_result["emails"]:
                email_result["verification_results"] = []
                for email in email_result["emails"]:
                    verify_result = verify_email(email)
                    email_result["verification_results"].append(verify_result)
            
            results["processed_contacts"] += 1
            
            if email_result["emails"]:
                results["successful_finds"] += 1
                results["contacts_with_emails"].append({
                    "contact": contact,
                    "email_results": email_result
                })
            else:
                results["contacts_without_emails"].append({
                    "contact": contact,
                    "email_results": email_result
                })
                
        except Exception as e:
            logger.error(f"Error processing contact {i}: {str(e)}")
            results["errors"].append({
                "contact_index": i,
                "contact": contact,
                "error": str(e)
            })
    
    # Calculate verification stats
    if include_verification:
        for contact_result in results["contacts_with_emails"]:
            email_results = contact_result["email_results"]
            if "verification_results" in email_results:
                for verify_result in email_results["verification_results"]:
                    if verify_result.get("is_deliverable", False):
                        results["verified_emails"] += 1
    
    logger.info(f"Bulk email finder complete: {results['successful_finds']}/{results['processed_contacts']} successful")
    return results


def enrich_contact_data(
    contact: Dict[str, Any],
    include_social_media: bool = True,
    include_company_info: bool = True
) -> Dict[str, Any]:
    """
    Enrich contact data with additional information.
    
    Args:
        contact: Contact dictionary with basic info
        include_social_media: Include social media profiles
        include_company_info: Include company information
    
    Returns:
        Enriched contact data
    """
    logger.info(f"Enriching contact data for: {contact.get('name', 'Unknown')}")
    
    enriched_data = {
        "original_contact": contact,
        "enriched_data": {},
        "social_media": {},
        "company_info": {},
        "confidence_scores": {}
    }
    
    name = contact.get("name", "")
    company = contact.get("company", "")
    
    # Enrich with social media profiles
    if include_social_media:
        social_results = _find_social_media_profiles(name, company)
        enriched_data["social_media"] = social_results
    
    # Enrich with company information
    if include_company_info:
        company_results = _get_company_information(company)
        enriched_data["company_info"] = company_results
    
    # Add confidence scores
    enriched_data["confidence_scores"] = {
        "social_media": len(enriched_data["social_media"]) * 10,
        "company_info": len(enriched_data["company_info"]) * 10
    }
    
    logger.info(f"Contact enrichment complete for {name}")
    return enriched_data


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
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Send an email using SMTP.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Plain text email body
        from_email: Sender email address (uses BD_AGENT_EMAIL if not provided)
        smtp_server: SMTP server (defaults to Gmail)
        smtp_port: SMTP port (defaults to 587)
        username: SMTP username (uses BD_AGENT_EMAIL if not provided)
        password: SMTP password (uses BD_AGENT_EMAIL_PASSWORD if not provided)
        html_body: HTML version of email body (optional)
        attachments: List of file paths to attach (optional)
    
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
    
    # Handle dry run
    if dry_run:
        logger.info(f"DRY RUN: Would send email to {to_email}")
        return {
            "status": "dry_run",
            "to_email": to_email,
            "subject": subject,
            "message": "Email would be sent in production"
        }
    
    # Validate required environment variables
    if not from_email or not username or not password:
        error_msg = "Email credentials not found. Please set BD_AGENT_EMAIL and BD_AGENT_EMAIL_PASSWORD environment variables."
        logger.error(error_msg)
        return {
            "status": "error",
            "to_email": to_email,
            "subject": subject,
            "error": error_msg
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
    dry_run: bool = False,
    delay_seconds: int = 1
) -> Dict[str, Any]:
    """
    Send bulk emails to a list of recipients.
    
    Args:
        email_list: List of dictionaries with recipient info (email, name, company, etc.)
            subject_template: Email subject template (use {{name}}, {{company}}, etc. for variables)
    body_template: Email body template (use {{name}}, {{company}}, etc. for variables)
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
            # Create a safe template context with only the needed variables
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
                    password=password
                )
                
                if result["status"] == "success":
                    results["sent_emails"] += 1
                else:
                    results["failed_emails"] += 1
                
                # Add delay between emails to avoid rate limiting
                if i < len(email_list) - 1 and delay_seconds > 0:
                    import time
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
        # Create a clean contact dictionary to avoid template conflicts
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


# Helper functions

def _extract_domain_from_company(company: str) -> str:
    """Extract domain from company name or return a common pattern."""
    # Common domain patterns
    common_domains = {
        "google": "google.com",
        "microsoft": "microsoft.com",
        "apple": "apple.com",
        "amazon": "amazon.com",
        "facebook": "facebook.com",
        "meta": "meta.com",
        "netflix": "netflix.com",
        "tesla": "tesla.com",
        "spacex": "spacex.com",
        "uber": "uber.com",
        "lyft": "lyft.com",
        "airbnb": "airbnb.com",
        "stripe": "stripe.com",
        "square": "square.com",
        "salesforce": "salesforce.com",
        "oracle": "oracle.com",
        "ibm": "ibm.com",
        "intel": "intel.com",
        "amd": "amd.com",
        "nvidia": "nvidia.com"
    }
    
    company_lower = company.lower().replace(" ", "")
    
    # Check if we have a known domain
    for key, domain in common_domains.items():
        if key in company_lower:
            return domain
    
    # Generate a domain based on company name
    clean_company = re.sub(r'[^a-zA-Z0-9]', '', company.lower())
    return f"{clean_company}.com"


def _generate_email_patterns(name: str, domain: str) -> List[Tuple[str, str]]:
    """Generate common email patterns for a name and domain."""
    patterns = []
    
    # Split name into parts and validate
    name_parts = name.lower().split()
    first_name = name_parts[0] if name_parts else ""
    last_name = name_parts[-1] if len(name_parts) > 1 else ""
    
    # Validate that we have valid names
    if not first_name:
        logger.warning(f"Invalid name provided: '{name}'")
        return patterns
    
    # Common email patterns (only include patterns that are valid)
    email_patterns = []
    
    # Basic patterns that always work
    email_patterns.append(f"{first_name}@{domain}")
    
    # Patterns that require both first and last name
    if last_name:
        email_patterns.extend([
            f"{first_name}.{last_name}@{domain}",
            f"{first_name}{last_name}@{domain}",
            f"{last_name}.{first_name}@{domain}",
            f"{last_name}{first_name}@{domain}",
            f"{first_name}_{last_name}@{domain}",
            f"{first_name}-{last_name}@{domain}",
        ])
        
        # Patterns that require first letter of last name
        if len(last_name) > 0:
            email_patterns.extend([
                f"{first_name}{last_name[0]}@{domain}",
                f"{first_name}.{last_name[0]}@{domain}"
            ])
    
    # Patterns that require first letter of first name
    if len(first_name) > 0:
        email_patterns.extend([
            f"{first_name[0]}{last_name}@{domain}",
            f"{first_name[0]}.{last_name}@{domain}"
        ])
    
    # Add patterns to results
    for pattern in email_patterns:
        patterns.append((pattern, "generated"))
    
    return patterns


def _calculate_pattern_confidence(pattern: str, name: str, company: str) -> int:
    """Calculate confidence score for an email pattern."""
    confidence = 50  # Base confidence
    
    # Higher confidence for common patterns
    if "firstname.lastname" in pattern or "firstname.lastname" in pattern:
        confidence += 20
    elif "firstname.lastname" in pattern:
        confidence += 15
    elif "firstname" in pattern and "lastname" in pattern:
        confidence += 10
    
    # Lower confidence for single name patterns
    if pattern.count("@") == 1 and len(pattern.split("@")[0]) < 3:
        confidence -= 20
    
    return min(100, max(0, confidence))


def _search_hunter_api(name: str, domain: str, company: str) -> Optional[Dict[str, Any]]:
    """Search for emails using Hunter.io API."""
    api_key = os.getenv("HUNTER_API_KEY")
    if not api_key:
        return None
    
    try:
        url = "https://api.hunter.io/v2/email-finder"
        params = {
            "api_key": api_key,
            "domain": domain,
            "first_name": name.split()[0],
            "last_name": name.split()[-1] if len(name.split()) > 1 else ""
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get("data", {}).get("email"):
            return {
                "emails": [data["data"]["email"]],
                "confidence_scores": [data["data"].get("score", 50)],
                "sources": ["hunter_api"],
                "verification_status": ["verified" if data["data"].get("verified") else "unverified"]
            }
    
    except Exception as e:
        logger.error(f"Hunter API error: {str(e)}")
    
    return None


def _search_clearbit_api(name: str, domain: str, company: str) -> Optional[Dict[str, Any]]:
    """Search for emails using Clearbit API."""
    api_key = os.getenv("CLEARBIT_API_KEY")
    if not api_key:
        return None
    
    try:
        url = "https://person.clearbit.com/v2/combined/find"
        params = {
            "domain": domain,
            "name": name
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get("email"):
            return {
                "emails": [data["email"]],
                "confidence_scores": [80],  # High confidence for Clearbit
                "sources": ["clearbit_api"],
                "verification_status": ["verified"]
            }
    
    except Exception as e:
        logger.error(f"Clearbit API error: {str(e)}")
    
    return None


def _search_web_sources(name: str, company: str, domain: str) -> Optional[Dict[str, Any]]:
    """Search web sources for email addresses."""
    # This is a simplified version - in production, you'd use more sophisticated web scraping
    return None


def _scrape_company_contact_page(company: str, domain: str) -> Optional[Dict[str, Any]]:
    """Scrape company contact page for email addresses."""
    # This is a simplified version - in production, you'd use more sophisticated web scraping
    return None


def _scrape_linkedin_company_page(company: str) -> Optional[Dict[str, Any]]:
    """Scrape LinkedIn company page for contact information."""
    # This is a simplified version - in production, you'd use more sophisticated web scraping
    return None


def _validate_email_format(email: str) -> bool:
    """Validate email format using regex."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def _validate_domain(domain: str) -> bool:
    """Validate domain by checking DNS records."""
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except:
        try:
            dns.resolver.resolve(domain, 'A')
            return True
        except:
            return False


def _verify_smtp(email: str, domain: str) -> Dict[str, Any]:
    """Verify email using SMTP."""
    try:
        # Get MX records
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_host = str(mx_records[0].exchange)
        
        # Connect to SMTP server
        server = smtplib.SMTP(mx_host, timeout=10)
        server.starttls()
        
        # Try to send a test email (but don't actually send)
        server.verify(email)
        server.quit()
        
        return {"is_deliverable": True}
    
    except Exception as e:
        return {"is_deliverable": False, "error": str(e)}


def _is_disposable_email(domain: str) -> bool:
    """Check if domain is a disposable email provider."""
    disposable_domains = {
        "10minutemail.com", "guerrillamail.com", "mailinator.com",
        "tempmail.org", "throwaway.email", "temp-mail.org"
    }
    return domain.lower() in disposable_domains


def _deduplicate_and_sort_results(results: Dict[str, Any]) -> Dict[str, Any]:
    """Remove duplicate emails and sort by confidence."""
    # Create a list of (email, confidence, source, verification) tuples
    email_data = list(zip(
        results["emails"],
        results["confidence_scores"],
        results["sources"],
        results["verification_status"]
    ))
    
    # Remove duplicates while keeping highest confidence
    seen_emails = set()
    unique_data = []
    
    for email, confidence, source, verification in email_data:
        if email not in seen_emails:
            seen_emails.add(email)
            unique_data.append((email, confidence, source, verification))
    
    # Sort by confidence (highest first)
    unique_data.sort(key=lambda x: x[1], reverse=True)
    
    # Reconstruct results
    return {
        "name": results["name"],
        "company": results["company"],
        "domain": results["domain"],
        "position": results["position"],
        "location": results["location"],
        "emails": [item[0] for item in unique_data],
        "confidence_scores": [item[1] for item in unique_data],
        "sources": [item[2] for item in unique_data],
        "verification_status": [item[3] for item in unique_data]
    }


def _find_social_media_profiles(name: str, company: str) -> Dict[str, Any]:
    """Find social media profiles for a person."""
    # This is a placeholder - in production, you'd integrate with social media APIs
    return {}


def _get_company_information(company: str) -> Dict[str, Any]:
    """Get additional company information."""
    # This is a placeholder - in production, you'd integrate with company data APIs
    return {}


# Create FunctionTool instances

find_person_email_tool = FunctionTool(
    func=find_person_email
)

find_company_admin_emails_tool = FunctionTool(
    func=find_company_admin_emails
)

verify_email_tool = FunctionTool(
    func=verify_email
)

bulk_email_finder_tool = FunctionTool(
    func=bulk_email_finder
)

enrich_contact_data_tool = FunctionTool(
    func=enrich_contact_data
)

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