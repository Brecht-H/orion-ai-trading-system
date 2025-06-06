"""
FILE: knowledge_center/llm_synthesis.py
PURPOSE: Synthesize research insights into actionable knowledge
CONTEXT: Part of Knowledge Center module - DO NOT DUPLICATE
DEPENDENCIES: Uses mistral:7b and qwen2:7b for synthesis
MAINTAIN: Single source of truth for knowledge synthesis

DO NOT:
- Create new synthesis files
- Move this functionality elsewhere
- Add trading execution here
- Skip the learning feedback loop

ONLY MODIFY:
- synthesize_insights() method
- generate_strategies() method
- update_knowledge_base() method
"""

import json
import sqlite3
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import logging
from pathlib import Path
import numpy as np
from dataclasses import dataclass, asdict
import chromadb
from chromadb.config import Settings

# Try to import ollama
try:
    import ollama
except ImportError:
    print("❌ Ollama not installed. Please run: pip install ollama chromadb")
    raise


@dataclass
class KnowledgeItem:
    """Structured knowledge representation"""
    id: str
    timestamp: float
    category: str  # market_pattern, strategy, risk_factor, etc.
    content: str
    confidence: float
    source: str
    metadata: Dict[str, Any]
    effectiveness_score: float = 0.0
    usage_count: int = 0
    last_used: Optional[float] = None


