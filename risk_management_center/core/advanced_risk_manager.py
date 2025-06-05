#!/usr/bin/env python3
"""
Advanced Risk Manager - ORION PHASE 4
Enterprise-grade risk management for live trading
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import os
import sys
from decimal import Decimal
from enum import Enum
import numpy as np
import pandas as pd

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertType(Enum):
    POSITION_LIMIT = "position_limit"
    DRAWDOWN = "drawdown"
    CORRELATION = "correlation"
    VOLATILITY = "volatility"
    LIQUIDITY = "liquidity"
    CONCENTRATION = "concentration"
    MARGIN = "margin"
    COMPLIANCE = "compliance"

@dataclass
class RiskAlert:
    """Risk management alert"""
    alert_id: str
    alert_type: AlertType
    risk_level: RiskLevel
    message: str
    affected_positions: List[str]
    recommended_action: str
    timestamp: datetime
    acknowledged: bool = False
    resolved: bool = False

@dataclass
class PortfolioMetrics:
    """Portfolio risk metrics"""
    total_value: Decimal
    total_pnl: Decimal
    unrealized_pnl: Decimal
    realized_pnl: Decimal
    max_drawdown: Decimal
    current_drawdown: Decimal
    sharpe_ratio: Decimal
    sortino_ratio: Decimal
    var_95: Decimal  # Value at Risk 95%
    var_99: Decimal  # Value at Risk 99%
    beta: Decimal
    correlation_risk: Decimal
    concentration_risk: Decimal
    liquidity_risk: Decimal
    timestamp: datetime

@dataclass
class RiskLimits:
    """Comprehensive risk limits"""
    # Position limits
    max_position_size_usd: Decimal = Decimal('1000')
    max_position_size_percent: Decimal = Decimal('5.0')
    max_positions_total: int = 10
    max_positions_per_strategy: int = 3
    max_positions_per_symbol: int = 2
    
    # Portfolio limits
    max_portfolio_risk_percent: Decimal = Decimal('2.0')
    max_daily_loss_usd: Decimal = Decimal('500')
    max_daily_loss_percent: Decimal = Decimal('5.0')
    max_drawdown_percent: Decimal = Decimal('15.0')
    max_leverage: Decimal = Decimal('3.0')
    
    # Correlation limits
    max_correlation_exposure: Decimal = Decimal('0.7')
    max_sector_concentration: Decimal = Decimal('30.0')
    max_single_asset_percent: Decimal = Decimal('20.0')
    
    # Risk metrics limits
    min_sharpe_ratio: Decimal = Decimal('0.5')
    max_var_95_percent: Decimal = Decimal('3.0')
    min_liquidity_score: Decimal = Decimal('0.6')
    
    # Trading limits
    min_confidence_threshold: Decimal = Decimal('0.7')
    max_trades_per_hour: int = 10
    max_trades_per_day: int = 50
    
    # Emergency limits
    emergency_stop_drawdown: Decimal = Decimal('20.0')
    emergency_stop_daily_loss: Decimal = Decimal('1000')

class AdvancedRiskManager:
    """
    ORION Advanced Risk Management System
    Enterprise-grade risk controls and monitoring
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.logger = self.setup_logging()
        
        # Load configuration
        self.config = self.load_config(config_path)
        self.risk_limits = RiskLimits()
        
        # Risk state
        self.active_alerts: Dict[str, RiskAlert] = {}
        self.portfolio_metrics: Optional[PortfolioMetrics] = None
        self.risk_monitoring_enabled = True
        self.emergency_mode = False
        
        # Historical data for risk calculations
        self.price_history: Dict[str, List[Tuple[datetime, Decimal]]] = {}
        self.pnl_history: List[Tuple[datetime, Decimal]] = []
        self.trade_history: List[Dict[str, Any]] = []
        
        # Risk calculation cache
        self.correlation_matrix: Optional[pd.DataFrame] = None
        self.volatility_cache: Dict[str, Decimal] = {}
        self.last_risk_calculation = datetime.min
        
        # Database connection
        self.db_path = "databases/sqlite_dbs/risk_management.db"
        self.initialize_database()
        
        self.logger.info("🛡️ Advanced Risk Manager initialized")
    
    def setup_logging(self):
        """Setup risk management logging"""
        Path("logs").mkdir(exist_ok=True)
        Path("logs/risk").mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - RiskManager - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/risk/risk_management.log'),
                logging.FileHandler('logs/risk/alerts.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load risk management configuration"""
        default_config = {
            "risk_calculation": {
                "var_confidence_levels": [0.95, 0.99],
                "correlation_lookback_days": 30,
                "volatility_lookback_days": 20,
                "update_interval_seconds": 30
            },
            "alerts": {
                "email_notifications": True,
                "slack_notifications": False,
                "notion_integration": True,
                "alert_cooldown_minutes": 5
            },
            "compliance": {
                "enable_audit_trail": True,
                "position_reporting": True,
                "risk_reporting_interval_hours": 6
            }
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                custom_config = json.load(f)
                default_config.update(custom_config)
        
        return default_config
    
    def initialize_database(self):
        """Initialize risk management database"""
        import sqlite3
        
        Path("databases/sqlite_dbs").mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Risk alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS risk_alerts (
                alert_id TEXT PRIMARY KEY,
                alert_type TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                message TEXT NOT NULL,
                affected_positions TEXT,
                recommended_action TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                acknowledged BOOLEAN DEFAULT FALSE,
                resolved BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # Portfolio metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS portfolio_metrics (
                timestamp TEXT PRIMARY KEY,
                total_value REAL NOT NULL,
                total_pnl REAL NOT NULL,
                unrealized_pnl REAL NOT NULL,
                realized_pnl REAL NOT NULL,
                max_drawdown REAL NOT NULL,
                current_drawdown REAL NOT NULL,
                sharpe_ratio REAL NOT NULL,
                sortino_ratio REAL NOT NULL,
                var_95 REAL NOT NULL,
                var_99 REAL NOT NULL,
                beta REAL NOT NULL,
                correlation_risk REAL NOT NULL,
                concentration_risk REAL NOT NULL,
                liquidity_risk REAL NOT NULL
            )
        ''')
        
        # Risk events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS risk_events (
                event_id TEXT PRIMARY KEY,
                event_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT NOT NULL,
                positions_affected TEXT,
                action_taken TEXT,
                timestamp TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        
        self.logger.info("✅ Risk management database initialized")
    
    async def assess_trading_signal_risk(self, signal: Dict[str, Any], current_positions: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive risk assessment for new trading signal"""
        
        assessment = {
            "approved": True,
            "risk_score": 0.0,
            "warnings": [],
            "blocking_issues": [],
            "recommended_position_size": None,
            "risk_adjustments": {}
        }
        
        try:
            # 1. Position limit checks
            position_risk = await self.check_position_limits(signal, current_positions)
            assessment["risk_score"] += position_risk["risk_score"]
            assessment["warnings"].extend(position_risk["warnings"])
            assessment["blocking_issues"].extend(position_risk["blocking_issues"])
            
            # 2. Portfolio risk assessment
            portfolio_risk = await self.assess_portfolio_risk(signal, current_positions)
            assessment["risk_score"] += portfolio_risk["risk_score"]
            assessment["warnings"].extend(portfolio_risk["warnings"])
            
            # 3. Correlation analysis
            correlation_risk = await self.analyze_correlation_risk(signal, current_positions)
            assessment["risk_score"] += correlation_risk["risk_score"]
            assessment["warnings"].extend(correlation_risk["warnings"])
            
            # 4. Volatility assessment
            volatility_risk = await self.assess_volatility_risk(signal)
            assessment["risk_score"] += volatility_risk["risk_score"]
            assessment["warnings"].extend(volatility_risk["warnings"])
            
            # 5. Liquidity check
            liquidity_risk = await self.check_liquidity_risk(signal)
            assessment["risk_score"] += liquidity_risk["risk_score"]
            assessment["warnings"].extend(liquidity_risk["warnings"])
            
            # 6. Calculate recommended position size
            assessment["recommended_position_size"] = await self.calculate_optimal_position_size(
                signal, current_positions, assessment["risk_score"]
            )
            
            # 7. Final approval decision
            if assessment["blocking_issues"]:
                assessment["approved"] = False
            elif assessment["risk_score"] > 0.8:
                assessment["approved"] = False
                assessment["blocking_issues"].append("Overall risk score too high")
            
            # 8. Generate risk-adjusted recommendations
            if assessment["approved"]:
                assessment["risk_adjustments"] = await self.generate_risk_adjustments(signal, assessment)
            
            self.logger.info(f"🔍 Risk assessment complete: {signal.get('symbol', 'Unknown')} - Score: {assessment['risk_score']:.2f}")
            
        except Exception as e:
            self.logger.error(f"❌ Error in risk assessment: {e}")
            assessment["approved"] = False
            assessment["blocking_issues"].append(f"Risk assessment error: {str(e)}")
        
        return assessment
    
    async def check_position_limits(self, signal: Dict[str, Any], current_positions: Dict[str, Any]) -> Dict[str, Any]:
        """Check position-related risk limits"""
        
        result = {
            "risk_score": 0.0,
            "warnings": [],
            "blocking_issues": []
        }
        
        # Count current positions
        total_positions = len(current_positions)
        strategy_positions = len([p for p in current_positions.values() 
                                if p.get('strategy') == signal.get('strategy_name')])
        symbol_positions = len([p for p in current_positions.values() 
                              if p.get('symbol') == signal.get('symbol')])
        
        # Check total position limit
        if total_positions >= self.risk_limits.max_positions_total:
            result["blocking_issues"].append(f"Maximum total positions ({self.risk_limits.max_positions_total}) reached")
        elif total_positions >= self.risk_limits.max_positions_total * 0.8:
            result["warnings"].append("Approaching maximum total positions")
            result["risk_score"] += 0.2
        
        # Check strategy position limit
        if strategy_positions >= self.risk_limits.max_positions_per_strategy:
            result["blocking_issues"].append(f"Maximum strategy positions ({self.risk_limits.max_positions_per_strategy}) reached")
        elif strategy_positions >= self.risk_limits.max_positions_per_strategy * 0.8:
            result["warnings"].append("Approaching maximum strategy positions")
            result["risk_score"] += 0.1
        
        # Check symbol position limit
        if symbol_positions >= self.risk_limits.max_positions_per_symbol:
            result["blocking_issues"].append(f"Maximum symbol positions ({self.risk_limits.max_positions_per_symbol}) reached")
        elif symbol_positions >= self.risk_limits.max_positions_per_symbol * 0.8:
            result["warnings"].append("Approaching maximum symbol positions")
            result["risk_score"] += 0.1
        
        return result
    
    async def assess_portfolio_risk(self, signal: Dict[str, Any], current_positions: Dict[str, Any]) -> Dict[str, Any]:
        """Assess portfolio-level risk metrics"""
        
        result = {
            "risk_score": 0.0,
            "warnings": []
        }
        
        # Calculate current portfolio metrics
        if self.portfolio_metrics:
            # Check drawdown
            if self.portfolio_metrics.current_drawdown >= self.risk_limits.max_drawdown_percent * 0.8:
                result["warnings"].append(f"High drawdown: {self.portfolio_metrics.current_drawdown:.2f}%")
                result["risk_score"] += 0.3
            
            # Check daily loss
            daily_loss_percent = abs(float(self.portfolio_metrics.total_pnl)) / float(self.portfolio_metrics.total_value) * 100
            if daily_loss_percent >= float(self.risk_limits.max_daily_loss_percent) * 0.8:
                result["warnings"].append(f"High daily loss: {daily_loss_percent:.2f}%")
                result["risk_score"] += 0.2
            
            # Check VaR
            if self.portfolio_metrics.var_95 >= self.risk_limits.max_var_95_percent * 0.8:
                result["warnings"].append(f"High VaR: {self.portfolio_metrics.var_95:.2f}%")
                result["risk_score"] += 0.2
            
            # Check Sharpe ratio
            if self.portfolio_metrics.sharpe_ratio <= self.risk_limits.min_sharpe_ratio:
                result["warnings"].append(f"Low Sharpe ratio: {self.portfolio_metrics.sharpe_ratio:.2f}")
                result["risk_score"] += 0.1
        
        return result
    
    async def analyze_correlation_risk(self, signal: Dict[str, Any], current_positions: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze correlation risk with existing positions"""
        
        result = {
            "risk_score": 0.0,
            "warnings": []
        }
        
        try:
            signal_symbol = signal.get('symbol', '')
            signal_asset = signal_symbol.split('/')[0] if '/' in signal_symbol else signal_symbol
            
            # Check for similar assets
            similar_assets = []
            for position in current_positions.values():
                pos_symbol = position.get('symbol', '')
                pos_asset = pos_symbol.split('/')[0] if '/' in pos_symbol else pos_symbol
                
                if pos_asset == signal_asset:
                    similar_assets.append(pos_asset)
            
            # Calculate concentration risk
            if len(similar_assets) > 0:
                concentration = len(similar_assets) / len(current_positions) if current_positions else 0
                if concentration > 0.5:
                    result["warnings"].append(f"High asset concentration: {concentration:.2f}")
                    result["risk_score"] += concentration * 0.3
            
        except Exception as e:
            self.logger.error(f"❌ Error in correlation analysis: {e}")
        
        return result
    
    async def assess_volatility_risk(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """Assess volatility risk for the signal"""
        
        result = {
            "risk_score": 0.0,
            "warnings": []
        }
        
        try:
            symbol = signal.get('symbol', '')
            
            # Get cached volatility or calculate
            volatility = self.volatility_cache.get(symbol)
            if volatility is None:
                volatility = await self.calculate_volatility(symbol)
                self.volatility_cache[symbol] = volatility
            
            # Assess volatility level
            if volatility > Decimal('0.05'):  # 5% daily volatility
                result["warnings"].append(f"High volatility: {volatility:.3f}")
                result["risk_score"] += float(volatility) * 2  # Scale volatility to risk score
            elif volatility > Decimal('0.03'):  # 3% daily volatility
                result["warnings"].append(f"Moderate volatility: {volatility:.3f}")
                result["risk_score"] += float(volatility) * 1
            
        except Exception as e:
            self.logger.error(f"❌ Error in volatility assessment: {e}")
        
        return result
    
    async def check_liquidity_risk(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """Check liquidity risk for the trading pair"""
        
        result = {
            "risk_score": 0.0,
            "warnings": []
        }
        
        try:
            symbol = signal.get('symbol', '')
            
            # Major pairs have lower liquidity risk
            major_pairs = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'ADA/USDT', 'SOL/USDT']
            
            if symbol not in major_pairs:
                result["warnings"].append("Lower liquidity trading pair")
                result["risk_score"] += 0.1
            
            # Check if it's a new or exotic pair
            if '/' not in symbol or len(symbol.split('/')[0]) > 5:
                result["warnings"].append("Potentially illiquid asset")
                result["risk_score"] += 0.2
            
        except Exception as e:
            self.logger.error(f"❌ Error in liquidity check: {e}")
        
        return result
    
    async def calculate_optimal_position_size(self, signal: Dict[str, Any], current_positions: Dict[str, Any], risk_score: float) -> Decimal:
        """Calculate optimal position size based on risk assessment"""
        
        try:
            # Base position size from signal confidence
            base_confidence = signal.get('confidence', 0.7)
            base_size_percent = float(self.risk_limits.max_position_size_percent) * base_confidence
            
            # Adjust for risk score
            risk_adjustment = max(0.1, 1.0 - risk_score)
            adjusted_size_percent = base_size_percent * risk_adjustment
            
            # Apply portfolio concentration limits
            portfolio_value = sum(float(p.get('margin_used', 0)) for p in current_positions.values())
            if portfolio_value > 0:
                concentration_limit = float(self.risk_limits.max_single_asset_percent) / 100
                max_position_value = portfolio_value * concentration_limit
                
                # Convert to percentage of available capital
                adjusted_size_percent = min(adjusted_size_percent, concentration_limit * 100)
            
            # Ensure minimum viable position
            final_size_percent = max(0.1, min(adjusted_size_percent, float(self.risk_limits.max_position_size_percent)))
            
            self.logger.info(f"💰 Optimal position size: {final_size_percent:.2f}% (risk-adjusted from {base_size_percent:.2f}%)")
            
            return Decimal(str(final_size_percent))
            
        except Exception as e:
            self.logger.error(f"❌ Error calculating position size: {e}")
            return Decimal('1.0')  # Conservative fallback
    
    async def generate_risk_adjustments(self, signal: Dict[str, Any], assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Generate risk-based adjustments for the trade"""
        
        adjustments = {
            "stop_loss_adjustment": 0.0,
            "take_profit_adjustment": 0.0,
            "position_size_multiplier": 1.0,
            "monitoring_frequency": "normal"
        }
        
        risk_score = assessment["risk_score"]
        
        # Tighter stops for higher risk
        if risk_score > 0.5:
            adjustments["stop_loss_adjustment"] = -0.5  # Tighter stop loss
            adjustments["monitoring_frequency"] = "high"
        
        if risk_score > 0.3:
            adjustments["take_profit_adjustment"] = -0.2  # Earlier profit taking
        
        # Reduce position size for high risk
        if risk_score > 0.6:
            adjustments["position_size_multiplier"] = 0.7
        elif risk_score > 0.4:
            adjustments["position_size_multiplier"] = 0.85
        
        return adjustments
    
    async def calculate_volatility(self, symbol: str) -> Decimal:
        """Calculate asset volatility"""
        # This would use historical price data
        # For now, return reasonable defaults based on asset type
        if 'BTC' in symbol:
            return Decimal('0.04')  # 4% daily volatility
        elif 'ETH' in symbol:
            return Decimal('0.05')  # 5% daily volatility
        else:
            return Decimal('0.06')  # 6% daily volatility for altcoins
    
    def get_risk_status(self) -> Dict[str, Any]:
        """Get comprehensive risk management status"""
        
        active_alerts_by_level = {}
        for alert in self.active_alerts.values():
            level = alert.risk_level.value
            if level not in active_alerts_by_level:
                active_alerts_by_level[level] = 0
            active_alerts_by_level[level] += 1
        
        return {
            "risk_monitoring_enabled": self.risk_monitoring_enabled,
            "emergency_mode": self.emergency_mode,
            "active_alerts": len(self.active_alerts),
            "alerts_by_level": active_alerts_by_level,
            "portfolio_metrics": asdict(self.portfolio_metrics) if self.portfolio_metrics else None,
            "risk_limits": asdict(self.risk_limits),
            "last_risk_calculation": self.last_risk_calculation.isoformat(),
            "cache_status": {
                "volatility_cache_size": len(self.volatility_cache),
                "correlation_matrix_available": self.correlation_matrix is not None,
                "pnl_history_length": len(self.pnl_history)
            }
        }

# Test function
async def main():
    """Test the Advanced Risk Manager"""
    print("🛡️ Testing Advanced Risk Manager - Phase 4...")
    
    try:
        # Initialize risk manager
        risk_manager = AdvancedRiskManager()
        
        # Get status
        status = risk_manager.get_risk_status()
        print(f"✅ Risk Manager Status:")
        print(f"   🔍 Monitoring: {'Enabled' if status['risk_monitoring_enabled'] else 'Disabled'}")
        print(f"   🚨 Active Alerts: {status['active_alerts']}")
        print(f"   📊 Cache Status: {status['cache_status']}")
        
        # Test signal risk assessment
        test_signal = {
            "strategy_name": "momentum",
            "symbol": "BTC/USDT",
            "action": "BUY",
            "confidence": 0.85,
            "expected_return": 0.05,
            "risk_score": 0.3
        }
        
        test_positions = {
            "pos1": {
                "symbol": "ETH/USDT",
                "strategy": "momentum",
                "margin_used": 500,
                "unrealized_pnl": 25,
                "realized_pnl": 0
            }
        }
        
        print(f"\n🧪 Testing signal risk assessment...")
        assessment = await risk_manager.assess_trading_signal_risk(test_signal, test_positions)
        
        print(f"   📊 Signal: {test_signal['symbol']} {test_signal['action']}")
        print(f"   ✅ Approved: {'YES' if assessment['approved'] else 'NO'}")
        print(f"   🎯 Risk Score: {assessment['risk_score']:.2f}")
        print(f"   ⚠️ Warnings: {len(assessment['warnings'])}")
        print(f"   🚫 Blocking Issues: {len(assessment['blocking_issues'])}")
        
        if assessment['warnings']:
            for warning in assessment['warnings']:
                print(f"      ⚠️ {warning}")
        
        if assessment['blocking_issues']:
            for issue in assessment['blocking_issues']:
                print(f"      🚫 {issue}")
        
        print(f"\n✅ Advanced Risk Manager test complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 