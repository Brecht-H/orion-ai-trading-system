#!/usr/bin/env python3
"""
Clean up Orion project root directory
Moves documentation and test files to appropriate folders
"""

import os
import shutil
from pathlib import Path

def cleanup_root():
    """Move files to appropriate directories to clean up root"""
    
    print("🧹 Cleaning up Orion project root directory...")
    
    # Define file moves
    moves = {
        # Test files -> tests/
        'test_system.py': 'tests/test_system.py',
        'test_mcp_integration.py': 'tests/test_mcp_integration.py',
        
        # Documentation -> documentation/
        'START_HERE.md': 'documentation/START_HERE.md',
        'COPILOT_HANDOVER.md': 'documentation/COPILOT_HANDOVER.md',
        'COMPLETE_SYSTEM_GUIDE.md': 'documentation/COMPLETE_SYSTEM_GUIDE.md',
        'INTELLIGENT_SYSTEM_GUIDE.md': 'documentation/INTELLIGENT_SYSTEM_GUIDE.md',
        'COPILOT_CONTEXT.md': 'documentation/COPILOT_CONTEXT.md',
        
        # Temporary files -> archive
        'run_system_direct.py': 'Crypto_ai_tool/old_docs/run_system_direct.py',
        'cleanup_root.sh': 'Crypto_ai_tool/old_docs/cleanup_root.sh',
        
        # Rename requirements
        'requirements_background_agent.txt': 'requirements.txt'
    }
    
    # Perform moves
    for src, dst in moves.items():
        if os.path.exists(src):
            try:
                # Create destination directory if needed
                dst_dir = os.path.dirname(dst)
                if dst_dir:
                    os.makedirs(dst_dir, exist_ok=True)
                
                # Move or rename file
                if os.path.exists(dst):
                    print(f"⚠️  {dst} already exists, skipping {src}")
                else:
                    shutil.move(src, dst)
                    print(f"✅ Moved {src} -> {dst}")
            except Exception as e:
                print(f"❌ Error moving {src}: {e}")
        else:
            print(f"⏭️  {src} not found, skipping")
    
    print("\n✅ Cleanup complete!")
    print("\n🎯 Root directory now contains only essential files:")
    print("  - run_orion_system.py (main entry point)")
    print("  - quick_setup.sh (setup script)")
    print("  - requirements.txt (dependencies)")
    print("  - README.md (main documentation)")
    print("  - .gitignore (git configuration)")
    print("\n📁 All module directories remain intact")
    
    # List remaining files in root
    print("\n📋 Current root directory contents:")
    for item in sorted(os.listdir('.')):
        if not item.startswith('.') and item != '__pycache__':
            print(f"  - {item}")

if __name__ == "__main__":
    cleanup_root()