class KnowledgeSynthesis:
    """
    Intelligent knowledge synthesis that combines insights
    Uses LOCAL LLMs and vector storage for efficiency
    """
    
    def __init__(self):
        self.client = ollama.Client()
        self.setup_logging()
        self.setup_databases()
        
        # Initialize ChromaDB for vector storage
        self.setup_vector_store()
        
        # Knowledge categories
        self.categories = [
            "market_pattern",
            "trading_strategy", 
            "risk_factor",
            "correlation",
            "anomaly",
            "opportunity"
        ]
        
        # Track synthesis performance
        self.daily_synthesis_count = 0
        self.synthesis_quality_scores = []
        
    def setup_logging(self):
        """Setup logging for synthesis tracking"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - KnowledgeSynthesis - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_databases(self):
        """Setup knowledge databases"""
        Path("databases/sqlite_dbs").mkdir(parents=True, exist_ok=True)
        
        self.knowledge_db = "databases/sqlite_dbs/knowledge_base.db"
        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()
        
        # Knowledge items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_items (
                id TEXT PRIMARY KEY,
                timestamp REAL NOT NULL,
                category TEXT NOT NULL,
                content TEXT NOT NULL,
                confidence REAL NOT NULL,
                source TEXT NOT NULL,
                metadata TEXT NOT NULL,
                effectiveness_score REAL DEFAULT 0,
                usage_count INTEGER DEFAULT 0,
                last_used REAL
            )
        """)
        
        # Synthesis history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS synthesis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                input_insights TEXT NOT NULL,
                synthesized_knowledge TEXT NOT NULL,
                quality_score REAL DEFAULT 0,
                strategies_generated INTEGER DEFAULT 0,
                applied_to_trading BOOLEAN DEFAULT FALSE
            )
        """)
        
        # Strategy templates
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS strategy_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                conditions TEXT NOT NULL,
                actions TEXT NOT NULL,
                risk_parameters TEXT NOT NULL,
                backtest_results TEXT,
                live_performance TEXT,
                created_timestamp REAL NOT NULL,
                last_updated REAL NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
        
    def setup_vector_store(self):
        """Setup ChromaDB for semantic search of knowledge"""
        Path("knowledge_center/storage").mkdir(parents=True, exist_ok=True)
        
        self.chroma_client = chromadb.PersistentClient(
            path="knowledge_center/storage/chroma_db",
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Create or get collection
        try:
            self.knowledge_collection = self.chroma_client.create_collection(
                name="knowledge_vectors",
                metadata={"description": "Vectorized trading knowledge"}
            )
            self.logger.info("✅ Created new knowledge vector collection")
        except:
            self.knowledge_collection = self.chroma_client.get_collection("knowledge_vectors")
            self.logger.info("✅ Loaded existing knowledge vector collection")
            
    async def synthesize_insights(self, research_analysis: Dict[str, Any], 
                                 historical_context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Synthesize research insights into actionable knowledge
        Combines new insights with historical patterns
        """
        self.logger.info("🧠 Starting knowledge synthesis...")
        
        # Prepare synthesis prompt
        prompt = self._create_synthesis_prompt(research_analysis, historical_context)
        
        try:
            # Use different models for different aspects
            # Mistral for pattern recognition
            pattern_response = await self.client.generate(
                model='mistral:7b',
                prompt=f"{prompt}\n\nFocus on identifying PATTERNS and CORRELATIONS. Output as JSON.",
                format='json'
            )
            patterns = json.loads(pattern_response['response'])
            
            # Qwen for strategy generation (if available)
            try:
                strategy_response = await self.client.generate(
                    model='qwen2:7b',
                    prompt=f"{prompt}\n\nFocus on generating TRADING STRATEGIES based on the patterns. Output as JSON.",
                    format='json'
                )
                strategies = json.loads(strategy_response['response'])
            except:
                # Fallback to mistral
                strategy_response = await self.client.generate(
                    model='mistral:7b',
                    prompt=f"{prompt}\n\nGenerate simple TRADING STRATEGIES. Output as JSON.",
                    format='json'
                )
                strategies = json.loads(strategy_response['response'])
            
            # Combine insights
            synthesized_knowledge = {
                'timestamp': datetime.now().isoformat(),
                'patterns_identified': patterns.get('patterns', []),
                'strategies_generated': strategies.get('strategies', []),
                'risk_factors': patterns.get('risks', []),
                'confidence_level': self._calculate_confidence(patterns, strategies),
                'recommended_actions': self._generate_recommendations(patterns, strategies)
            }
            
            # Store in vector database for retrieval
            await self._store_knowledge_vectors(synthesized_knowledge)
            
            # Store synthesis history
            await self._store_synthesis_history(research_analysis, synthesized_knowledge)
            
            self.daily_synthesis_count += 1
            self.logger.info(f"✅ Synthesis complete. Generated {len(strategies.get('strategies', []))} strategies")
            
            return {
                'success': True,
                'knowledge': synthesized_knowledge,
                'quality_score': synthesized_knowledge['confidence_level']
            }
            
        except Exception as e:
            self.logger.error(f"❌ Synthesis failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'fallback': self._get_fallback_synthesis(research_analysis)
            }
            
    def _create_synthesis_prompt(self, research_analysis: Dict, historical_context: Optional[Dict]) -> str:
        """Create comprehensive prompt for synthesis"""
        prompt_parts = [
            "You are an expert trading strategist synthesizing market insights.",
            "\nCURRENT MARKET ANALYSIS:",
            json.dumps(research_analysis.get('analysis', {}), indent=2)
        ]
        
        if historical_context:
            prompt_parts.extend([
                "\nHISTORICAL CONTEXT:",
                f"Similar patterns occurred: {historical_context.get('pattern_count', 0)} times",
                f"Average outcome: {historical_context.get('avg_outcome', 'unknown')}"
            ])
            
        prompt_parts.extend([
            "\nSYNTHESIZE this information to:",
            "1. Identify reliable patterns",
            "2. Generate actionable trading strategies",
            "3. Assess risk factors",
            "4. Recommend specific actions",
            "\nBe specific, practical, and risk-aware."
        ])
        
        return "\n".join(prompt_parts)
        
    async def generate_strategies(self, knowledge: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate specific trading strategies from synthesized knowledge
        """
        strategies = []
        
        for pattern in knowledge.get('patterns_identified', []):
            prompt = f"""Based on this market pattern: {pattern}
            
Generate a specific trading strategy in JSON format:
{{
    "name": "strategy name",
    "entry_conditions": ["condition1", "condition2"],
    "exit_conditions": ["condition1", "condition2"],
    "position_size": "percentage or calculation",
    "stop_loss": "percentage or price level",
    "take_profit": "percentage or price level",
    "time_horizon": "minutes/hours/days",
    "confidence": 0.0-1.0
}}

Be specific with numbers and conditions."""

            try:
                response = await self.client.generate(
                    model='mistral:7b',
                    prompt=prompt,
                    format='json'
                )
                
                strategy = json.loads(response['response'])
                strategy['pattern_basis'] = pattern
                strategy['generated_at'] = datetime.now().isoformat()
                
                strategies.append(strategy)
                
                # Store as template if high confidence
                if strategy.get('confidence', 0) > 0.7:
                    await self._store_strategy_template(strategy)
                    
            except Exception as e:
                self.logger.error(f"Strategy generation error: {e}")
                
        return strategies
        
    async def _store_knowledge_vectors(self, knowledge: Dict[str, Any]):
        """Store knowledge in vector database for semantic search"""
        # Create knowledge items
        items = []
        
        # Store patterns
        for pattern in knowledge.get('patterns_identified', []):
            item = KnowledgeItem(
                id=f"pattern_{datetime.now().timestamp()}_{hash(pattern)}",
                timestamp=datetime.now().timestamp(),
                category="market_pattern",
                content=pattern,
                confidence=knowledge.get('confidence_level', 0.5),
                source="synthesis",
                metadata={"synthesis_timestamp": knowledge['timestamp']}
            )
            items.append(item)
            
        # Store strategies
        for strategy in knowledge.get('strategies_generated', []):
            item = KnowledgeItem(
                id=f"strategy_{datetime.now().timestamp()}_{hash(str(strategy))}",
                timestamp=datetime.now().timestamp(),
                category="trading_strategy",
                content=json.dumps(strategy),
                confidence=strategy.get('confidence', 0.5),
                source="synthesis",
                metadata={"pattern_basis": strategy.get('pattern_basis', '')}
            )
            items.append(item)
            
        # Add to vector store
        if items:
            self.knowledge_collection.add(
                ids=[item.id for item in items],
                documents=[item.content for item in items],
                metadatas=[{"category": item.category, "confidence": item.confidence} for item in items]
            )
            
            # Also store in SQL for structured queries
            conn = sqlite3.connect(self.knowledge_db)
            cursor = conn.cursor()
            
            for item in items:
                cursor.execute("""
                    INSERT OR REPLACE INTO knowledge_items
                    (id, timestamp, category, content, confidence, source, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    item.id,
                    item.timestamp,
                    item.category,
                    item.content,
                    item.confidence,
                    item.source,
                    json.dumps(item.metadata)
                ))
                
            conn.commit()
            conn.close()
            
    async def _store_synthesis_history(self, input_data: Dict, output_knowledge: Dict):
        """Store synthesis history for learning"""
        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO synthesis_history
            (timestamp, input_insights, synthesized_knowledge, quality_score, strategies_generated)
            VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.now().timestamp(),
            json.dumps(input_data),
            json.dumps(output_knowledge),
            output_knowledge.get('confidence_level', 0),
            len(output_knowledge.get('strategies_generated', []))
        ))
        
        conn.commit()
        conn.close()
        
    async def _store_strategy_template(self, strategy: Dict[str, Any]):
        """Store high-confidence strategies as templates"""
        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO strategy_templates
            (name, conditions, actions, risk_parameters, created_timestamp, last_updated)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            strategy.get('name', 'Unnamed Strategy'),
            json.dumps(strategy.get('entry_conditions', [])),
            json.dumps({
                'entry': strategy.get('entry_conditions', []),
                'exit': strategy.get('exit_conditions', [])
            }),
            json.dumps({
                'stop_loss': strategy.get('stop_loss', '2%'),
                'take_profit': strategy.get('take_profit', '5%'),
                'position_size': strategy.get('position_size', '5%')
            }),
            datetime.now().timestamp(),
            datetime.now().timestamp()
        ))
        
        conn.commit()
        conn.close()
        
    def _calculate_confidence(self, patterns: Dict, strategies: Dict) -> float:
        """Calculate overall confidence in synthesized knowledge"""
        confidence_factors = []
        
        # Pattern confidence
        if patterns.get('confidence'):
            confidence_factors.append(patterns['confidence'])
            
        # Strategy confidence
        for strategy in strategies.get('strategies', []):
            if isinstance(strategy, dict) and strategy.get('confidence'):
                confidence_factors.append(strategy['confidence'])
                
        # Historical performance factor
        # (would check past performance of similar patterns)
        
        return np.mean(confidence_factors) if confidence_factors else 0.5
        
    def _generate_recommendations(self, patterns: Dict, strategies: Dict) -> List[str]:
        """Generate specific action recommendations"""
        recommendations = []
        
        # Based on patterns
        if patterns.get('market_trend') == 'bullish':
            recommendations.append("Consider increasing long positions gradually")
        elif patterns.get('market_trend') == 'bearish':
            recommendations.append("Reduce exposure and tighten stop losses")
            
        # Based on confidence
        confidence = self._calculate_confidence(patterns, strategies)
        if confidence > 0.8:
            recommendations.append("High confidence - consider larger position sizes")
        elif confidence < 0.3:
            recommendations.append("Low confidence - wait for clearer signals")
            
        # Risk-based recommendations
        if patterns.get('volatility', 'normal') == 'high':
            recommendations.append("High volatility detected - reduce position sizes")
            
        return recommendations
        
    def _get_fallback_synthesis(self, research_analysis: Dict) -> Dict[str, Any]:
        """Simple rule-based synthesis when LLM fails"""
        sentiment = research_analysis.get('analysis', {}).get('market_sentiment', 'neutral')
        
        basic_synthesis = {
            'patterns_identified': [f"Market appears {sentiment}"],
            'strategies_generated': [{
                'name': f'Basic {sentiment} strategy',
                'entry_conditions': ['Wait for confirmation'],
                'exit_conditions': ['Stop loss at 2%'],
                'confidence': 0.3
            }],
            'risk_factors': ['Operating without AI synthesis'],
            'confidence_level': 0.3,
            'recommended_actions': ['Proceed with caution', 'Manual analysis recommended']
        }
        
        return basic_synthesis
        
    async def search_similar_knowledge(self, query: str, category: Optional[str] = None) -> List[Dict]:
        """Search vector store for similar knowledge"""
        try:
            results = self.knowledge_collection.query(
                query_texts=[query],
                n_results=5,
                where={"category": category} if category else None
            )
            
            return [{
                'id': results['ids'][0][i],
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            } for i in range(len(results['ids'][0]))]
            
        except Exception as e:
            self.logger.error(f"Vector search error: {e}")
            return []
            
    async def update_knowledge_effectiveness(self, knowledge_id: str, 
                                           outcome: Dict[str, Any]) -> bool:
        """Update knowledge item based on real-world performance"""
        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()
        
        # Calculate effectiveness score
        profit = outcome.get('profit_loss', 0)
        effectiveness = 1.0 if profit > 0 else 0.3
        
        cursor.execute("""
            UPDATE knowledge_items
            SET effectiveness_score = (effectiveness_score * usage_count + ?) / (usage_count + 1),
                usage_count = usage_count + 1,
                last_used = ?
            WHERE id = ?
        """, (effectiveness, datetime.now().timestamp(), knowledge_id))
        
        conn.commit()
        conn.close()
        
        return True


