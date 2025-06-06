"""
FILE: research_center/llm_analyzer.py
PURPOSE: Intelligent market data analysis using LLMs
CONTEXT: Part of Research Center module - DO NOT DUPLICATE
DEPENDENCIES: Uses mistral:7b for analysis (FREE, LOCAL)
MAINTAIN: Single source of truth for research intelligence

DO NOT:
- Create new research analyzer files
- Move this functionality elsewhere  
- Add trading logic here
- Use paid LLMs unless critical

ONLY MODIFY:
- analyze_market_data() method
- learn_from_analysis() method
- store_learning() method
"""

import json
import sqlite3
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
from pathlib import Path
import subprocess
import aiohttp

# Try to import ollama, provide instructions if not available
try:
    import ollama
except ImportError:
    print("❌ Ollama not installed. Please run: pip install ollama")
    print("Also ensure Ollama desktop app is running")
    raise


class ResearchIntelligence:
    """
    Intelligent research analyzer that learns and improves
    Uses LOCAL LLMs for cost efficiency
    """
    
    def __init__(self):
        self.client = ollama.Client()
        self.setup_logging()
        self.setup_database()
        
        # Cost tracking
        self.daily_llm_calls = 0
        self.daily_cost = 0.0
        
        # Learning memory
        self.learning_db = "databases/sqlite_dbs/research_learnings.db"
        
    def setup_logging(self):
        """Setup logging for intelligence tracking"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - ResearchIntelligence - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_database(self):
        """Setup learning database"""
        Path("databases/sqlite_dbs").mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.cursor()
        
        # Learning storage
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                context TEXT NOT NULL,
                insight TEXT NOT NULL,
                outcome TEXT,
                usefulness_score REAL DEFAULT 0,
                applied BOOLEAN DEFAULT FALSE
            )
        """)
        
        # Analysis history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                data_summary TEXT NOT NULL,
                analysis TEXT NOT NULL,
                quality_score REAL DEFAULT 0,
                led_to_profit BOOLEAN DEFAULT NULL
            )
        """)
        
        conn.commit()
        conn.close()
        
    async def ensure_model_available(self, model: str = "mistral:7b"):
        """Ensure the required model is available locally"""
        try:
            # Check if model exists
            models = await self.client.list()
            if not any(model in m['name'] for m in models.get('models', [])):
                self.logger.info(f"📥 Downloading {model}... This may take a few minutes")
                await self.client.pull(model)
                self.logger.info(f"✅ {model} ready for use")
        except Exception as e:
            self.logger.error(f"❌ Error checking/downloading model: {e}")
            raise
            
    async def analyze_market_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Intelligently analyze market data for insights
        Uses LOCAL mistral:7b for cost efficiency
        """
        await self.ensure_model_available()
        
        # Prepare data summary for LLM
        data_summary = self._prepare_data_summary(data)
        
        # Check if we've seen similar patterns before
        similar_analyses = await self._find_similar_analyses(data_summary)
        
        # Construct intelligent prompt
        prompt = f"""You are an expert crypto market analyst. Analyze this market data for trading insights.

Current Market Data:
{data_summary}

{f"Previous similar situations resulted in: {similar_analyses}" if similar_analyses else ""}

Provide analysis in this JSON format:
{{
    "market_sentiment": "bullish/bearish/neutral",
    "key_insights": ["insight1", "insight2", "insight3"],
    "risk_factors": ["risk1", "risk2"],
    "opportunities": ["opportunity1", "opportunity2"],
    "recommended_focus": "what data to collect next",
    "confidence": 0.0-1.0
}}

Be specific and actionable. Focus on patterns that could lead to profitable trades."""

        try:
            # Call LOCAL LLM (FREE)
            response = await self.client.generate(
                model='mistral:7b',
                prompt=prompt,
                format='json'
            )
            
            self.daily_llm_calls += 1
            
            # Parse response
            analysis = json.loads(response['response'])
            
            # Store for learning
            await self._store_analysis(data_summary, analysis)
            
            self.logger.info(f"✅ Market analysis complete. Confidence: {analysis.get('confidence', 0)}")
            
            return {
                'success': True,
                'analysis': analysis,
                'data_summary': data_summary,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Analysis failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'fallback': self._get_fallback_analysis(data)
            }
            
    async def learn_from_analysis(self, analysis: Dict[str, Any], outcomes: Dict[str, Any]) -> Dict[str, Any]:
        """
        Learn from the results of our analysis
        This is how the system gets smarter
        """
        prompt = f"""You are reviewing a previous market analysis to learn and improve.

Previous Analysis:
{json.dumps(analysis, indent=2)}

Actual Outcomes:
{json.dumps(outcomes, indent=2)}

Provide learning insights in JSON format:
{{
    "what_worked": ["thing1", "thing2"],
    "what_failed": ["thing1", "thing2"],
    "key_learning": "main insight for future",
    "pattern_identified": "describe any reliable pattern",
    "improvement_suggestion": "specific way to analyze better next time",
    "usefulness_score": 0.0-1.0
}}

Be specific about what indicators or patterns were most predictive."""

        try:
            response = await self.client.generate(
                model='mistral:7b',
                prompt=prompt,
                format='json'
            )
            
            learning = json.loads(response['response'])
            
            # Store learning in database
            await self._store_learning(
                context=json.dumps(analysis),
                insight=learning['key_learning'],
                outcome=json.dumps(outcomes),
                usefulness_score=learning['usefulness_score']
            )
            
            self.logger.info(f"🧠 Learned: {learning['key_learning']}")
            
            return learning
            
        except Exception as e:
            self.logger.error(f"❌ Learning failed: {e}")
            return {'error': str(e)}
            
    def _prepare_data_summary(self, data: Dict[str, Any]) -> str:
        """Prepare concise data summary for LLM analysis"""
        summary_parts = []
        
        # Price data
        if 'prices' in data:
            for symbol, price_data in data['prices'].items():
                summary_parts.append(
                    f"{symbol}: ${price_data.get('price', 0):.2f} "
                    f"({price_data.get('change_24h', 0):+.2f}%)"
                )
                
        # Volume data
        if 'volumes' in data:
            summary_parts.append(f"Volume trends: {data['volumes']}")
            
        # Sentiment data
        if 'sentiment' in data:
            summary_parts.append(f"Market sentiment: {data['sentiment']}")
            
        # Technical indicators
        if 'indicators' in data:
            summary_parts.append(f"Key indicators: {data['indicators']}")
            
        return "\n".join(summary_parts)
        
    async def _find_similar_analyses(self, data_summary: str) -> Optional[str]:
        """Find similar past analyses to provide context"""
        # For now, simple implementation
        # Could be enhanced with vector similarity search
        
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT analysis, outcome
            FROM analysis_history
            WHERE quality_score > 0.7
            ORDER BY timestamp DESC
            LIMIT 3
        """)
        
        results = cursor.fetchall()
        conn.close()
        
        if results:
            return f"Similar patterns: {results}"
        return None
        
    async def _store_analysis(self, data_summary: str, analysis: Dict[str, Any]):
        """Store analysis for future learning"""
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO analysis_history 
            (timestamp, data_summary, analysis, quality_score)
            VALUES (?, ?, ?, ?)
        """, (
            datetime.now().timestamp(),
            data_summary,
            json.dumps(analysis),
            analysis.get('confidence', 0)
        ))
        
        conn.commit()
        conn.close()
        
    async def _store_learning(self, context: str, insight: str, outcome: str, usefulness_score: float):
        """Store learning for future use"""
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO learnings
            (timestamp, context, insight, outcome, usefulness_score)
            VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.now().timestamp(),
            context,
            insight,
            outcome,
            usefulness_score
        ))
        
        conn.commit()
        conn.close()
        
    def _get_fallback_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Simple rule-based fallback when LLM fails"""
        # Basic analysis without LLM
        analysis = {
            'market_sentiment': 'neutral',
            'key_insights': ['LLM analysis unavailable, using basic rules'],
            'risk_factors': ['Operating without AI insights'],
            'opportunities': [],
            'recommended_focus': 'Fix LLM connection',
            'confidence': 0.3
        }
        
        # Simple price-based sentiment
        if 'prices' in data:
            positive_changes = sum(1 for p in data['prices'].values() 
                                 if p.get('change_24h', 0) > 0)
            total_symbols = len(data['prices'])
            
            if positive_changes > total_symbols * 0.7:
                analysis['market_sentiment'] = 'bullish'
            elif positive_changes < total_symbols * 0.3:
                analysis['market_sentiment'] = 'bearish'
                
        return analysis
        
    async def get_daily_insights(self) -> Dict[str, Any]:
        """Get summary of daily learnings and insights"""
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.cursor()
        
        # Get today's learnings
        today_start = datetime.now().replace(hour=0, minute=0, second=0).timestamp()
        
        cursor.execute("""
            SELECT insight, usefulness_score
            FROM learnings
            WHERE timestamp > ?
            ORDER BY usefulness_score DESC
            LIMIT 5
        """, (today_start,))
        
        top_learnings = cursor.fetchall()
        
        cursor.execute("""
            SELECT COUNT(*), AVG(quality_score)
            FROM analysis_history
            WHERE timestamp > ?
        """, (today_start,))
        
        stats = cursor.fetchone()
        conn.close()
        
        return {
            'top_learnings': [{'insight': l[0], 'score': l[1]} for l in top_learnings],
            'analyses_today': stats[0] if stats else 0,
            'avg_confidence': stats[1] if stats and stats[1] else 0,
            'llm_calls': self.daily_llm_calls,
            'estimated_cost': self.daily_cost
        }


# Example usage
async def main():
    """Test the intelligent research analyzer"""
    analyzer = ResearchIntelligence()
    
    # Sample market data
    test_data = {
        'prices': {
            'BTC': {'price': 52000, 'change_24h': 2.5},
            'ETH': {'price': 3200, 'change_24h': -1.2},
            'SOL': {'price': 95, 'change_24h': 5.8}
        },
        'sentiment': {
            'fear_greed_index': 65,
            'social_sentiment': 'positive'
        },
        'indicators': {
            'btc_rsi': 58,
            'eth_rsi': 45,
            'market_trend': 'consolidating'
        }
    }
    
    # Analyze market data
    print("🧠 Analyzing market data...")
    analysis = await analyzer.analyze_market_data(test_data)
    
    if analysis['success']:
        print(f"\n✅ Analysis Results:")
        print(json.dumps(analysis['analysis'], indent=2))
        
        # Simulate some outcomes after trading
        fake_outcomes = {
            'trades_placed': 2,
            'profit_loss': 125.50,
            'accuracy': 'bullish prediction was correct'
        }
        
        # Learn from the analysis
        print("\n🎓 Learning from outcomes...")
        learning = await analyzer.learn_from_analysis(
            analysis['analysis'], 
            fake_outcomes
        )
        print(json.dumps(learning, indent=2))
        
        # Get daily insights
        print("\n📊 Daily Insights:")
        insights = await analyzer.get_daily_insights()
        print(json.dumps(insights, indent=2))
    else:
        print(f"❌ Analysis failed: {analysis['error']}")


if __name__ == "__main__":
    asyncio.run(main())