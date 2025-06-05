#!/usr/bin/env python3
"""
🔄 INTELLIGENCE TO ACTION PIPELINE
Converts knowledge insights into automated system improvements and profit generation
FORTUNE IMPACT: Continuous system optimization, automated strategy improvements
"""

import asyncio
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging
from dataclasses import dataclass
from enum import Enum
import hashlib

class ActionPriority(Enum):
    IMMEDIATE = "immediate"      # Auto-implement within minutes
    HIGH = "high"               # CEO approval within hours
    MEDIUM = "medium"           # CEO approval within days
    LOW = "low"                 # Store for future reference

class ActionType(Enum):
    STRATEGY_OPTIMIZATION = "strategy_optimization"
    RISK_ADJUSTMENT = "risk_adjustment"
    POSITION_SIZING = "position_sizing"
    MARKET_TIMING = "market_timing"
    SYSTEM_CONFIGURATION = "system_configuration"
    ALERT_SETUP = "alert_setup"

@dataclass
class KnowledgeInsight:
    insight_id: str
    content: str
    source: str
    insight_type: str
    confidence: float
    profit_potential: float
    risk_level: float
    time_sensitivity: int  # hours
    supporting_data: Dict[str, Any]
    created_at: datetime

@dataclass
class SystemAction:
    action_id: str
    action_type: ActionType
    priority: ActionPriority
    description: str
    implementation_details: Dict[str, Any]
    expected_impact: float
    risk_assessment: str
    auto_implementable: bool
    requires_approval: bool
    target_component: str
    profit_potential: float
    created_at: datetime
    status: str = "pending"

@dataclass
class PerformanceCorrelation:
    correlation_id: str
    insight_id: str
    action_id: str
    profit_generated: float
    accuracy_score: float
    implementation_time: float
    success_indicators: Dict[str, Any]
    lessons_learned: str
    created_at: datetime