# Example usage
async def main():
    """Test the knowledge synthesis system"""
    synthesizer = KnowledgeSynthesis()
    
    # Sample research analysis output
    research_analysis = {
        'analysis': {
            'market_sentiment': 'bullish',
            'key_insights': [
                'BTC showing strong support at $50k',
                'Institutional buying increasing',
                'Fear & Greed index at 65 (greed)'
            ],
            'risk_factors': ['Potential resistance at $55k'],
            'opportunities': ['Breakout possible above $55k'],
            'confidence': 0.75
        }
    }
    
    # Synthesize knowledge
    print("🧠 Synthesizing market insights...")
    result = await synthesizer.synthesize_insights(research_analysis)
    
    if result['success']:
        print("\n✅ Knowledge Synthesis Complete:")
        knowledge = result['knowledge']
        print(f"   Patterns: {len(knowledge['patterns_identified'])}")
        print(f"   Strategies: {len(knowledge['strategies_generated'])}")
        print(f"   Confidence: {knowledge['confidence_level']:.2%}")
        
        # Generate detailed strategies
        print("\n📊 Generating detailed strategies...")
        strategies = await synthesizer.generate_strategies(knowledge)
        
        for i, strategy in enumerate(strategies, 1):
            print(f"\n   Strategy {i}: {strategy.get('name', 'Unnamed')}")
            print(f"   Confidence: {strategy.get('confidence', 0):.2%}")
            print(f"   Entry: {strategy.get('entry_conditions', [])}")
            
        # Search for similar knowledge
        print("\n🔍 Searching for similar patterns...")
        similar = await synthesizer.search_similar_knowledge(
            "bullish breakout pattern",
            category="market_pattern"
        )
        print(f"   Found {len(similar)} similar patterns")
    else:
        print(f"❌ Synthesis failed: {result['error']}")


if __name__ == "__main__":
    asyncio.run(main())