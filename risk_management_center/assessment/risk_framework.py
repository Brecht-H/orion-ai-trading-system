#!/usr/bin/env python3
"""
Orion Risk Management Framework v1.0
Comprehensive risk management system for crypto trading platform
"""

import sys
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import logging
sys.path.append('.')

from src.protocols.orion_unified_protocol_enhanced import EnhancedOrionUnifiedProtocolV3

class OrionRiskManager:
    """Advanced risk management system for crypto trading"""
    
    def __init__(self):
        """Initialize risk management system"""
        self.protocol = EnhancedOrionUnifiedProtocolV3()
        self.logger = logging.getLogger(__name__)
        
        # Risk Parameters (CEO can adjust these)
        self.risk_parameters = {
            "max_position_size_pct": 2.0,  # Maximum 2% per position
            "max_daily_loss_pct": 5.0,     # Maximum 5% daily loss
            "max_portfolio_drawdown_pct": 20.0,  # Maximum 20% portfolio drawdown
            "stop_loss_pct": 3.0,          # Default 3% stop loss
            "take_profit_pct": 6.0,        # Default 6% take profit (2:1 ratio)
            "max_open_positions": 5,       # Maximum simultaneous positions
            "max_correlation_exposure": 0.7,  # Maximum correlation between positions
            "leverage_limit": 2.0,          # Maximum 2x leverage
            "cooldown_period_hours": 4,     # Hours to wait after stop loss
        }
        
        # Portfolio tracking
        self.portfolio = {
            "total_capital": 10000.0,  # Default $10,000 - CEO should update
            "available_capital": 10000.0,
            "allocated_capital": 0.0,
            "current_positions": {},
            "daily_pnl": 0.0,
            "total_pnl": 0.0,
            "max_drawdown": 0.0,
            "win_rate": 0.0,
            "last_updated": datetime.now().isoformat()
        }
        
        self._setup_risk_database()
    
    def _setup_risk_database(self):
        """Set up risk management database tables"""
        
        # Create risk_settings table
        self.protocol._db_execute("""
            CREATE TABLE IF NOT EXISTS risk_settings (
                id TEXT PRIMARY KEY,
                parameter_name TEXT NOT NULL,
                parameter_value REAL NOT NULL,
                description TEXT,
                updated_date TEXT,
                updated_by TEXT
            )
        """, commit=True)
        
        # Create trading_positions table
        self.protocol._db_execute("""
            CREATE TABLE IF NOT EXISTS trading_positions (
                id TEXT PRIMARY KEY,
                symbol TEXT NOT NULL,
                side TEXT NOT NULL,
                entry_price REAL NOT NULL,
                position_size REAL NOT NULL,
                stop_loss REAL,
                take_profit REAL,
                current_price REAL,
                unrealized_pnl REAL,
                status TEXT DEFAULT 'open',
                entry_time TEXT,
                exit_time TEXT,
                exit_price REAL,
                realized_pnl REAL,
                created_date TEXT
            )
        """, commit=True)
        
        # Create risk_alerts table
        self.protocol._db_execute("""
            CREATE TABLE IF NOT EXISTS risk_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                message TEXT NOT NULL,
                portfolio_value REAL,
                current_drawdown REAL,
                triggered_time TEXT,
                acknowledged BOOLEAN DEFAULT FALSE
            )
        """, commit=True)
        
        # Create daily_performance table
        self.protocol._db_execute("""
            CREATE TABLE IF NOT EXISTS daily_performance (
                date TEXT PRIMARY KEY,
                starting_capital REAL,
                ending_capital REAL,
                daily_pnl REAL,
                daily_return_pct REAL,
                max_drawdown_pct REAL,
                number_of_trades INTEGER,
                winning_trades INTEGER,
                losing_trades INTEGER,
                largest_win REAL,
                largest_loss REAL
            )
        """, commit=True)
        
        print("✅ Risk management database tables created")
        
        # Initialize default risk parameters
        self._initialize_risk_parameters()
    
    def _initialize_risk_parameters(self):
        """Initialize default risk parameters in database"""
        now_iso = datetime.now().isoformat()
        
        for param_name, param_value in self.risk_parameters.items():
            self.protocol._db_execute("""
                INSERT OR REPLACE INTO risk_settings 
                (id, parameter_name, parameter_value, description, updated_date, updated_by)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                f"RISK_{param_name.upper()}",
                param_name,
                param_value,
                f"Risk parameter: {param_name.replace('_', ' ').title()}",
                now_iso,
                "orion_risk_manager"
            ), commit=True)
        
        print(f"✅ Initialized {len(self.risk_parameters)} risk parameters")
    
    def calculate_position_size(self, symbol: str, entry_price: float, 
                              account_balance: float) -> Dict:
        """Calculate optimal position size based on risk parameters"""
        
        max_position_value = account_balance * (self.risk_parameters["max_position_size_pct"] / 100)
        stop_loss_pct = self.risk_parameters["stop_loss_pct"] / 100
        
        # Calculate position size based on stop loss
        risk_per_share = entry_price * stop_loss_pct
        max_shares = max_position_value / entry_price
        risk_based_shares = max_position_value / risk_per_share if risk_per_share > 0 else max_shares
        
        # Use the more conservative calculation
        recommended_shares = min(max_shares, risk_based_shares)
        recommended_value = recommended_shares * entry_price
        
        return {
            "symbol": symbol,
            "recommended_shares": round(recommended_shares, 6),
            "recommended_value": round(recommended_value, 2),
            "max_loss": round(recommended_value * stop_loss_pct, 2),
            "max_loss_pct": self.risk_parameters["stop_loss_pct"],
            "position_size_pct": round((recommended_value / account_balance) * 100, 2),
            "entry_price": entry_price,
            "stop_loss_price": round(entry_price * (1 - stop_loss_pct), 6),
            "take_profit_price": round(entry_price * (1 + (self.risk_parameters["take_profit_pct"] / 100)), 6)
        }
    
    def validate_trade(self, trade_request: Dict) -> Dict:
        """Comprehensive trade validation against risk parameters"""
        
        validation_result = {
            "valid": True,
            "warnings": [],
            "rejections": [],
            "recommendations": []
        }
        
        symbol = trade_request.get("symbol", "")
        side = trade_request.get("side", "")  # "buy" or "sell"
        quantity = trade_request.get("quantity", 0)
        price = trade_request.get("price", 0)
        trade_value = quantity * price
        
        # 1. Position size validation
        position_pct = (trade_value / self.portfolio["available_capital"]) * 100
        if position_pct > self.risk_parameters["max_position_size_pct"]:
            validation_result["rejections"].append(
                f"Position size {position_pct:.1f}% exceeds maximum {self.risk_parameters['max_position_size_pct']}%"
            )
            validation_result["valid"] = False
        
        # 2. Available capital validation
        if trade_value > self.portfolio["available_capital"]:
            validation_result["rejections"].append(
                f"Insufficient capital: Need ${trade_value:.2f}, Available ${self.portfolio['available_capital']:.2f}"
            )
            validation_result["valid"] = False
        
        # 3. Maximum positions validation
        current_positions = len(self.portfolio["current_positions"])
        if current_positions >= self.risk_parameters["max_open_positions"]:
            validation_result["rejections"].append(
                f"Maximum positions limit reached: {current_positions}/{self.risk_parameters['max_open_positions']}"
            )
            validation_result["valid"] = False
        
        # 4. Daily loss limit validation
        if abs(self.portfolio["daily_pnl"]) >= (self.portfolio["total_capital"] * self.risk_parameters["max_daily_loss_pct"] / 100):
            validation_result["rejections"].append(
                f"Daily loss limit reached: {abs(self.portfolio['daily_pnl']):.2f}"
            )
            validation_result["valid"] = False
        
        # 5. Portfolio drawdown validation
        if self.portfolio["max_drawdown"] >= self.risk_parameters["max_portfolio_drawdown_pct"]:
            validation_result["rejections"].append(
                f"Portfolio drawdown limit reached: {self.portfolio['max_drawdown']:.1f}%"
            )
            validation_result["valid"] = False
        
        # 6. Generate recommendations if valid
        if validation_result["valid"]:
            optimal_size = self.calculate_position_size(symbol, price, self.portfolio["available_capital"])
            
            if quantity != optimal_size["recommended_shares"]:
                validation_result["recommendations"].append(
                    f"Recommended position size: {optimal_size['recommended_shares']} shares (${optimal_size['recommended_value']:.2f})"
                )
            
            validation_result["optimal_position"] = optimal_size
        
        return validation_result
    
    def create_risk_alert(self, alert_type: str, severity: str, message: str):
        """Create risk management alert"""
        now_iso = datetime.now().isoformat()
        
        self.protocol._db_execute("""
            INSERT INTO risk_alerts 
            (alert_type, severity, message, portfolio_value, current_drawdown, triggered_time)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            alert_type, severity, message,
            self.portfolio["total_capital"],
            self.portfolio["max_drawdown"],
            now_iso
        ), commit=True)
        
        print(f"🚨 RISK ALERT [{severity}]: {message}")
        
        # Log API usage for alert system
        self.protocol.log_api_usage("risk_manager", f"/alert/{alert_type}", 0.0, 0)
    
    def update_portfolio(self, positions_data: List[Dict]):
        """Update portfolio with current position data"""
        
        total_value = self.portfolio["total_capital"]
        allocated_value = 0
        unrealized_pnl = 0
        
        for position in positions_data:
            symbol = position["symbol"]
            current_value = position["quantity"] * position["current_price"]
            position_pnl = position.get("unrealized_pnl", 0)
            
            allocated_value += current_value
            unrealized_pnl += position_pnl
            
            # Update position in portfolio tracking
            self.portfolio["current_positions"][symbol] = {
                "quantity": position["quantity"],
                "entry_price": position["entry_price"],
                "current_price": position["current_price"],
                "current_value": current_value,
                "unrealized_pnl": position_pnl,
                "pnl_pct": (position_pnl / current_value) * 100 if current_value > 0 else 0
            }
        
        # Update portfolio metrics
        self.portfolio["allocated_capital"] = allocated_value
        self.portfolio["available_capital"] = total_value - allocated_value
        current_total = total_value + unrealized_pnl
        
        # Calculate drawdown
        if current_total < self.portfolio["total_capital"]:
            drawdown_pct = ((self.portfolio["total_capital"] - current_total) / self.portfolio["total_capital"]) * 100
            self.portfolio["max_drawdown"] = max(self.portfolio["max_drawdown"], drawdown_pct)
        
        # Check for risk alerts
        self._check_risk_thresholds()
        
        self.portfolio["last_updated"] = datetime.now().isoformat()
    
    def _check_risk_thresholds(self):
        """Check if any risk thresholds are breached"""
        
        # Check daily loss limit
        daily_loss_limit = self.portfolio["total_capital"] * (self.risk_parameters["max_daily_loss_pct"] / 100)
        if abs(self.portfolio["daily_pnl"]) >= (daily_loss_limit * 0.8):  # 80% warning threshold
            self.create_risk_alert(
                "daily_loss_warning",
                "HIGH",
                f"Daily loss approaching limit: ${abs(self.portfolio['daily_pnl']):.2f} / ${daily_loss_limit:.2f}"
            )
        
        # Check portfolio drawdown
        if self.portfolio["max_drawdown"] >= (self.risk_parameters["max_portfolio_drawdown_pct"] * 0.8):
            self.create_risk_alert(
                "drawdown_warning",
                "HIGH",
                f"Portfolio drawdown approaching limit: {self.portfolio['max_drawdown']:.1f}%"
            )
        
        # Check position concentration
        for symbol, position in self.portfolio["current_positions"].items():
            position_pct = (position["current_value"] / self.portfolio["total_capital"]) * 100
            if position_pct > (self.risk_parameters["max_position_size_pct"] * 1.2):  # 20% over limit
                self.create_risk_alert(
                    "position_concentration",
                    "MEDIUM",
                    f"{symbol} position size {position_pct:.1f}% exceeds recommended limit"
                )
    
    def generate_risk_report(self) -> Dict:
        """Generate comprehensive risk management report"""
        
        # Get recent alerts
        recent_alerts = self.protocol._db_execute("""
            SELECT * FROM risk_alerts 
            WHERE triggered_time >= datetime('now', '-7 days')
            ORDER BY triggered_time DESC
            LIMIT 10
        """)
        
        # Get recent performance
        recent_performance = self.protocol._db_execute("""
            SELECT * FROM daily_performance 
            ORDER BY date DESC 
            LIMIT 30
        """)
        
        # Calculate risk metrics
        risk_metrics = {
            "current_risk_level": "LOW",  # Will be calculated
            "capital_utilization": (self.portfolio["allocated_capital"] / self.portfolio["total_capital"]) * 100,
            "available_margin": self.portfolio["available_capital"],
            "max_drawdown": self.portfolio["max_drawdown"],
            "daily_pnl": self.portfolio["daily_pnl"],
            "open_positions": len(self.portfolio["current_positions"]),
            "risk_score": 0  # 0-100 scale
        }
        
        # Calculate risk score
        risk_score = 0
        if risk_metrics["capital_utilization"] > 80:
            risk_score += 30
        if risk_metrics["max_drawdown"] > 10:
            risk_score += 25
        if len(recent_alerts) > 3:
            risk_score += 20
        if risk_metrics["open_positions"] >= self.risk_parameters["max_open_positions"]:
            risk_score += 25
        
        risk_metrics["risk_score"] = min(risk_score, 100)
        
        if risk_score >= 70:
            risk_metrics["current_risk_level"] = "HIGH"
        elif risk_score >= 40:
            risk_metrics["current_risk_level"] = "MEDIUM"
        else:
            risk_metrics["current_risk_level"] = "LOW"
        
        return {
            "portfolio_summary": self.portfolio,
            "risk_parameters": self.risk_parameters,
            "risk_metrics": risk_metrics,
            "recent_alerts": recent_alerts,
            "recent_performance": recent_performance[:7],  # Last 7 days
            "recommendations": self._generate_risk_recommendations(risk_metrics)
        }
    
    def _generate_risk_recommendations(self, risk_metrics: Dict) -> List[str]:
        """Generate risk management recommendations"""
        recommendations = []
        
        if risk_metrics["capital_utilization"] > 80:
            recommendations.append("Consider reducing position sizes - high capital utilization")
        
        if risk_metrics["max_drawdown"] > 15:
            recommendations.append("Review trading strategy - significant drawdown detected")
        
        if risk_metrics["open_positions"] >= self.risk_parameters["max_open_positions"]:
            recommendations.append("Maximum position limit reached - avoid new trades")
        
        if risk_metrics["risk_score"] > 60:
            recommendations.append("Overall risk level elevated - consider defensive strategies")
        
        if len(recommendations) == 0:
            recommendations.append("Risk profile within acceptable parameters")
        
        return recommendations

