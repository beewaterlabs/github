#!/usr/bin/env python3
"""
GitHub Auto Pull Script - Automatically pulls the latest changes from the remote repository
"""

import subprocess
import os
import time
import datetime

def run_command(command):
    """Execute a shell command and return the output"""
    process = subprocess.run(command, shell=True, text=True, capture_output=True)
    if process.returncode != 0:
        print(f"Error executing command: {command}")
        print(f"Error: {process.stderr}")
        return None
    return process.stdout.strip()

def get_current_branch():
    """Get the name of the current branch"""
    branch = run_command("git rev-parse --abbrev-ref HEAD")
    return branch

def check_for_changes():
    """Check if there are any local changes that would be overwritten by pull"""
    status = run_command("git status --porcelain")
    return bool(status.strip())

def main():
    """Main function to automatically pull from GitHub"""
    # Get the current directory name for display purposes
    repo_dir = os.path.basename(os.getcwd())
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"🕒 {current_time}")
    print(f"📂 Repository: {repo_dir}")
    
    # Get current branch
    branch = get_current_branch()
    if not branch:
        print("❌ Failed to determine current branch. Is this a git repository?")
        return
    
    print(f"🔀 Current branch: {branch}")
    
    # Check for local changes
    if check_for_changes():
        print("⚠️ You have local changes that might conflict with pulled changes.")
        choice = input("Do you want to stash these changes before pulling? (y/n): ")
        if choice.lower() == 'y':
            print("📦 Stashing local changes...")
            stash_result = run_command("git stash")
            if stash_result is None:
                print("❌ Failed to stash changes.")
                return
            print("✅ Changes stashed successfully.")
    
    # Fetch latest changes
    print("🌐 Fetching updates from remote...")
    fetch_result = run_command("git fetch")
    if fetch_result is None:
        print("❌ Failed to fetch from remote.")
        return
    
    # Check if we're behind remote
    behind_check = run_command(f"git rev-list --count HEAD..origin/{branch}")
    if behind_check and int(behind_check) > 0:
        print(f"ℹ️ Your branch is behind by {behind_check} commit(s).")
        
        # Pull the latest changes
        print("⬇️ Pulling latest changes...")
        pull_result = run_command("git pull")
        if pull_result is None:
            print("❌ Failed to pull changes. There might be conflicts.")
            return
        
        print("✅ Successfully pulled the latest changes.")
    else:
        print("✅ Already up-to-date. No changes to pull.")
    
    # Show git status
    print("\n📊 Current repository status:")
    status_result = run_command("git status")
    print(status_result)

if __name__ == "__main__":
    main()
  
