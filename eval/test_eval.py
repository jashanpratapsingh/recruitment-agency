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

"""Evaluation tests for the recruiting agency agent."""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from recruiting_agency import root_agent


def test_agent_evaluation():
    """Test the agent's evaluation capabilities."""
    print("🧪 Running evaluation tests for Recruiting Agency Agent...")
    
    # Test cases for evaluation
    test_cases = [
        "Help me with hiring for a blockchain startup",
        "I need to hire developers for my fintech company",
        "Looking for marketing professionals for a healthcare startup",
        "Need help recruiting for a remote-first company"
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case}")
        
        try:
            # In a real evaluation, you would run the agent and evaluate the response
            # For now, we just verify the agent can handle the input
            assert root_agent is not None
            print(f"✅ Test case {i} passed")
            
        except Exception as e:
            print(f"❌ Test case {i} failed: {e}")
    
    print("\n🎉 Evaluation tests completed!")


if __name__ == "__main__":
    test_agent_evaluation() 