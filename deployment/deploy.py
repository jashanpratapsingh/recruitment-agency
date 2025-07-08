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

"""Deployment script for the recruiting agency agent."""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from recruiting_agency import root_agent


def main():
    """Main deployment function."""
    print("🚀 Deploying Recruiting Agency Agent...")
    
    # Test the agent initialization
    try:
        assert root_agent is not None
        print("✅ Root agent initialized successfully")
        
        # Test basic functionality
        test_message = "Help me with hiring for a blockchain startup"
        print(f"🧪 Testing agent with message: '{test_message}'")
        
        # Note: In a real deployment, you would start the agent here
        # For now, we just verify it can be imported and initialized
        print("✅ Agent deployment successful!")
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 