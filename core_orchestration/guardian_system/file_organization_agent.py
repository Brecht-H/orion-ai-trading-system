#!/usr/bin/env python3
"""
🛡️ FILE ORGANIZATION AGENT
Automated file organization for the Orion Project Guardian System

This agent automatically organizes loose files in the root directory
according to the established project structure and best practices.
"""

import os
import shutil
import sqlite3
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import json

class FileOrganizationAgent:
    """
    Guardian System File Organization Agent
    
    RESPONSIBILITIES:
    - Monitor root directory for loose files
    - Automatically organize files into proper directories
    - Maintain file movement audit trail
    - Prevent accidental deletion of important files
    - Generate organization reports for Guardian system
    """
    
    def __init__(self):
        self.agent_id = "file_organization_guardian_001"
        self.project_root = Path.cwd()
        self.db_path = self.project_root / "core_orchestration" / "guardian_system" / "databases" / "file_organization.db"
        self.setup_database()
        self.setup_logging()
        
        # File organization rules
        self.organization_rules = {
            # Documentation files
            '.md': 'documentation',
            '.txt': 'documentation', 
            '.pdf': 'documentation',
            '.docx': 'documentation',
            
            # Configuration files
            '.json': 'config',
            '.yaml': 'config',
            '.yml': 'config',
            '.toml': 'config',
            '.ini': 'config',
            '.env': 'config',
            
            # Data files
            '.csv': 'data',
            '.db': 'databases/sqlite_dbs',
            '.sqlite': 'databases/sqlite_dbs',
            '.sqlite3': 'databases/sqlite_dbs',
            
            # Log files
            '.log': 'logs/system_logs',
            
            # Python files (special handling)
            '.py': self._determine_python_location,
            
            # Backup files
            '.backup': 'backups',
            '.bak': 'backups',
            
            # Archive files
            '.zip': 'backups',
            '.tar': 'backups',
            '.gz': 'backups'
        }
        
        # Protected files that should never be moved
        self.protected_files = {
            '.env',
            '.gitignore', 
            'README.md',
            'requirements.txt',
            'setup.py',
            'pyproject.toml',
            'Pipfile',
            'Pipfile.lock',
            'poetry.lock',
            'package.json',
            'package-lock.json'
        }
        
        # Important files that require CEO approval before moving
        self.sensitive_files = {
            'ORION_PROJECT_MASTER.md',
            'EXECUTIVE_SUMMARY.md',
            'DEPLOYMENT_SUCCESS_SUMMARY.md',
            'SYSTEM_STATUS_FINAL.md'
        }
        
    def setup_database(self):
        """Setup file organization tracking database"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # File movements tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS file_movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                filename TEXT NOT NULL,
                original_path TEXT NOT NULL,
                new_path TEXT NOT NULL,
                file_type TEXT NOT NULL,
                size_bytes INTEGER NOT NULL,
                action_type TEXT NOT NULL,
                success BOOLEAN NOT NULL,
                error_message TEXT
            )
        """)
        
        # Organization rules tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS organization_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_extension TEXT NOT NULL,
                target_directory TEXT NOT NULL,
                rule_type TEXT NOT NULL,
                created_at REAL NOT NULL,
                last_used REAL
            )
        """)
        
        # File scan results
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scan_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                files_found INTEGER NOT NULL,
                files_organized INTEGER NOT NULL,
                files_protected INTEGER NOT NULL,
                files_requiring_approval INTEGER NOT NULL,
                scan_duration REAL NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
        
    def setup_logging(self):
        """Setup file organization logging"""
        log_dir = self.project_root / "logs" / "guardian_system"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - FileOrganizer - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'file_organization.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"🛡️ File Organization Agent {self.agent_id} initialized")
        
    async def run_organization_cycle(self) -> Dict[str, any]:
        """Run complete file organization cycle"""
        self.logger.info("🧹 Starting file organization cycle...")
        
        start_time = datetime.now()
        results = {
            'files_found': 0,
            'files_organized': 0,
            'files_protected': 0,
            'files_requiring_approval': 0,
            'movements': [],
            'errors': []
        }
        
        try:
            # Scan root directory for loose files
            loose_files = self._scan_root_directory()
            results['files_found'] = len(loose_files)
            
            self.logger.info(f"📁 Found {len(loose_files)} files to analyze")
            
            # Process each file
            for file_path in loose_files:
                try:
                    movement_result = await self._process_file(file_path)
                    
                    if movement_result['action'] == 'organized':
                        results['files_organized'] += 1
                        results['movements'].append(movement_result)
                    elif movement_result['action'] == 'protected':
                        results['files_protected'] += 1
                    elif movement_result['action'] == 'requires_approval':
                        results['files_requiring_approval'] += 1
                        
                except Exception as e:
                    error_msg = f"Error processing {file_path}: {str(e)}"
                    self.logger.error(error_msg)
                    results['errors'].append(error_msg)
            
            # Record scan results
            duration = (datetime.now() - start_time).total_seconds()
            self._record_scan_results(results, duration)
            
            self.logger.info(f"✅ Organization cycle completed: {results['files_organized']} files organized")
            
        except Exception as e:
            self.logger.error(f"❌ Organization cycle failed: {str(e)}")
            results['errors'].append(f"Cycle error: {str(e)}")
            
        return results
        
    def _scan_root_directory(self) -> List[Path]:
        """Scan root directory for files that need organization"""
        loose_files = []
        
        for item in self.project_root.iterdir():
            if item.is_file() and not item.name.startswith('.'):
                # Skip protected files
                if item.name not in self.protected_files:
                    loose_files.append(item)
                    
        return loose_files
        
    async def _process_file(self, file_path: Path) -> Dict[str, any]:
        """Process individual file for organization"""
        
        # Check if file is sensitive and requires approval
        if file_path.name in self.sensitive_files:
            self.logger.info(f"🔒 Sensitive file {file_path.name} requires CEO approval")
            return {
                'action': 'requires_approval',
                'filename': file_path.name,
                'reason': 'Sensitive file requiring CEO approval'
            }
            
        # Determine target directory
        target_dir = self._determine_target_directory(file_path)
        
        if target_dir is None:
            self.logger.info(f"🛡️ Protected file {file_path.name} - no action taken")
            return {
                'action': 'protected',
                'filename': file_path.name,
                'reason': 'Protected file'
            }
            
        # Create target directory if it doesn't exist
        full_target_path = self.project_root / target_dir
        full_target_path.mkdir(parents=True, exist_ok=True)
        
        # Move file
        new_file_path = full_target_path / file_path.name
        
        try:
            shutil.move(str(file_path), str(new_file_path))
            
            # Record movement
            self._record_file_movement(
                filename=file_path.name,
                original_path=str(file_path),
                new_path=str(new_file_path),
                file_type=file_path.suffix,
                size_bytes=new_file_path.stat().st_size,
                action_type='automatic_organization',
                success=True
            )
            
            self.logger.info(f"📁 Moved {file_path.name} → {target_dir}/")
            
            return {
                'action': 'organized',
                'filename': file_path.name,
                'original_path': str(file_path),
                'new_path': str(new_file_path),
                'target_directory': target_dir
            }
            
        except Exception as e:
            # Record failed movement
            self._record_file_movement(
                filename=file_path.name,
                original_path=str(file_path),
                new_path=str(new_file_path),
                file_type=file_path.suffix,
                size_bytes=0,
                action_type='automatic_organization',
                success=False,
                error_message=str(e)
            )
            
            raise e
            
    def _determine_target_directory(self, file_path: Path) -> Optional[str]:
        """Determine target directory for file based on organization rules"""
        
        file_extension = file_path.suffix.lower()
        
        if file_extension in self.organization_rules:
            rule = self.organization_rules[file_extension]
            
            if callable(rule):
                return rule(file_path)
            else:
                return rule
                
        # Default for unknown file types
        return 'misc'
        
    def _determine_python_location(self, file_path: Path) -> str:
        """Determine appropriate location for Python files"""
        
        filename = file_path.name.lower()
        
        # Test files
        if 'test' in filename:
            return 'tests'
            
        # Agent files
        if 'agent' in filename:
            return 'core_orchestration/agents'
            
        # Dashboard files
        if 'dashboard' in filename:
            return 'dashboard'
            
        # Configuration/setup files
        if filename in ['setup.py', 'config.py', 'settings.py']:
            return 'config'
            
        # Optimization scripts
        if 'optim' in filename:
            return 'core_orchestration/system_coordinator'
            
        # Default for other Python files
        return 'core_orchestration'
        
    def _record_file_movement(self, filename: str, original_path: str, new_path: str,
                            file_type: str, size_bytes: int, action_type: str,
                            success: bool, error_message: str = None):
        """Record file movement in database"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO file_movements 
            (timestamp, filename, original_path, new_path, file_type, size_bytes, 
             action_type, success, error_message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().timestamp(),
            filename,
            original_path,
            new_path,
            file_type,
            size_bytes,
            action_type,
            success,
            error_message
        ))
        
        conn.commit()
        conn.close()
        
    def _record_scan_results(self, results: Dict[str, any], duration: float):
        """Record scan results in database"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO scan_results 
            (timestamp, files_found, files_organized, files_protected, 
             files_requiring_approval, scan_duration)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().timestamp(),
            results['files_found'],
            results['files_organized'],
            results['files_protected'],
            results['files_requiring_approval'],
            duration
        ))
        
        conn.commit()
        conn.close()
        
    def get_organization_report(self) -> Dict[str, any]:
        """Generate organization status report"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get recent scan results
        cursor.execute("""
            SELECT * FROM scan_results 
            ORDER BY timestamp DESC 
            LIMIT 1
        """)
        latest_scan = cursor.fetchone()
        
        # Get movement statistics
        cursor.execute("""
            SELECT COUNT(*) as total_movements,
                   SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_movements,
                   SUM(size_bytes) as total_bytes_organized
            FROM file_movements
            WHERE timestamp > ?
        """, (datetime.now().timestamp() - 86400,))  # Last 24 hours
        
        movement_stats = cursor.fetchone()
        
        conn.close()
        
        return {
            'latest_scan': {
                'timestamp': latest_scan[1] if latest_scan else None,
                'files_found': latest_scan[2] if latest_scan else 0,
                'files_organized': latest_scan[3] if latest_scan else 0,
                'files_protected': latest_scan[4] if latest_scan else 0,
                'files_requiring_approval': latest_scan[5] if latest_scan else 0
            },
            'daily_stats': {
                'total_movements': movement_stats[0] if movement_stats else 0,
                'successful_movements': movement_stats[1] if movement_stats else 0,
                'total_bytes_organized': movement_stats[2] if movement_stats else 0
            },
            'agent_status': 'active',
            'agent_id': self.agent_id
        }

# Test function for development
async def main():
    """Test function for the file organization agent"""
    agent = FileOrganizationAgent()
    results = await agent.run_organization_cycle()
    
    print("🧹 File Organization Results:")
    print(f"   Files Found: {results['files_found']}")
    print(f"   Files Organized: {results['files_organized']}")
    print(f"   Files Protected: {results['files_protected']}")
    print(f"   Requiring Approval: {results['files_requiring_approval']}")
    
    if results['errors']:
        print(f"   Errors: {len(results['errors'])}")
        
    report = agent.get_organization_report()
    print(f"\n📊 Organization Report: {json.dumps(report, indent=2)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 