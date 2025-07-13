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

"""Email Discovery Agent for finding emails of people and companies."""

from google.adk import Agent
from . import prompt
from .tools import (
    find_person_email_tool,
    find_company_admin_emails_tool,
    verify_email_tool,
    bulk_email_finder_tool,
    enrich_contact_data_tool,
    send_email_tool,
    send_bulk_emails_tool,
    send_follow_up_email_tool,
    create_email_campaign_tool
)
from ...model_selector import get_model_for_interaction, TEXT_MODEL

# Default to text model for safety, can be overridden per interaction
MODEL = get_model_for_interaction("text")

email_discovery_agent = Agent(
    model=MODEL,
    name="email_discovery_agent",
    description=(
        "Specialized agent for finding and verifying email addresses of individuals "
        "and company admin contacts. Can also send emails directly using SMTP. "
        "Uses multiple data sources and verification methods."
    ),
    instruction=prompt.EMAIL_DISCOVERY_PROMPT,
    output_key="email_discovery_output",
    tools=[
        find_person_email_tool,
        find_company_admin_emails_tool,
        verify_email_tool,
        bulk_email_finder_tool,
        enrich_contact_data_tool,
        send_email_tool,
        send_bulk_emails_tool,
        send_follow_up_email_tool,
        create_email_campaign_tool
    ],
) 