#!/usr/bin/env python3
"""
🗂️ ORION FILE ORGANIZATION SCRIPT
Moves loose documentation files from root to appropriate folders
"""

import os
import shutil
from pathlib import Path

def organize_root_files():
    """Organize loose files in root directory"""
    root_path = Path('.')
    
    # Create organization folders
    folders = {
        'documentation/guides': ['.md'],
        'config/environment': ['.env'],
        'logs/organization': ['.log'],
    }
    
    for folder in folders.keys():
        Path(folder).mkdir(parents=True, exist_ok=True)
    
    # Get loose files in root
    loose_files = []
    for file in root_path.iterdir():
        if file.is_file() and not file.name.startswith('.'):
            if file.suffix in ['.md', '.log', '.txt']:
                loose_files.append(file)
    
    print(f"📁 Found {len(loose_files)} loose files to organize")
    
    # Organize files
    moved_count = 0
    for file in loose_files:
        if file.suffix == '.md':
            target = Path('documentation/guides') / file.name
            if not target.exists():
                shutil.move(str(file), str(target))
                print(f"✅ Moved: {file.name} → documentation/guides/")
                moved_count += 1
    
    print(f"📊 Organized {moved_count} files")
    print("✅ Root directory cleaned up!")

if __name__ == "__main__":
    organize_root_files() 