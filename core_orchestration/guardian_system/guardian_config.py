"""
🛡️ Guardian System Configuration
Monitors entire Orion project health and functionality
"""

import os
from pathlib import Path

# Orion project paths
ORION_ROOT = Path(__file__).parent.parent.parent
DATABASE_PATHS = {
    "sqlite": ORION_ROOT / "databases" / "sqlite_dbs",
    "vector": ORION_ROOT / "databases" / "vector_stores",
    "cache": ORION_ROOT / "databases" / "cache"
}

MONITORING_CENTERS = [
    "research_center",
    "knowledge_center", 
    "strategy_center",
    "technical_analysis_center",
    "risk_management_center",
    "notion_integration_hub"
]

# Guardian capabilities
GUARDIAN_FEATURES = {
    "health_monitoring": True,
    "cost_optimization": True,
    "gap_analysis": True,
    "user_story_generation": True,
    "automated_testing": True,
    "performance_tracking": True
}

# Mac Mini integration
MAC_MINI_CONFIG = {
    "deployment_ready": True,
    "24_7_operation": True,
    "autonomous_mode": True,
    "backup_processing": True
}
