import os
import subprocess

port = os.environ.get("PORT", "10000")
subprocess.run(["poetry", "run", "adk", "web", "--host", "0.0.0.0", "--port", port]) 