def setup_risk_management_system():
    """Set up the complete risk management system"""
    print("🛡️ SETTING UP ORION RISK MANAGEMENT SYSTEM")
    print("=" * 60)
    
    # Initialize risk manager
    risk_manager = OrionRiskManager()
    
    # Test risk calculations
    print("\n�� TESTING RISK CALCULATIONS")
    print("-" * 40)
    
    # Test position size calculation
    test_position = risk_manager.calculate_position_size("BTC", 50000, 10000)
    print(f"📊 BTC Position Test:")
    print(f"   Entry Price: ${test_position['entry_price']:,}")
    print(f"   Recommended Size: {test_position['recommended_shares']} BTC")
    print(f"   Position Value: ${test_position['recommended_value']:,}")
    print(f"   Stop Loss: ${test_position['stop_loss_price']:,}")
    print(f"   Take Profit: ${test_position['take_profit_price']:,}")
    print(f"   Max Loss: ${test_position['max_loss']}")
    
    # Test trade validation
    test_trade = {
        "symbol": "BTC",
        "side": "buy",
        "quantity": 0.1,
        "price": 50000
    }
    
    validation = risk_manager.validate_trade(test_trade)
    print(f"\n✅ Trade Validation Test:")
    print(f"   Valid: {validation['valid']}")
    if validation["rejections"]:
        for rejection in validation["rejections"]:
            print(f"   ❌ {rejection}")
    if validation["recommendations"]:
        for rec in validation["recommendations"]:
            print(f"   �� {rec}")
    
    # Generate initial risk report
    print("\n📊 INITIAL RISK REPORT")
    print("-" * 40)
    
    risk_report = risk_manager.generate_risk_report()
    print(f"Risk Level: {risk_report['risk_metrics']['current_risk_level']}")
    print(f"Risk Score: {risk_report['risk_metrics']['risk_score']}/100")
    print(f"Capital Utilization: {risk_report['risk_metrics']['capital_utilization']:.1f}%")
    print(f"Available Margin: ${risk_report['risk_metrics']['available_margin']:,.2f}")
    
    return {
        "risk_manager": risk_manager,
        "system_ready": True,
        "test_results": {
            "position_calculation": test_position,
            "trade_validation": validation,
            "risk_report": risk_report
        }
    }

if __name__ == "__main__":
    result = setup_risk_management_system()
    print(f"\n🎯 Risk Management System Setup Complete!")
    print(f"✅ System Ready: {result['system_ready']}")
