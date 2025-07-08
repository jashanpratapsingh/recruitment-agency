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

"""Tests for the recruiting agency agent."""

import pytest
from recruiting_agency import root_agent


def test_root_agent_initialization():
    """Test that the root agent is properly initialized."""
    assert root_agent is not None
    assert hasattr(root_agent, 'chat')


def test_root_agent_name():
    """Test that the root agent has the correct name."""
    assert root_agent.name == "recruiting_coordinator"


def test_root_agent_tools():
    """Test that the root agent has the expected tools."""
    assert len(root_agent.tools) == 4
    tool_names = [tool.agent.name for tool in root_agent.tools]
    expected_names = [
        "bd_agent",
        "candidate_outreach_agent", 
        "marketing_content_agent",
        "backend_matching_agent"
    ]
    assert all(name in tool_names for name in expected_names)


if __name__ == "__main__":
    pytest.main([__file__]) 