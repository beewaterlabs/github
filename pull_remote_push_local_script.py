# This will fetch and pull from GitHub repo and then push any local changes:

import subprocess

# Execute all git commands in sequence
subprocess.run("git pull && git add email_slicer.py && git commit -a -m \"Adding email_slicer.py\" && git push && git status", shell=True)

print("Successfully fetched and pulled from a GitHub repo and then push any local changes")
