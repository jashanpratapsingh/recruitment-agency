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

"""Recruiting Agency Agent: Orchestrates specialized sub-agents for comprehensive hiring solutions."""

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .sub_agents.bd_agent import bd_agent
from .sub_agents.candidate_outreach_agent import candidate_outreach_agent
from .sub_agents.marketing_content_agent import marketing_content_agent
from .sub_agents.backend_matching_agent import backend_matching_agent

MODEL = "gemini-2.0-flash-live-001"

recruiting_coordinator = LlmAgent(
    name="recruiting_coordinator",
    model=MODEL,
    description=(
        "Orchestrates a comprehensive recruiting process by coordinating specialized "
        "sub-agents for business development, candidate outreach, marketing content, "
        "and backend matching to provide end-to-end hiring solutions."
    ),
    instruction=prompt.RECRUITING_COORDINATOR_PROMPT,
    output_key="recruiting_coordinator_output",
    tools=[
        AgentTool(agent=bd_agent),
        AgentTool(agent=candidate_outreach_agent),
        AgentTool(agent=marketing_content_agent),
        AgentTool(agent=backend_matching_agent),
    ],
)

root_agent = recruiting_coordinator 