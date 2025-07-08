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

# Import the factory functions for flexible agent creation
from .agent_factory import (
    create_recruiting_coordinator,
    create_voice_agent,
    create_text_agent,
    create_auto_agent,
    root_agent
)

# For backward compatibility, also export the default agent
recruiting_coordinator = root_agent

# Export factory functions for dynamic agent creation
__all__ = [
    "create_recruiting_coordinator",
    "create_voice_agent", 
    "create_text_agent",
    "create_auto_agent",
    "recruiting_coordinator",
    "root_agent"
] 