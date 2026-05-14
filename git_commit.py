#!/usr/bin/env python3
# git_commit.py - Automate git push for agent-harness feature

import os
from git import Repo

repo = Repo(".")

# Check if we're on a branch
print(f"📍 Current branch: {repo.active_branch.name}")

# Stage files
repo.git.add(".")
staged = repo.git.diff("--cached", "--name-only")
print(f"\n📦 Files to commit:\n{staged}")

# Commit
commit_msg = "feat: add agent harness with guardrails and trace logging"
repo.git.commit("-m", commit_msg)
print(f"\n✅ Committed: {commit_msg}")

# Check git status
status = repo.git.status()
print(f"\n📊 Status:\n{status}")

# Try push if on feature branch
if "feature/agent-harness" in repo.active_branch.name:
    try:
        origin = repo.remote("origin")
        origin.push(repo.active_branch.name)
        print(f"\n🚀 Pushed to origin/{repo.active_branch.name}")
        print("\n✨ สำเร็จ! ตอนนี้ไปสร้าง Pull Request บน GitHub")
    except Exception as e:
        print(f"\n⚠️ Push failed: {e}")
        print("(อาจต้องตั้งค่า GitHub credentials)")
else:
    print(f"\n⚠️ ไม่ได้อยู่บน feature/agent-harness branch")
