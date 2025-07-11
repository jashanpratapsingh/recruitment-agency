#!/usr/bin/env python3
"""
Email Discovery Example

This script demonstrates the email discovery capabilities for finding:
1. Individual people's emails based on companies
2. Company admin/contact emails
3. Email verification and validation

Usage:
    python email_discovery_example.py
"""

import os
import sys
import logging
from typing import Dict, Any, List

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from recruiting_agency.sub_agents.email_discovery_agent.tools import (
    find_person_email,
    find_company_admin_emails,
    verify_email,
    bulk_email_finder,
    enrich_contact_data
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def demonstrate_individual_email_finding():
    """Demonstrate finding individual email addresses."""
    print("\n🔍 Individual Email Finding Demonstration")
    print("=" * 50)
    
    # Example 1: Find email for a person at a company
    print("\n1️⃣ Finding email for John Smith at Google")
    result = find_person_email(
        name="John Smith",
        company="Google",
        position="Software Engineer",
        location="Mountain View, CA"
    )
    
    print(f"   Name: {result['name']}")
    print(f"   Company: {result['company']}")
    print(f"   Domain: {result['domain']}")
    print(f"   Found {len(result['emails'])} potential emails:")
    
    for i, (email, confidence, source, verification) in enumerate(zip(
        result['emails'], 
        result['confidence_scores'], 
        result['sources'], 
        result['verification_status']
    )):
        print(f"   {i+1}. {email} (Confidence: {confidence}%, Source: {source}, Status: {verification})")
    
    # Example 2: Find email for a person at a startup
    print("\n2️⃣ Finding email for Sarah Johnson at Stripe")
    result2 = find_person_email(
        name="Sarah Johnson",
        company="Stripe",
        position="Product Manager"
    )
    
    print(f"   Name: {result2['name']}")
    print(f"   Company: {result2['company']}")
    print(f"   Domain: {result2['domain']}")
    print(f"   Found {len(result2['emails'])} potential emails:")
    
    for i, (email, confidence, source, verification) in enumerate(zip(
        result2['emails'], 
        result2['confidence_scores'], 
        result2['sources'], 
        result2['verification_status']
    )):
        print(f"   {i+1}. {email} (Confidence: {confidence}%, Source: {source}, Status: {verification})")


def demonstrate_company_admin_email_finding():
    """Demonstrate finding company admin emails."""
    print("\n🏢 Company Admin Email Finding Demonstration")
    print("=" * 50)
    
    # Example 1: Find admin emails for a tech company
    print("\n1️⃣ Finding admin emails for Microsoft")
    result = find_company_admin_emails(
        company="Microsoft",
        include_departments=True,
        include_general=True
    )
    
    print(f"   Company: {result['company']}")
    print(f"   Domain: {result['domain']}")
    print(f"   General emails ({len(result['general_emails'])}):")
    for email in result['general_emails'][:5]:  # Show first 5
        print(f"     • {email}")
    
    print(f"   Department emails ({len(result['department_emails'])}):")
    for email in result['department_emails'][:10]:  # Show first 10
        print(f"     • {email}")
    
    # Example 2: Find admin emails for a startup
    print("\n2️⃣ Finding admin emails for Airbnb")
    result2 = find_company_admin_emails(
        company="Airbnb",
        include_departments=True,
        include_general=True
    )
    
    print(f"   Company: {result2['company']}")
    print(f"   Domain: {result2['domain']}")
    print(f"   General emails ({len(result2['general_emails'])}):")
    for email in result2['general_emails'][:5]:
        print(f"     • {email}")
    
    print(f"   Department emails ({len(result2['department_emails'])}):")
    for email in result2['department_emails'][:10]:
        print(f"     • {email}")


def demonstrate_email_verification():
    """Demonstrate email verification capabilities."""
    print("\n✅ Email Verification Demonstration")
    print("=" * 50)
    
    # Example emails to verify
    test_emails = [
        "john.doe@google.com",
        "sarah.johnson@stripe.com",
        "contact@microsoft.com",
        "hr@airbnb.com",
        "invalid.email@nonexistent.com",
        "test@10minutemail.com"  # Disposable email
    ]
    
    print(f"   Testing {len(test_emails)} email addresses:")
    
    for email in test_emails:
        print(f"\n   📧 Verifying: {email}")
        result = verify_email(email)
        
        print(f"     Format valid: {result['is_valid_format']}")
        print(f"     Deliverable: {result['is_deliverable']}")
        print(f"     Confidence: {result['confidence_score']}%")
        print(f"     Methods: {', '.join(result['verification_methods'])}")
        
        if result['errors']:
            print(f"     Errors: {', '.join(result['errors'])}")


def demonstrate_bulk_email_finding():
    """Demonstrate bulk email finding capabilities."""
    print("\n📦 Bulk Email Finding Demonstration")
    print("=" * 50)
    
    # Sample contacts for bulk processing
    contacts = [
        {
            "name": "Alice Johnson",
            "company": "Google",
            "position": "Software Engineer",
            "location": "Mountain View, CA"
        },
        {
            "name": "Bob Smith",
            "company": "Microsoft",
            "position": "Product Manager",
            "location": "Seattle, WA"
        },
        {
            "name": "Carol Davis",
            "company": "Stripe",
            "position": "Designer",
            "location": "San Francisco, CA"
        },
        {
            "name": "David Wilson",
            "company": "Airbnb",
            "position": "Data Scientist",
            "location": "San Francisco, CA"
        }
    ]
    
    print(f"   Processing {len(contacts)} contacts in bulk...")
    result = bulk_email_finder(
        contacts=contacts,
        include_verification=True,
        max_requests=10
    )
    
    print(f"\n   📊 Bulk Processing Results:")
    print(f"     Total contacts: {result['total_contacts']}")
    print(f"     Processed: {result['processed_contacts']}")
    print(f"     Successful finds: {result['successful_finds']}")
    print(f"     Verified emails: {result['verified_emails']}")
    print(f"     Errors: {len(result['errors'])}")
    
    # Show detailed results for successful finds
    if result['contacts_with_emails']:
        print(f"\n   ✅ Successful Email Finds:")
        for contact_result in result['contacts_with_emails'][:3]:  # Show first 3
            contact = contact_result['contact']
            email_results = contact_result['email_results']
            print(f"     • {contact['name']} at {contact['company']}")
            for email in email_results['emails'][:2]:  # Show first 2 emails
                print(f"       - {email}")


def demonstrate_contact_enrichment():
    """Demonstrate contact data enrichment."""
    print("\n🔍 Contact Data Enrichment Demonstration")
    print("=" * 50)
    
    # Sample contact for enrichment
    contact = {
        "name": "Emily Chen",
        "company": "Netflix",
        "position": "Senior Product Manager",
        "location": "Los Gatos, CA",
        "email": "emily.chen@netflix.com"
    }
    
    print(f"   Enriching contact data for: {contact['name']}")
    result = enrich_contact_data(
        contact=contact,
        include_social_media=True,
        include_company_info=True
    )
    
    print(f"   Original contact: {result['original_contact']['name']} at {result['original_contact']['company']}")
    print(f"   Social media profiles found: {len(result['social_media'])}")
    print(f"   Company info fields: {len(result['company_info'])}")
    print(f"   Overall confidence: {sum(result['confidence_scores'].values())}%")


def show_api_configuration():
    """Show how to configure API keys for enhanced functionality."""
    print("\n🔧 API Configuration Guide")
    print("=" * 50)
    
    print("   To enable enhanced email finding capabilities, set these environment variables:")
    print()
    print("   # Hunter.io API (for email finding)")
    print("   export HUNTER_API_KEY='your-hunter-api-key'")
    print()
    print("   # Clearbit API (for contact enrichment)")
    print("   export CLEARBIT_API_KEY='your-clearbit-api-key'")
    print()
    print("   # Enable SMTP verification (optional)")
    print("   export ENABLE_SMTP_VERIFICATION='true'")
    print()
    print("   # Email sending configuration (for outreach)")
    print("   export BD_AGENT_EMAIL='your-email@gmail.com'")
    print("   export BD_AGENT_EMAIL_PASSWORD='your-app-password'")
    print()
    print("   📝 Note: Without API keys, the system will use pattern generation and basic verification.")


def main():
    """Main demonstration function."""
    print("🚀 Email Discovery System Demonstration")
    print("=" * 60)
    print("This demo shows how to find emails for both individuals and companies.")
    print("The system uses multiple methods: pattern generation, API lookups, and verification.")
    
    try:
        # Run demonstrations
        demonstrate_individual_email_finding()
        demonstrate_company_admin_email_finding()
        demonstrate_email_verification()
        demonstrate_bulk_email_finding()
        demonstrate_contact_enrichment()
        show_api_configuration()
        
        print("\n✅ All demonstrations completed successfully!")
        print("\n💡 Key Features Demonstrated:")
        print("   • Individual email finding with confidence scores")
        print("   • Company admin email discovery")
        print("   • Email verification and validation")
        print("   • Bulk processing capabilities")
        print("   • Contact data enrichment")
        print("   • Multiple data sources and methods")
        
    except Exception as e:
        logger.error(f"Error during demonstration: {str(e)}")
        print(f"\n❌ Error during demonstration: {str(e)}")
        print("   This might be due to missing dependencies or API keys.")
        print("   Check the configuration guide above for setup instructions.")


if __name__ == "__main__":
    main() 