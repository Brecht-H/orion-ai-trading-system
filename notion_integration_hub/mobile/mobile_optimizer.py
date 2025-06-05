#!/usr/bin/env python3
"""
Mobile Optimizer - ORION PHASE 3
CEO-optimized mobile experience for executive dashboard
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import logging
import os

@dataclass
class MobileConfig:
    """Mobile optimization configuration"""
    max_items_per_view: int = 10
    enable_push_notifications: bool = True
    fast_loading_mode: bool = True
    compact_view: bool = True
    critical_alerts_only: bool = False
    one_click_actions: bool = True
    offline_fallback: bool = True

@dataclass
class MobileView:
    """Optimized mobile view structure"""
    view_type: str
    title: str
    items: List[Dict[str, Any]]
    actions: List[Dict[str, Any]]
    refresh_time: str
    status: str

class MobileOptimizer:
    """
    ORION Mobile Optimizer
    Optimizes all dashboard content for mobile CEO experience
    """
    
    def __init__(self, config: Optional[MobileConfig] = None):
        self.config = config or MobileConfig()
        self.logger = self.setup_logging()
        
        # Mobile state
        self.cached_views = {}
        self.last_optimization_time = None
        self.optimization_count = 0
        
        self.logger.info("📱 Mobile Optimizer initialized for CEO dashboard")
    
    def setup_logging(self):
        """Setup mobile optimizer logging"""
        Path("logs").mkdir(exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - MobileOptimizer - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/mobile_optimizer.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def optimize_dashboard_for_mobile(self, dashboard_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform dashboard data for optimal mobile experience"""
        self.logger.info("📱 Optimizing dashboard for mobile experience...")
        
        start_time = time.time()
        
        try:
            # Create mobile-optimized views
            mobile_dashboard = {
                "overview": self.create_overview_mobile_view(dashboard_data),
                "alerts": self.create_alerts_mobile_view(dashboard_data),
                "signals": self.create_signals_mobile_view(dashboard_data),
                "performance": self.create_performance_mobile_view(dashboard_data),
                "quick_actions": self.create_quick_actions_view(),
                "settings": self.create_settings_mobile_view()
            }
            
            # Add mobile metadata
            mobile_dashboard["mobile_metadata"] = {
                "optimized_at": datetime.now().isoformat(),
                "optimization_time": time.time() - start_time,
                "views_count": len(mobile_dashboard) - 1,  # Exclude metadata
                "config": asdict(self.config),
                "device_type": "mobile_optimized"
            }
            
            # Cache for offline access
            if self.config.offline_fallback:
                self.cached_views = mobile_dashboard.copy()
            
            self.optimization_count += 1
            self.last_optimization_time = datetime.now()
            
            self.logger.info(f"✅ Mobile optimization complete in {time.time() - start_time:.2f}s")
            return mobile_dashboard
            
        except Exception as e:
            self.logger.error(f"❌ Error optimizing for mobile: {e}")
            
            # Return cached views if available
            if self.cached_views:
                self.logger.info("📱 Returning cached mobile views")
                return self.cached_views
            
            raise
    
    def create_overview_mobile_view(self, dashboard_data: Dict[str, Any]) -> MobileView:
        """Create mobile-optimized overview with most critical metrics"""
        
        try:
            # Get critical metrics only
            all_metrics = dashboard_data.get('metrics', [])
            
            # Prioritize most important metrics for mobile
            critical_metrics = []
            priority_names = [
                "System Health", "Total Signals Processed", "Active Strategies",
                "Processing Speed", "Strategy Signals", "Market Signals Generated"
            ]
            
            # Add priority metrics first
            for priority_name in priority_names:
                for metric in all_metrics:
                    if any(priority in metric.get('name', '') for priority in priority_name.split()):
                        critical_metrics.append({
                            "name": self.shorten_metric_name(metric.get('name', '')),
                            "value": metric.get('value', ''),
                            "status": self.get_status_emoji(metric.get('status', 'good')),
                            "change": metric.get('change', ''),
                            "priority": "high"
                        })
                        break
            
            # Limit to mobile-friendly count
            critical_metrics = critical_metrics[:self.config.max_items_per_view]
            
            actions = [
                {
                    "name": "🚨 View Alerts",
                    "type": "navigate",
                    "target": "alerts",
                    "urgent": True
                },
                {
                    "name": "🎯 Strategy Signals",
                    "type": "navigate", 
                    "target": "signals",
                    "urgent": False
                },
                {
                    "name": "🔄 Refresh",
                    "type": "refresh",
                    "target": "overview",
                    "urgent": False
                }
            ]
            
            return MobileView(
                view_type="overview",
                title="🎯 ORION Command Center",
                items=critical_metrics,
                actions=actions,
                refresh_time=datetime.now().strftime('%H:%M'),
                status="operational"
            )
            
        except Exception as e:
            self.logger.error(f"❌ Error creating mobile overview: {e}")
            return self.create_fallback_view("overview")
    
    def create_alerts_mobile_view(self, dashboard_data: Dict[str, Any]) -> MobileView:
        """Create mobile-optimized alerts view with action priorities"""
        
        try:
            all_alerts = dashboard_data.get('alerts', [])
            
            # Sort alerts by priority for mobile
            priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
            sorted_alerts = sorted(all_alerts, key=lambda x: priority_order.get(x.get('priority', 'LOW'), 3))
            
            # Filter for mobile display
            if self.config.critical_alerts_only:
                mobile_alerts = [a for a in sorted_alerts if a.get('priority') in ['CRITICAL', 'HIGH']]
            else:
                mobile_alerts = sorted_alerts[:self.config.max_items_per_view]
            
            # Format for mobile
            formatted_alerts = []
            for alert in mobile_alerts:
                formatted_alerts.append({
                    "title": self.truncate_text(alert.get('title', ''), 40),
                    "message": self.truncate_text(alert.get('message', ''), 80),
                    "priority": self.get_priority_emoji(alert.get('priority', 'LOW')),
                    "source": alert.get('source', ''),
                    "requires_action": alert.get('requires_action', False),
                    "timestamp": self.format_mobile_time(alert.get('timestamp', ''))
                })
            
            actions = [
                {
                    "name": "✅ Acknowledge All",
                    "type": "action",
                    "target": "acknowledge_alerts",
                    "urgent": len(mobile_alerts) > 0
                },
                {
                    "name": "🔍 View Details",
                    "type": "navigate",
                    "target": "alert_details",
                    "urgent": False
                }
            ]
            
            return MobileView(
                view_type="alerts",
                title=f"🚨 Alerts ({len(formatted_alerts)})",
                items=formatted_alerts,
                actions=actions,
                refresh_time=datetime.now().strftime('%H:%M'),
                status="requires_attention" if len(mobile_alerts) > 0 else "clear"
            )
            
        except Exception as e:
            self.logger.error(f"❌ Error creating mobile alerts view: {e}")
            return self.create_fallback_view("alerts")
    
    def create_signals_mobile_view(self, dashboard_data: Dict[str, Any]) -> MobileView:
        """Create mobile-optimized strategy signals view for CEO approval"""
        
        try:
            all_signals = dashboard_data.get('strategy_signals', [])
            
            # Show only pending signals on mobile
            pending_signals = [s for s in all_signals if s.get('status') == 'pending']
            mobile_signals = pending_signals[:self.config.max_items_per_view]
            
            # Format for mobile decision making
            formatted_signals = []
            for signal in mobile_signals:
                formatted_signals.append({
                    "strategy": signal.get('strategy', ''),
                    "symbol": signal.get('symbol', ''),
                    "action": self.get_action_emoji(signal.get('action', '')),
                    "confidence": f"{signal.get('confidence', 0)*100:.0f}%",
                    "expected_return": f"{signal.get('expected_return', 0)*100:.1f}%",
                    "risk_score": f"{signal.get('risk_score', 0)*100:.0f}%",
                    "reasoning": self.truncate_text(signal.get('reasoning', ''), 60),
                    "quick_decision": True
                })
            
            actions = []
            if len(formatted_signals) > 0:
                actions.extend([
                    {
                        "name": "✅ Approve All",
                        "type": "bulk_action",
                        "target": "approve_signals",
                        "urgent": True
                    },
                    {
                        "name": "❌ Reject All",
                        "type": "bulk_action",
                        "target": "reject_signals",
                        "urgent": False
                    },
                    {
                        "name": "📊 Individual Review",
                        "type": "navigate",
                        "target": "signal_details",
                        "urgent": False
                    }
                ])
            else:
                actions.append({
                    "name": "🔍 Check for New Signals",
                    "type": "refresh",
                    "target": "signals",
                    "urgent": False
                })
            
            return MobileView(
                view_type="signals",
                title=f"🎯 Strategy Signals ({len(formatted_signals)})",
                items=formatted_signals,
                actions=actions,
                refresh_time=datetime.now().strftime('%H:%M'),
                status="requires_decision" if len(formatted_signals) > 0 else "no_pending"
            )
            
        except Exception as e:
            self.logger.error(f"❌ Error creating mobile signals view: {e}")
            return self.create_fallback_view("signals")
    
    def create_performance_mobile_view(self, dashboard_data: Dict[str, Any]) -> MobileView:
        """Create mobile-optimized performance summary"""
        
        try:
            all_performance = dashboard_data.get('performance', [])
            
            # Show key performance indicators on mobile
            mobile_performance = []
            key_metrics = ["Signal Accuracy", "Processing Speed", "System Uptime", "Dashboard Updates"]
            
            for metric_name in key_metrics:
                for perf in all_performance:
                    if metric_name.lower() in perf.get('metric', '').lower():
                        mobile_performance.append({
                            "name": self.shorten_metric_name(perf.get('metric', '')),
                            "current": perf.get('daily', ''),
                            "trend": self.get_trend_emoji(perf.get('trend', 'Stable')),
                            "target": perf.get('target', ''),
                            "status": "good" if perf.get('trend') == "Improving" else "stable"
                        })
                        break
            
            actions = [
                {
                    "name": "📈 Detailed Report",
                    "type": "navigate",
                    "target": "detailed_performance",
                    "urgent": False
                },
                {
                    "name": "📊 Historical Data",
                    "type": "navigate",
                    "target": "performance_history",
                    "urgent": False
                }
            ]
            
            return MobileView(
                view_type="performance",
                title="📈 Performance Summary",
                items=mobile_performance,
                actions=actions,
                refresh_time=datetime.now().strftime('%H:%M'),
                status="tracking"
            )
            
        except Exception as e:
            self.logger.error(f"❌ Error creating mobile performance view: {e}")
            return self.create_fallback_view("performance")
    
    def create_quick_actions_view(self) -> MobileView:
        """Create quick action buttons for CEO mobile experience"""
        
        quick_actions = [
            {
                "name": "🚨 Emergency Stop",
                "description": "Stop all trading immediately",
                "type": "emergency_action",
                "target": "emergency_stop",
                "urgent": True,
                "confirmation_required": True
            },
            {
                "name": "⏸️ Pause System",
                "description": "Temporarily pause signal processing",
                "type": "system_action",
                "target": "pause_system",
                "urgent": False,
                "confirmation_required": True
            },
            {
                "name": "🔄 Force Refresh",
                "description": "Refresh all data immediately",
                "type": "refresh_action",
                "target": "force_refresh",
                "urgent": False,
                "confirmation_required": False
            },
            {
                "name": "📧 Send Report",
                "description": "Email current status report",
                "type": "report_action",
                "target": "send_report",
                "urgent": False,
                "confirmation_required": False
            },
            {
                "name": "⚙️ System Settings",
                "description": "Adjust system parameters",
                "type": "navigate",
                "target": "settings",
                "urgent": False,
                "confirmation_required": False
            }
        ]
        
        return MobileView(
            view_type="quick_actions",
            title="⚡ Quick Actions",
            items=quick_actions,
            actions=[],
            refresh_time=datetime.now().strftime('%H:%M'),
            status="ready"
        )
    
    def create_settings_mobile_view(self) -> MobileView:
        """Create mobile-optimized settings view"""
        
        settings = [
            {
                "name": "Alert Threshold",
                "current_value": "HIGH+",
                "type": "select",
                "options": ["ALL", "MEDIUM+", "HIGH+", "CRITICAL"]
            },
            {
                "name": "Auto-Refresh",
                "current_value": "30s",
                "type": "select",
                "options": ["10s", "30s", "60s", "MANUAL"]
            },
            {
                "name": "Notification Push",
                "current_value": "ON",
                "type": "toggle",
                "options": ["ON", "OFF"]
            },
            {
                "name": "Compact View",
                "current_value": "ON",
                "type": "toggle",
                "options": ["ON", "OFF"]
            }
        ]
        
        actions = [
            {
                "name": "💾 Save Settings",
                "type": "save_action",
                "target": "save_settings",
                "urgent": False
            },
            {
                "name": "🔄 Reset Defaults",
                "type": "reset_action",
                "target": "reset_settings",
                "urgent": False
            }
        ]
        
        return MobileView(
            view_type="settings",
            title="⚙️ Mobile Settings",
            items=settings,
            actions=actions,
            refresh_time=datetime.now().strftime('%H:%M'),
            status="configurable"
        )
    
    def create_fallback_view(self, view_type: str) -> MobileView:
        """Create fallback view when data unavailable"""
        
        return MobileView(
            view_type=view_type,
            title=f"📱 {view_type.title()} (Offline)",
            items=[{
                "name": "System Status",
                "value": "Offline Mode",
                "status": "⚠️",
                "message": "Using cached data"
            }],
            actions=[{
                "name": "🔄 Retry Connection",
                "type": "refresh",
                "target": view_type,
                "urgent": True
            }],
            refresh_time=datetime.now().strftime('%H:%M'),
            status="offline"
        )
    
    # Utility methods for mobile optimization
    
    def shorten_metric_name(self, name: str) -> str:
        """Shorten metric names for mobile display"""
        replacements = {
            "Total Signals Processed": "🔄 Signals",
            "Market Signals Generated": "🎯 Market",
            "Strategy Signals Generated": "📊 Strategy", 
            "Processing Speed": "⚡ Speed",
            "Active Strategies": "🎮 Active",
            "Database Records": "💾 Records",
            "System Health": "💚 Health",
            "Dashboard Updates": "🔄 Updates"
        }
        
        for long_name, short_name in replacements.items():
            if long_name in name:
                return short_name
        
        # Generic shortening
        if len(name) > 15:
            return name[:12] + "..."
        
        return name
    
    def truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text for mobile display"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    def get_status_emoji(self, status: str) -> str:
        """Convert status to emoji for mobile"""
        status_map = {
            "good": "🟢",
            "warning": "🟡", 
            "critical": "🔴",
            "unknown": "⚪"
        }
        return status_map.get(status, "⚪")
    
    def get_priority_emoji(self, priority: str) -> str:
        """Convert priority to emoji for mobile"""
        priority_map = {
            "CRITICAL": "🔴",
            "HIGH": "🟠",
            "MEDIUM": "🟡",
            "LOW": "🟢"
        }
        return priority_map.get(priority, "🟢")
    
    def get_action_emoji(self, action: str) -> str:
        """Convert action to emoji for mobile"""
        action_map = {
            "BUY": "🟢",
            "SELL": "🔴",
            "CLOSE": "⏹️",
            "HOLD": "⏸️"
        }
        return action_map.get(action, "⚪")
    
    def get_trend_emoji(self, trend: str) -> str:
        """Convert trend to emoji for mobile"""
        trend_map = {
            "Improving": "📈",
            "Stable": "📊",
            "Declining": "📉"
        }
        return trend_map.get(trend, "📊")
    
    def format_mobile_time(self, timestamp: str) -> str:
        """Format timestamp for mobile display"""
        try:
            if isinstance(timestamp, str):
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            else:
                dt = timestamp
            
            now = datetime.now()
            diff = now - dt.replace(tzinfo=None)
            
            if diff.days > 0:
                return f"{diff.days}d ago"
            elif diff.seconds > 3600:
                return f"{diff.seconds // 3600}h ago"
            elif diff.seconds > 60:
                return f"{diff.seconds // 60}m ago"
            else:
                return "just now"
                
        except Exception:
            return "unknown"
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Get mobile optimization statistics"""
        return {
            "optimization_count": self.optimization_count,
            "last_optimization": self.last_optimization_time.isoformat() if self.last_optimization_time else None,
            "cached_views": len(self.cached_views),
            "config": asdict(self.config),
            "status": "operational"
        }

# Test function
def main():
    """Test the Mobile Optimizer"""
    print("📱 Testing Mobile Optimizer - Phase 3 Dashboard Integration...")
    
    # Mock dashboard data
    test_data = {
        "metrics": [
            {"name": "Total Signals Processed", "value": "78", "status": "good", "change": "+12%"},
            {"name": "System Health", "value": "100%", "status": "good", "change": "Excellent"},
            {"name": "Processing Speed", "value": "145.7/sec", "status": "good", "change": "Stable"}
        ],
        "alerts": [
            {"title": "High Confidence Signal", "message": "BTC signal detected", "priority": "HIGH", "requires_action": True, "timestamp": datetime.now().isoformat()},
            {"title": "Correlation Pattern", "message": "1,399 correlations found", "priority": "MEDIUM", "requires_action": False, "timestamp": datetime.now().isoformat()}
        ],
        "strategy_signals": [],
        "performance": [
            {"metric": "Signal Accuracy", "daily": "78%", "trend": "Improving", "target": "75%+"}
        ]
    }
    
    try:
        optimizer = MobileOptimizer()
        mobile_dashboard = optimizer.optimize_dashboard_for_mobile(test_data)
        
        print(f"✅ Mobile Dashboard Optimized:")
        print(f"   📱 Views Created: {len(mobile_dashboard) - 1}")
        print(f"   ⏱️ Optimization Time: {mobile_dashboard['mobile_metadata']['optimization_time']:.2f}s")
        print(f"   📊 Overview Items: {len(mobile_dashboard['overview'].items)}")
        print(f"   🚨 Alert Items: {len(mobile_dashboard['alerts'].items)}")
        
        stats = optimizer.get_optimization_stats()
        print(f"\n📈 Optimization Stats:")
        print(f"   🔄 Count: {stats['optimization_count']}")
        print(f"   💾 Cached Views: {stats['cached_views']}")
        print(f"   ✅ Status: {stats['status']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()