class IntelligenceToActionPipeline:
    """
    Converts knowledge insights into automated system improvements and profit generation
    
    Core Capabilities:
    - Insight impact assessment and prioritization
    - Automated low-risk improvement implementation
    - CEO approval queue for high-impact changes
    - Performance correlation tracking
    - Knowledge → profit optimization
    """
    
    def __init__(self):
        self.pipeline_id = "intelligence_action_pipeline_001"
        self.db_path = "databases/sqlite_dbs/decision_pipeline.db"
        self.setup_database()
        self.setup_logging()
        
        # Action implementation thresholds
        self.auto_implementation_thresholds = {
            'min_confidence': 0.8,
            'max_risk': 0.3,
            'min_profit_potential': 0.1,
            'max_impact_without_approval': 0.5
        }
        
        # Component integration points
        self.component_integrations = {
            'strategy_center': 'strategy_center/optimization/auto_optimizer.py',
            'risk_management': 'risk_management_center/core/dynamic_risk_manager.py',
            'trading_execution': 'trading_execution_center/core/execution_optimizer.py',
            'technical_analysis': 'technical_analysis_center/core/indicator_optimizer.py',
            'notion_dashboard': 'notion_integration_hub/core/ceo_approval_queue.py'
        }
        
        # Performance tracking
        self.performance_metrics = {
            'total_insights_processed': 0,
            'auto_implementations': 0,
            'ceo_approvals_queued': 0,
            'profit_generated': 0.0,
            'accuracy_rate': 0.0,
            'avg_response_time': 0.0
        }
        
    def setup_database(self):
        """Setup decision pipeline database"""
        Path("databases/sqlite_dbs").mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Knowledge insights table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_insights (
                insight_id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                source TEXT NOT NULL,
                insight_type TEXT NOT NULL,
                confidence REAL NOT NULL,
                profit_potential REAL NOT NULL,
                risk_level REAL NOT NULL,
                time_sensitivity INTEGER NOT NULL,
                supporting_data TEXT NOT NULL,
                created_at REAL NOT NULL,
                processed BOOLEAN DEFAULT FALSE
            )
        """)
        
        # System actions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_actions (
                action_id TEXT PRIMARY KEY,
                action_type TEXT NOT NULL,
                priority TEXT NOT NULL,
                description TEXT NOT NULL,
                implementation_details TEXT NOT NULL,
                expected_impact REAL NOT NULL,
                risk_assessment TEXT NOT NULL,
                auto_implementable BOOLEAN NOT NULL,
                requires_approval BOOLEAN NOT NULL,
                target_component TEXT NOT NULL,
                profit_potential REAL NOT NULL,
                created_at REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                implemented_at REAL,
                implementation_result TEXT
            )
        """)
        
        # Performance correlations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance_correlations (
                correlation_id TEXT PRIMARY KEY,
                insight_id TEXT NOT NULL,
                action_id TEXT NOT NULL,
                profit_generated REAL NOT NULL,
                accuracy_score REAL NOT NULL,
                implementation_time REAL NOT NULL,
                success_indicators TEXT NOT NULL,
                lessons_learned TEXT NOT NULL,
                created_at REAL NOT NULL
            )
        """)
        
        # CEO approval queue table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ceo_approval_queue (
                queue_id TEXT PRIMARY KEY,
                action_id TEXT NOT NULL,
                insight_summary TEXT NOT NULL,
                profit_potential REAL NOT NULL,
                risk_assessment TEXT NOT NULL,
                recommendation TEXT NOT NULL,
                urgency_level TEXT NOT NULL,
                created_at REAL NOT NULL,
                approved_at REAL,
                approval_status TEXT DEFAULT 'pending',
                ceo_feedback TEXT
            )
        """)
        
        # Pipeline performance table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pipeline_performance (
                performance_id TEXT PRIMARY KEY,
                date_tracked DATE NOT NULL,
                insights_processed INTEGER NOT NULL,
                auto_implementations INTEGER NOT NULL,
                ceo_approvals INTEGER NOT NULL,
                profit_generated REAL NOT NULL,
                accuracy_rate REAL NOT NULL,
                avg_response_time REAL NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
        
    def setup_logging(self):
        """Setup pipeline logging"""
        Path("logs/knowledge_center").mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - IntelligenceActionPipeline - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/knowledge_center/intelligence_action_pipeline.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"🔄 Intelligence to Action Pipeline {self.pipeline_id} initialized")
    
    async def process_insight(self, insight: KnowledgeInsight) -> Dict[str, Any]:
        """Main processing function - converts insight into action"""
        self.logger.info(f"📥 Processing insight: {insight.insight_id}")
        
        try:
            # 1. Store insight for tracking
            self.store_insight(insight)
            
            # 2. Assess profit potential and impact
            impact_assessment = await self.assess_profit_potential(insight)
            
            # 3. Generate system actions
            actions = await self.generate_system_actions(insight, impact_assessment)
            
            # 4. Route actions based on priority and risk
            routing_results = await self.route_actions(actions)
            
            # 5. Track performance correlation
            await self.track_knowledge_to_profit_correlation(insight, actions)
            
            result = {
                'insight_id': insight.insight_id,
                'impact_assessment': impact_assessment,
                'actions_generated': len(actions),
                'auto_implemented': routing_results['auto_implemented'],
                'queued_for_approval': routing_results['queued_for_approval'],
                'expected_profit': sum(a.profit_potential for a in actions),
                'processing_time': routing_results['processing_time']
            }
            
            self.logger.info(f"✅ Insight processed successfully")
            self.logger.info(f"   Actions generated: {len(actions)}")
            self.logger.info(f"   Auto-implemented: {routing_results['auto_implemented']}")
            self.logger.info(f"   Expected profit: ${result['expected_profit']:.2f}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Insight processing failed: {e}")
            return {'error': str(e), 'insight_id': insight.insight_id}
    
    async def assess_profit_potential(self, insight: KnowledgeInsight) -> Dict[str, Any]:
        """Assess the profit potential and impact of an insight"""
        
        # Base profit calculation
        base_profit = insight.profit_potential * insight.confidence
        
        # Time sensitivity multiplier
        time_multiplier = 1.0
        if insight.time_sensitivity <= 24:
            time_multiplier = 1.5  # High urgency bonus
        elif insight.time_sensitivity <= 72:
            time_multiplier = 1.2  # Medium urgency bonus
        
        # Risk adjustment
        risk_adjustment = 1.0 - (insight.risk_level * 0.5)
        
        # Calculate final profit score
        profit_score = base_profit * time_multiplier * risk_adjustment
        
        assessment = {
            'profit_score': profit_score,
            'base_profit': base_profit,
            'time_multiplier': time_multiplier,
            'risk_adjustment': risk_adjustment,
            'implementation_urgency': self.calculate_urgency(insight),
            'impact_category': self.categorize_impact(profit_score),
            'recommended_action': self.recommend_action_level(profit_score, insight.risk_level)
        }
        
        return assessment
    
    async def generate_system_actions(self, insight: KnowledgeInsight, impact_assessment: Dict[str, Any]) -> List[SystemAction]:
        """Generate specific system actions based on insight"""
        actions = []
        
        # Determine action types based on insight type
        if insight.insight_type == 'market_opportunity':
            actions.extend(await self.generate_market_opportunity_actions(insight, impact_assessment))
        elif insight.insight_type == 'risk_signal':
            actions.extend(await self.generate_risk_management_actions(insight, impact_assessment))
        elif insight.insight_type == 'strategy_improvement':
            actions.extend(await self.generate_strategy_optimization_actions(insight, impact_assessment))
        elif insight.insight_type == 'technical_signal':
            actions.extend(await self.generate_technical_analysis_actions(insight, impact_assessment))
        else:
            # Generic action generation
            actions.extend(await self.generate_generic_actions(insight, impact_assessment))
        
        return actions
    
    async def generate_market_opportunity_actions(self, insight: KnowledgeInsight, assessment: Dict[str, Any]) -> List[SystemAction]:
        """Generate actions for market opportunity insights"""
        actions = []
        
        # Position sizing adjustment
        if assessment['profit_score'] > 0.7:
            action = SystemAction(
                action_id=f"pos_size_{insight.insight_id}",
                action_type=ActionType.POSITION_SIZING,
                priority=ActionPriority.HIGH,
                description=f"Increase position sizing for {insight.source} opportunity",
                implementation_details={
                    'current_size': '2%',
                    'recommended_size': '4%',
                    'reason': f"High profit potential detected: {assessment['profit_score']:.2f}"
                },
                expected_impact=assessment['profit_score'],
                risk_assessment=f"Medium risk - based on {insight.confidence:.2f} confidence",
                auto_implementable=insight.confidence > 0.8 and insight.risk_level < 0.4,
                requires_approval=assessment['profit_score'] > 0.5,
                target_component='risk_management',
                profit_potential=assessment['profit_score'] * 10000,  # Estimated profit in USD
                created_at=datetime.now()
            )
            actions.append(action)
        
        # Market timing alerts
        if insight.time_sensitivity <= 48:
            action = SystemAction(
                action_id=f"timing_alert_{insight.insight_id}",
                action_type=ActionType.ALERT_SETUP,
                priority=ActionPriority.IMMEDIATE,
                description=f"Setup time-sensitive alerts for {insight.source}",
                implementation_details={
                    'alert_type': 'price_movement',
                    'threshold': '3%',
                    'time_window': f"{insight.time_sensitivity}h"
                },
                expected_impact=0.3,
                risk_assessment="Low risk - alert setup only",
                auto_implementable=True,
                requires_approval=False,
                target_component='technical_analysis',
                profit_potential=2000,  # Estimated profit from early alert
                created_at=datetime.now()
            )
            actions.append(action)
        
        return actions
    
    async def generate_risk_management_actions(self, insight: KnowledgeInsight, assessment: Dict[str, Any]) -> List[SystemAction]:
        """Generate actions for risk management insights"""
        actions = []
        
        # Dynamic stop-loss adjustment
        if insight.risk_level > 0.6:
            action = SystemAction(
                action_id=f"stop_loss_{insight.insight_id}",
                action_type=ActionType.RISK_ADJUSTMENT,
                priority=ActionPriority.HIGH,
                description=f"Tighten stop-loss based on {insight.source} risk signal",
                implementation_details={
                    'current_stop': '5%',
                    'recommended_stop': '3%',
                    'reason': f"Elevated risk detected: {insight.risk_level:.2f}"
                },
                expected_impact=0.4,
                risk_assessment="Low risk - protective measure",
                auto_implementable=True,
                requires_approval=False,
                target_component='risk_management',
                profit_potential=5000,  # Capital preservation value
                created_at=datetime.now()
            )
            actions.append(action)
        
        return actions
    
    async def generate_strategy_optimization_actions(self, insight: KnowledgeInsight, assessment: Dict[str, Any]) -> List[SystemAction]:
        """Generate actions for strategy optimization insights"""
        actions = []
        
        # Parameter optimization
        if assessment['profit_score'] > 0.6:
            action = SystemAction(
                action_id=f"strategy_opt_{insight.insight_id}",
                action_type=ActionType.STRATEGY_OPTIMIZATION,
                priority=ActionPriority.MEDIUM,
                description=f"Optimize strategy parameters based on {insight.source}",
                implementation_details={
                    'optimization_type': 'parameter_tuning',
                    'target_strategies': ['momentum_breakout', 'mean_reversion'],
                    'expected_improvement': f"{assessment['profit_score']*10:.1f}%"
                },
                expected_impact=assessment['profit_score'],
                risk_assessment="Medium risk - strategy modification",
                auto_implementable=assessment['profit_score'] < 0.5,
                requires_approval=assessment['profit_score'] >= 0.5,
                target_component='strategy_center',
                profit_potential=assessment['profit_score'] * 15000,
                created_at=datetime.now()
            )
            actions.append(action)
        
        return actions
    
    async def generate_technical_analysis_actions(self, insight: KnowledgeInsight, assessment: Dict[str, Any]) -> List[SystemAction]:
        """Generate actions for technical analysis insights"""
        actions = []
        
        # Indicator weight adjustment
        action = SystemAction(
            action_id=f"indicator_adj_{insight.insight_id}",
            action_type=ActionType.SYSTEM_CONFIGURATION,
            priority=ActionPriority.LOW,
            description=f"Adjust indicator weights based on {insight.source}",
            implementation_details={
                'indicator_type': 'momentum',
                'current_weight': 0.3,
                'recommended_weight': 0.4,
                'reason': f"Technical pattern strength: {insight.confidence:.2f}"
            },
            expected_impact=0.2,
            risk_assessment="Low risk - weight adjustment",
            auto_implementable=True,
            requires_approval=False,
            target_component='technical_analysis',
            profit_potential=3000,
            created_at=datetime.now()
        )
        actions.append(action)
        
        return actions
    
    async def generate_generic_actions(self, insight: KnowledgeInsight, assessment: Dict[str, Any]) -> List[SystemAction]:
        """Generate generic actions for unknown insight types"""
        actions = []
        
        # Generic monitoring action
        action = SystemAction(
            action_id=f"monitor_{insight.insight_id}",
            action_type=ActionType.ALERT_SETUP,
            priority=ActionPriority.LOW,
            description=f"Monitor {insight.source} for follow-up signals",
            implementation_details={
                'monitoring_type': 'general',
                'duration': '7d',
                'sensitivity': 'medium'
            },
            expected_impact=0.1,
            risk_assessment="No risk - monitoring only",
            auto_implementable=True,
            requires_approval=False,
            target_component='research_center',
            profit_potential=1000,
            created_at=datetime.now()
        )
        actions.append(action)
        
        return actions
    
    async def route_actions(self, actions: List[SystemAction]) -> Dict[str, Any]:
        """Route actions based on priority and risk"""
        auto_implemented = 0
        queued_for_approval = 0
        start_time = datetime.now()
        
        for action in actions:
            # Store action in database
            self.store_action(action)
            
            if action.auto_implementable and not action.requires_approval:
                # Auto-implement low-risk actions
                await self.implement_immediate_improvement(action)
                auto_implemented += 1
            elif action.requires_approval or action.expected_impact > 0.5:
                # Queue for CEO approval
                await self.queue_for_ceo_approval(action)
                queued_for_approval += 1
            else:
                # Store for future reference
                await self.store_for_future_reference(action)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            'auto_implemented': auto_implemented,
            'queued_for_approval': queued_for_approval,
            'stored_for_future': len(actions) - auto_implemented - queued_for_approval,
            'processing_time': processing_time
        }
    
    async def implement_immediate_improvement(self, action: SystemAction):
        """Implement low-risk improvements immediately"""
        self.logger.info(f"⚡ Auto-implementing action: {action.action_id}")
        
        try:
            # Mock implementation - would integrate with actual system components
            implementation_result = {
                'status': 'success',
                'timestamp': datetime.now(),
                'component': action.target_component,
                'details': action.implementation_details
            }
            
            # Update action status
            self.update_action_status(action.action_id, 'implemented', implementation_result)
            
            self.logger.info(f"✅ Action implemented successfully: {action.description}")
            
        except Exception as e:
            self.logger.error(f"❌ Auto-implementation failed: {e}")
            self.update_action_status(action.action_id, 'failed', {'error': str(e)})
    
    async def queue_for_ceo_approval(self, action: SystemAction):
        """Queue high-impact actions for CEO approval"""
        self.logger.info(f"📋 Queuing for CEO approval: {action.action_id}")
        
        try:
            # Create approval queue entry
            queue_entry = {
                'queue_id': f"ceo_approval_{action.action_id}",
                'action_id': action.action_id,
                'insight_summary': action.description,
                'profit_potential': action.profit_potential,
                'risk_assessment': action.risk_assessment,
                'recommendation': self.generate_ceo_recommendation(action),
                'urgency_level': action.priority.value,
                'created_at': datetime.now().timestamp()
            }
            
            # Store in CEO approval queue
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO ceo_approval_queue 
                (queue_id, action_id, insight_summary, profit_potential, risk_assessment, 
                 recommendation, urgency_level, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                queue_entry['queue_id'],
                queue_entry['action_id'],
                queue_entry['insight_summary'],
                queue_entry['profit_potential'],
                queue_entry['risk_assessment'],
                queue_entry['recommendation'],
                queue_entry['urgency_level'],
                queue_entry['created_at']
            ))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"✅ Action queued for CEO approval")
            
        except Exception as e:
            self.logger.error(f"❌ CEO queue failed: {e}")
    
    async def store_for_future_reference(self, action: SystemAction):
        """Store actions for future reference"""
        self.logger.info(f"📁 Storing for future reference: {action.action_id}")
        self.update_action_status(action.action_id, 'stored', {'reason': 'low_priority'})
    
    async def track_knowledge_to_profit_correlation(self, insight: KnowledgeInsight, actions: List[SystemAction]):
        """Track correlation between knowledge and profit generation"""
        try:
            total_expected_profit = sum(a.profit_potential for a in actions)
            
            correlation = PerformanceCorrelation(
                correlation_id=f"corr_{insight.insight_id}",
                insight_id=insight.insight_id,
                action_id=f"batch_{len(actions)}",
                profit_generated=0.0,  # Will be updated when realized
                accuracy_score=insight.confidence,
                implementation_time=0.0,  # Will be updated
                success_indicators={
                    'expected_profit': total_expected_profit,
                    'actions_count': len(actions),
                    'confidence': insight.confidence
                },
                lessons_learned="Initial correlation tracking",
                created_at=datetime.now()
            )
            
            self.store_correlation(correlation)
            
        except Exception as e:
            self.logger.error(f"❌ Correlation tracking failed: {e}")
    
    def calculate_urgency(self, insight: KnowledgeInsight) -> str:
        """Calculate implementation urgency"""
        if insight.time_sensitivity <= 6:
            return "CRITICAL"
        elif insight.time_sensitivity <= 24:
            return "HIGH"
        elif insight.time_sensitivity <= 72:
            return "MEDIUM"
        else:
            return "LOW"
    
    def categorize_impact(self, profit_score: float) -> str:
        """Categorize impact level"""
        if profit_score >= 0.8:
            return "HIGH_IMPACT"
        elif profit_score >= 0.5:
            return "MEDIUM_IMPACT"
        elif profit_score >= 0.2:
            return "LOW_IMPACT"
        else:
            return "MINIMAL_IMPACT"
    
    def recommend_action_level(self, profit_score: float, risk_level: float) -> str:
        """Recommend action level"""
        if profit_score > 0.7 and risk_level < 0.4:
            return "AUTO_IMPLEMENT"
        elif profit_score > 0.5:
            return "CEO_APPROVAL"
        elif profit_score > 0.2:
            return "MONITOR"
        else:
            return "STORE"
    
    def generate_ceo_recommendation(self, action: SystemAction) -> str:
        """Generate CEO recommendation text"""
        return f"RECOMMENDATION: {action.priority.value.upper()} priority action with ${action.profit_potential:.0f} profit potential. Risk level: {action.risk_assessment}. Suggested implementation: {action.description}"
    
    def store_insight(self, insight: KnowledgeInsight):
        """Store insight in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO knowledge_insights 
            (insight_id, content, source, insight_type, confidence, profit_potential, 
             risk_level, time_sensitivity, supporting_data, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            insight.insight_id,
            insight.content,
            insight.source,
            insight.insight_type,
            insight.confidence,
            insight.profit_potential,
            insight.risk_level,
            insight.time_sensitivity,
            json.dumps(insight.supporting_data),
            insight.created_at.timestamp()
        ))
        
        conn.commit()
        conn.close()
    
    def store_action(self, action: SystemAction):
        """Store action in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO system_actions 
            (action_id, action_type, priority, description, implementation_details, 
             expected_impact, risk_assessment, auto_implementable, requires_approval, 
             target_component, profit_potential, created_at, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            action.action_id,
            action.action_type.value,
            action.priority.value,
            action.description,
            json.dumps(action.implementation_details),
            action.expected_impact,
            action.risk_assessment,
            action.auto_implementable,
            action.requires_approval,
            action.target_component,
            action.profit_potential,
            action.created_at.timestamp(),
            action.status
        ))
        
        conn.commit()
        conn.close()
    
    def store_correlation(self, correlation: PerformanceCorrelation):
        """Store performance correlation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO performance_correlations 
            (correlation_id, insight_id, action_id, profit_generated, accuracy_score, 
             implementation_time, success_indicators, lessons_learned, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            correlation.correlation_id,
            correlation.insight_id,
            correlation.action_id,
            correlation.profit_generated,
            correlation.accuracy_score,
            correlation.implementation_time,
            json.dumps(correlation.success_indicators),
            correlation.lessons_learned,
            correlation.created_at.timestamp()
        ))
        
        conn.commit()
        conn.close()
    
    def update_action_status(self, action_id: str, status: str, result: Dict[str, Any]):
        """Update action status and result"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE system_actions 
            SET status = ?, implemented_at = ?, implementation_result = ?
            WHERE action_id = ?
        """, (
            status,
            datetime.now().timestamp(),
            json.dumps(result),
            action_id
        ))
        
        conn.commit()
        conn.close()

# Test and demonstration function
async def main():
    """Test the Intelligence to Action Pipeline"""
    print("🔄 ORION Intelligence to Action Pipeline - Test Run")
    print("=" * 60)
    
    pipeline = IntelligenceToActionPipeline()
    
    # Create test insight
    test_insight = KnowledgeInsight(
        insight_id="test_insight_001",
        content="Regulatory approval signal detected for Bitcoin ETF with 85% confidence",
        source="Market Intelligence Hunter",
        insight_type="market_opportunity",
        confidence=0.85,
        profit_potential=0.8,
        risk_level=0.3,
        time_sensitivity=24,
        supporting_data={
            'sources': ['federal_register', 'sec_filings'],
            'signal_strength': 0.85,
            'market_impact': 0.8
        },
        created_at=datetime.now()
    )
    
    # Process insight
    result = await pipeline.process_insight(test_insight)
    
    print(f"\n📊 PROCESSING RESULTS:")
    print(f"   Insight ID: {result.get('insight_id')}")
    print(f"   Actions generated: {result.get('actions_generated')}")
    print(f"   Auto-implemented: {result.get('auto_implemented')}")
    print(f"   Queued for approval: {result.get('queued_for_approval')}")
    print(f"   Expected profit: ${result.get('expected_profit', 0):.2f}")
    print(f"   Processing time: {result.get('processing_time', 0):.3f}s")

if __name__ == "__main__":
    asyncio.run(main()) 