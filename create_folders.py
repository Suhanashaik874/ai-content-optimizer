#!/usr/bin/env python3
"""
Quick fix: Create required folders
"""

import os
from pathlib import Path

# Create all required folders
folders = [
    "data",
    "results", 
    "logs",
    "credentials",
    "config",
    "data_collectors",

    "utils"
]

print("🔧 Creating folder structure...")
for folder in folders:
    Path(folder).mkdir(exist_ok=True)
    print(f"✅ Created: {folder}")

# Create empty __init__.py files
init_files = [
    "data_collectors/__init__.py",
    "milestone_2/__init__.py", 
    "utils/__init__.py"
]

for init_file in init_files:
    Path(init_file).touch()
    print(f"✅ Created: {init_file}")

print("\n🎉 Folder structure created successfully!")
print("\nNow run: python main.py")