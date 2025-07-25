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

"""Marketing Content Agent for creating compelling recruitment content."""

from google.adk import Agent

from . import prompt

marketing_content_agent = Agent(
    model="gemini-1.5-pro-latest",
    name="marketing_content_agent",
    instruction=prompt.MARKETING_CONTENT_AGENT_PROMPT,
    output_key="marketing_content_output",
    tools=[],
) 