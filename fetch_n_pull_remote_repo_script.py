# This will fetch and pull from GitHub repo and then push any local changes:

#!/usr/bin/env python3
"""
GitHub Fetch, Pull & Push Script - Fetches remote changes, pulls them, and pushes local changes
"""

import subprocess
import os

def run_command(command):
    """Execute a shell command and return the output"""
    process = subprocess.run(command, shell=True, text=True, capture_output=True)
    if process.returncode != 0:
        print(f"Error executing command: {command}")
        print(f"Error: {process.stderr}")
        return None
    return process.stdout.strip()

def get_changed_files():
    """Get list of changed files that are not yet committed"""
    # Get all modified, added, and untracked files
    status_output = run_command("git status --porcelain")
    if not status_output:
        return []
    
    changed_files = []
    for line in status_output.split('\n'):
        if line.strip():
            # Extract filename (status is in the first 2 characters)
            file_status = line[:2].strip()
            file_name = line[3:].strip()
            
            # Skip deleted files as we can't add them
            if file_status != 'D ' and file_status != 'DD':
                changed_files.append(file_name)
    
    return changed_files

def main():
    """Main function to fetch, pull and push changes"""
    print("🌐 Fetching latest changes from remote repository...")
    fetch_result = run_command("git fetch")
    
    print("⬇️ Pulling changes from remote repository...")
    pull_result = run_command("git pull")
    if pull_result is None:
        print("❌ Failed to pull changes. There might be conflicts.")
        return
    
    # Get changed files
    changed_files = get_changed_files()
    
    if not changed_files:
        print("✅ Repository is up to date. No local changes to push.")
        return
    
    print(f"🔄 Found {len(changed_files)} changed file(s):")
    for file in changed_files:
        print(f"  - {file}")
    
    # Generate commit message with file names
    file_names = ", ".join(changed_files)
    commit_message = f"Adding: {file_names}"
    
    # Add all changes
    print("➕ Adding changes...")
    run_command("git add .")
    
    # Commit changes
    print("💾 Committing changes...")
    commit_command = f'git commit -m "{commit_message}"'
    result = run_command(commit_command)
    
    if result is None:
        print("❌ Failed to commit changes.")
        return
    
    # Push to remote
    print("⬆️ Pushing to remote repository...")
    push_result = run_command("git push")
    
    if push_result is None:
        print("❌ Failed to push changes to remote.")
        return
    
    print("✅ Successfully pushed changes to GitHub!")
    print(f"📝 Commit message: \"{commit_message}\"")
    
    # Show current status
    print("\n📊 Current repository status:")
    status_result = run_command("git status")
    print(status_result)

if __name__ == "__main__":
    main()


