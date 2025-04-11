# This will fetch and pull from GitHub repo and then push any local changes:

import subprocess

# Execute all git commands in sequence
subprocess.run("git fetch && git pull && git status", shell=True)
