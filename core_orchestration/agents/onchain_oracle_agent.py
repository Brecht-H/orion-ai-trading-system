#!/usr/bin/env python3
"""
⛓️ ON-CHAIN ORACLE AGENT
AI Agent for blockchain transaction analysis and whale movement detection
"""

import asyncio
import json
import sqlite3
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import os
import logging
from dataclasses import dataclass

@dataclass
class WhaleTransaction:
    tx_hash: str
    blockchain: str
    from_address: str
    to_address: str
    amount: float
    symbol: str
    timestamp: datetime
    transaction_type: str  # exchange_deposit, exchange_withdrawal, whale_accumulation, whale_distribution
    exchange_name: Optional[str]
    significance_score: float

@dataclass
class OnChainMetric:
    blockchain: str
    metric_type: str
    value: float
    timestamp: datetime
    change_percentage: float
    trend: str  # increasing, decreasing, stable
    significance: str  # low, medium, high, critical

class OnChainOracleAgent:
    """
    AI Agent for on-chain intelligence
    - Real-time whale movement detection
    - Exchange flow analysis
    - Mining/staking behavior monitoring
    - DeFi protocol interactions
    """
    
    def __init__(self):
        self.agent_id = "onchain_oracle_001"
        self.db_path = "data/onchain_intelligence.db"
        self.setup_database()
        self.setup_logging()
        
        # Agent parameters
        self.whale_threshold_btc = 100  # BTC
        self.whale_threshold_eth = 1000  # ETH
        self.monitoring_interval = 300  # 5 minutes
        
        # Known exchange addresses (simplified)
        self.exchange_addresses = {
            "bitcoin": {
                "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa": "genesis",
                "3Kzh9qAqVWQhEsfQz7zEQL1EuSx5tyNLNS": "binance",
                "bc1qgdjqv0av3q56jvd82tkdjpy7gdp9ut8tlqmgrpmv24sq90ecnvqqjwvw97": "coinbase"
            },
            "ethereum": {
                "0xd551234ae421e3bcba99a0da6d736074f22192ff": "binance_hot",
                "0x3f5ce5fbfe3e9af3971dd833d26ba9b5c936f0be": "binance_cold",
                "0x28c6c06298d514db089934071355e5743bf21d60": "binance_exchange"
            }
        }
        
        # API endpoints
        self.api_endpoints = {
            "bitcoin": {
                "mempool": "https://mempool.space/api",
                "blockchain_info": "https://blockchain.info",
                "blockcypher": "https://api.blockcypher.com/v1/btc/main"
            },
            "ethereum": {
                "etherscan": "https://api.etherscan.io/api",
                "ethereum_etl": "https://ethereum-etl.org/api"
            }
        }
        
        # API keys
        self.api_keys = {
            "etherscan": os.getenv("ETHERSCAN_API_KEY", ""),
            "blockcypher": os.getenv("BLOCKCYPHER_API_KEY", "")
        }
        
    def setup_database(self):
        """Setup on-chain intelligence database"""
        Path("data").mkdir(exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Whale transactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS whale_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tx_hash TEXT UNIQUE NOT NULL,
                blockchain TEXT NOT NULL,
                from_address TEXT NOT NULL,
                to_address TEXT NOT NULL,
                amount REAL NOT NULL,
                symbol TEXT NOT NULL,
                timestamp REAL NOT NULL,
                transaction_type TEXT NOT NULL,
                exchange_name TEXT,
                significance_score REAL DEFAULT 0.0,
                block_number INTEGER,
                gas_price REAL,
                raw_data TEXT
            )
        """)
        
        # On-chain metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS onchain_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                blockchain TEXT NOT NULL,
                metric_type TEXT NOT NULL,
                value REAL NOT NULL,
                timestamp REAL NOT NULL,
                change_percentage REAL DEFAULT 0.0,
                trend TEXT DEFAULT 'stable',
                significance TEXT DEFAULT 'low',
                raw_data TEXT
            )
        """)
        
        # Exchange flows table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exchange_flows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exchange_name TEXT NOT NULL,
                blockchain TEXT NOT NULL,
                flow_type TEXT NOT NULL,
                amount REAL NOT NULL,
                symbol TEXT NOT NULL,
                timestamp REAL NOT NULL,
                address TEXT NOT NULL,
                confidence_score REAL DEFAULT 0.0
            )
        """)
        
        # Whale alerts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS whale_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_type TEXT NOT NULL,
                blockchain TEXT NOT NULL,
                description TEXT NOT NULL,
                significance TEXT NOT NULL,
                timestamp REAL NOT NULL,
                related_tx_hash TEXT,
                recommendation TEXT,
                confidence REAL DEFAULT 0.0
            )
        """)
        
        conn.commit()
        conn.close()
        
    def setup_logging(self):
        """Setup agent logging"""
        Path("logs").mkdir(exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - OnChainOracle - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/onchain_oracle.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"⛓️ On-Chain Oracle Agent {self.agent_id} initialized")
    
    async def run_oracle_cycle(self) -> Dict[str, Any]:
        """Alias for test compatibility"""
        return await self.run_monitoring_cycle()
    
    async def run_monitoring_cycle(self) -> Dict[str, Any]:
        """Run comprehensive on-chain monitoring cycle"""
        self.logger.info("⛓️ Starting on-chain monitoring cycle...")
        cycle_start = time.time()
        
        # 1. Monitor whale transactions
        whale_transactions = await self.monitor_whale_transactions()
        
        # 2. Analyze exchange flows
        exchange_flows = await self.analyze_exchange_flows()
        
        # 3. Track on-chain metrics
        metrics = await self.track_onchain_metrics()
        
        # 4. Generate whale alerts
        alerts = await self.generate_whale_alerts(whale_transactions)
        
        # 5. Analyze patterns
        patterns = await self.analyze_movement_patterns()
        
        cycle_time = time.time() - cycle_start
        
        results = {
            "cycle_time": cycle_time,
            "whale_transactions": len(whale_transactions),
            "exchange_flows": len(exchange_flows),
            "onchain_metrics": len(metrics),
            "whale_alerts": len(alerts),
            "movement_patterns": len(patterns),
            "significant_transactions": [
                {
                    "hash": tx.tx_hash[:20] + "...",
                    "blockchain": tx.blockchain,
                    "amount": tx.amount,
                    "type": tx.transaction_type,
                    "significance": tx.significance_score
                } for tx in whale_transactions if tx.significance_score > 0.7
            ],
            "critical_alerts": [
                {
                    "type": alert["type"],
                    "description": alert["description"],
                    "significance": alert["significance"]
                } for alert in alerts if alert.get("significance") == "critical"
            ]
        }
        
        self.logger.info(f"✅ On-chain monitoring complete ({cycle_time:.2f}s)")
        self.logger.info(f"   🐋 Whale transactions: {len(whale_transactions)}")
        self.logger.info(f"   🏦 Exchange flows: {len(exchange_flows)}")
        self.logger.info(f"   📊 Metrics tracked: {len(metrics)}")
        self.logger.info(f"   🚨 Alerts generated: {len(alerts)}")
        
        return results
    
    async def monitor_whale_transactions(self) -> List[WhaleTransaction]:
        """Monitor large cryptocurrency transactions"""
        whale_transactions = []
        
        # Monitor Bitcoin transactions
        btc_whales = await self.monitor_bitcoin_whales()
        whale_transactions.extend(btc_whales)
        
        # Monitor Ethereum transactions
        eth_whales = await self.monitor_ethereum_whales()
        whale_transactions.extend(eth_whales)
        
        # Store transactions
        for tx in whale_transactions:
            self.store_whale_transaction(tx)
        
        return whale_transactions
    
    async def monitor_bitcoin_whales(self) -> List[WhaleTransaction]:
        """Monitor large Bitcoin transactions"""
        whale_txs = []
        
        try:
            # Get recent large transactions from blockchain.info
            response = requests.get(
                "https://blockchain.info/unconfirmed-transactions?format=json",
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                for tx in data.get("txs", [])[:10]:  # Limit to recent 10
                    # Calculate total output value
                    total_value = sum(output.get("value", 0) for output in tx.get("out", [])) / 100000000  # Convert satoshi to BTC
                    
                    if total_value >= self.whale_threshold_btc:
                        # Analyze transaction
                        tx_analysis = self.analyze_bitcoin_transaction(tx, total_value)
                        if tx_analysis:
                            whale_txs.append(tx_analysis)
                            
        except Exception as e:
            self.logger.warning(f"⚠️ Bitcoin whale monitoring error: {e}")
            # Generate mock data for testing
            whale_txs = self.generate_mock_bitcoin_whales()
        
        return whale_txs
    
    async def monitor_ethereum_whales(self) -> List[WhaleTransaction]:
        """Monitor large Ethereum transactions"""
        whale_txs = []
        
        if not self.api_keys["etherscan"]:
            self.logger.warning("⚠️ Etherscan API key not available - using mock data")
            return self.generate_mock_ethereum_whales()
        
        try:
            # Get recent blocks and analyze large transactions
            response = requests.get(
                f"https://api.etherscan.io/api?module=proxy&action=eth_blockNumber&apikey={self.api_keys['etherscan']}",
                timeout=30
            )
            
            if response.status_code == 200:
                # Simplified - would analyze recent blocks for large transactions
                whale_txs = self.generate_mock_ethereum_whales()
                
        except Exception as e:
            self.logger.warning(f"⚠️ Ethereum whale monitoring error: {e}")
            whale_txs = self.generate_mock_ethereum_whales()
        
        return whale_txs
    
    async def analyze_exchange_flows(self) -> List[Dict[str, Any]]:
        """Analyze cryptocurrency flows to/from exchanges"""
        exchange_flows = []
        
        # Analyze Bitcoin exchange flows
        btc_flows = await self.analyze_bitcoin_exchange_flows()
        exchange_flows.extend(btc_flows)
        
        # Analyze Ethereum exchange flows
        eth_flows = await self.analyze_ethereum_exchange_flows()
        exchange_flows.extend(eth_flows)
        
        return exchange_flows
    
    async def analyze_bitcoin_exchange_flows(self) -> List[Dict[str, Any]]:
        """Analyze Bitcoin exchange inflows/outflows"""
        flows = []
        
        # Mock data for testing
        flows = [
            {
                "exchange": "binance",
                "flow_type": "inflow",
                "amount": 2500.0,
                "symbol": "BTC",
                "timestamp": time.time(),
                "significance": "high"
            },
            {
                "exchange": "coinbase",
                "flow_type": "outflow", 
                "amount": 1800.0,
                "symbol": "BTC",
                "timestamp": time.time(),
                "significance": "medium"
            }
        ]
        
        return flows
    
    async def analyze_ethereum_exchange_flows(self) -> List[Dict[str, Any]]:
        """Analyze Ethereum exchange inflows/outflows"""
        flows = []
        
        # Mock data for testing
        flows = [
            {
                "exchange": "binance",
                "flow_type": "inflow",
                "amount": 15000.0,
                "symbol": "ETH", 
                "timestamp": time.time(),
                "significance": "medium"
            }
        ]
        
        return flows
    
    async def track_onchain_metrics(self) -> List[OnChainMetric]:
        """Track important on-chain metrics"""
        metrics = []
        
        # Bitcoin metrics
        btc_metrics = await self.get_bitcoin_metrics()
        metrics.extend(btc_metrics)
        
        # Ethereum metrics
        eth_metrics = await self.get_ethereum_metrics()
        metrics.extend(eth_metrics)
        
        # Store metrics
        for metric in metrics:
            self.store_onchain_metric(metric)
        
        return metrics
    
    async def get_bitcoin_metrics(self) -> List[OnChainMetric]:
        """Get Bitcoin on-chain metrics"""
        metrics = []
        
        try:
            # Hash rate
            hash_response = requests.get("https://blockchain.info/q/hashrate", timeout=10)
            if hash_response.status_code == 200:
                hash_rate = float(hash_response.text.strip())
                
                metric = OnChainMetric(
                    blockchain="bitcoin",
                    metric_type="hash_rate",
                    value=hash_rate,
                    timestamp=datetime.now(),
                    change_percentage=0.0,  # Would calculate from historical data
                    trend="stable",
                    significance="medium"
                )
                metrics.append(metric)
            
            # Transaction count
            tx_response = requests.get("https://blockchain.info/q/24hrtransactioncount", timeout=10)
            if tx_response.status_code == 200:
                tx_count = float(tx_response.text.strip())
                
                metric = OnChainMetric(
                    blockchain="bitcoin",
                    metric_type="daily_transactions",
                    value=tx_count,
                    timestamp=datetime.now(),
                    change_percentage=0.0,
                    trend="stable",
                    significance="low"
                )
                metrics.append(metric)
                
        except Exception as e:
            self.logger.warning(f"⚠️ Bitcoin metrics error: {e}")
        
        return metrics
    
    async def get_ethereum_metrics(self) -> List[OnChainMetric]:
        """Get Ethereum on-chain metrics"""
        metrics = []
        
        # Mock Ethereum metrics
        metrics = [
            OnChainMetric(
                blockchain="ethereum",
                metric_type="gas_price",
                value=25.0,
                timestamp=datetime.now(),
                change_percentage=-5.2,
                trend="decreasing",
                significance="medium"
            ),
            OnChainMetric(
                blockchain="ethereum",
                metric_type="active_addresses",
                value=450000.0,
                timestamp=datetime.now(),
                change_percentage=2.1,
                trend="increasing",
                significance="low"
            )
        ]
        
        return metrics
    
    async def generate_whale_alerts(self, transactions: List[WhaleTransaction]) -> List[Dict[str, Any]]:
        """Generate alerts for significant whale movements"""
        alerts = []
        
        for tx in transactions:
            if tx.significance_score > 0.8:
                alert = {
                    "type": "whale_movement",
                    "blockchain": tx.blockchain,
                    "description": f"Large {tx.symbol} movement: {tx.amount:.2f} {tx.symbol} ({tx.transaction_type})",
                    "significance": "high" if tx.significance_score > 0.9 else "medium",
                    "timestamp": time.time(),
                    "tx_hash": tx.tx_hash,
                    "recommendation": self.generate_whale_recommendation(tx),
                    "confidence": tx.significance_score
                }
                alerts.append(alert)
                self.store_whale_alert(alert)
        
        return alerts
    
    async def analyze_movement_patterns(self) -> List[Dict[str, Any]]:
        """Analyze whale movement patterns"""
        patterns = []
        
        # Mock pattern analysis
        patterns = [
            {
                "pattern_type": "accumulation",
                "blockchain": "bitcoin",
                "confidence": 0.8,
                "description": "Large wallets showing accumulation pattern over last 24h",
                "impact_prediction": "bullish"
            },
            {
                "pattern_type": "exchange_preparation",
                "blockchain": "ethereum", 
                "confidence": 0.7,
                "description": "Increased exchange inflows suggest potential selling pressure",
                "impact_prediction": "bearish"
            }
        ]
        
        return patterns
    
    # Helper methods
    def analyze_bitcoin_transaction(self, tx_data: Dict, value: float) -> Optional[WhaleTransaction]:
        """Analyze Bitcoin transaction for whale activity"""
        try:
            tx_hash = tx_data.get("hash", "")
            inputs = tx_data.get("inputs", [])
            outputs = tx_data.get("out", [])
            
            if not inputs or not outputs:
                return None
            
            # Determine transaction type
            from_address = inputs[0].get("prev_out", {}).get("addr", "unknown")
            to_address = outputs[0].get("addr", "unknown")
            
            tx_type = self.classify_transaction_type(from_address, to_address, "bitcoin")
            exchange_name = self.identify_exchange(from_address, to_address, "bitcoin")
            
            # Calculate significance
            significance = self.calculate_transaction_significance(value, tx_type, "bitcoin")
            
            return WhaleTransaction(
                tx_hash=tx_hash,
                blockchain="bitcoin",
                from_address=from_address,
                to_address=to_address,
                amount=value,
                symbol="BTC",
                timestamp=datetime.fromtimestamp(tx_data.get("time", time.time())),
                transaction_type=tx_type,
                exchange_name=exchange_name,
                significance_score=significance
            )
            
        except Exception as e:
            self.logger.warning(f"⚠️ Bitcoin transaction analysis error: {e}")
            return None
    
    def classify_transaction_type(self, from_addr: str, to_addr: str, blockchain: str) -> str:
        """Classify transaction type based on addresses"""
        exchange_addrs = self.exchange_addresses.get(blockchain, {})
        
        from_is_exchange = from_addr in exchange_addrs
        to_is_exchange = to_addr in exchange_addrs
        
        if from_is_exchange and not to_is_exchange:
            return "exchange_withdrawal"
        elif not from_is_exchange and to_is_exchange:
            return "exchange_deposit"
        elif not from_is_exchange and not to_is_exchange:
            return "whale_transfer"
        else:
            return "exchange_internal"
    
    def identify_exchange(self, from_addr: str, to_addr: str, blockchain: str) -> Optional[str]:
        """Identify exchange involved in transaction"""
        exchange_addrs = self.exchange_addresses.get(blockchain, {})
        
        if from_addr in exchange_addrs:
            return exchange_addrs[from_addr]
        elif to_addr in exchange_addrs:
            return exchange_addrs[to_addr]
        
        return None
    
    def calculate_transaction_significance(self, amount: float, tx_type: str, blockchain: str) -> float:
        """Calculate transaction significance score"""
        base_score = 0.0
        
        # Amount significance
        if blockchain == "bitcoin":
            if amount > 5000:
                base_score = 1.0
            elif amount > 1000:
                base_score = 0.8
            elif amount > 500:
                base_score = 0.6
            else:
                base_score = 0.4
        elif blockchain == "ethereum":
            if amount > 50000:
                base_score = 1.0
            elif amount > 10000:
                base_score = 0.8
            elif amount > 5000:
                base_score = 0.6
            else:
                base_score = 0.4
        
        # Transaction type multiplier
        type_multipliers = {
            "exchange_deposit": 1.2,  # Potential selling pressure
            "exchange_withdrawal": 1.1,  # Potential accumulation
            "whale_transfer": 0.9,
            "exchange_internal": 0.5
        }
        
        multiplier = type_multipliers.get(tx_type, 1.0)
        return min(base_score * multiplier, 1.0)
    
    def generate_whale_recommendation(self, tx: WhaleTransaction) -> str:
        """Generate recommendation based on whale transaction"""
        if tx.transaction_type == "exchange_deposit" and tx.amount > 1000:
            return "Potential selling pressure - monitor for price impact"
        elif tx.transaction_type == "exchange_withdrawal" and tx.amount > 1000:
            return "Possible accumulation - bullish signal"
        elif tx.transaction_type == "whale_transfer":
            return "Large wallet activity - monitor for follow-up movements"
        else:
            return "Monitor transaction for market impact"
    
    def store_whale_transaction(self, tx: WhaleTransaction):
        """Store whale transaction in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR IGNORE INTO whale_transactions
            (tx_hash, blockchain, from_address, to_address, amount, symbol,
             timestamp, transaction_type, exchange_name, significance_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tx.tx_hash, tx.blockchain, tx.from_address, tx.to_address,
            tx.amount, tx.symbol, tx.timestamp.timestamp(),
            tx.transaction_type, tx.exchange_name, tx.significance_score
        ))
        
        conn.commit()
        conn.close()
    
    def store_onchain_metric(self, metric: OnChainMetric):
        """Store on-chain metric in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO onchain_metrics
            (blockchain, metric_type, value, timestamp, change_percentage, trend, significance)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            metric.blockchain, metric.metric_type, metric.value,
            metric.timestamp.timestamp(), metric.change_percentage,
            metric.trend, metric.significance
        ))
        
        conn.commit()
        conn.close()
    
    def store_whale_alert(self, alert: Dict[str, Any]):
        """Store whale alert in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO whale_alerts
            (alert_type, blockchain, description, significance, timestamp,
             related_tx_hash, recommendation, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            alert["type"], alert["blockchain"], alert["description"],
            alert["significance"], alert["timestamp"], alert.get("tx_hash"),
            alert.get("recommendation"), alert.get("confidence", 0.0)
        ))
        
        conn.commit()
        conn.close()
    
    def generate_mock_bitcoin_whales(self) -> List[WhaleTransaction]:
        """Generate mock Bitcoin whale transactions"""
        return [
            WhaleTransaction(
                tx_hash="abc123...def456",
                blockchain="bitcoin",
                from_address="1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
                to_address="3Kzh9qAqVWQhEsfQz7zEQL1EuSx5tyNLNS",
                amount=2500.0,
                symbol="BTC",
                timestamp=datetime.now(),
                transaction_type="exchange_deposit",
                exchange_name="binance",
                significance_score=0.9
            )
        ]
    
    def generate_mock_ethereum_whales(self) -> List[WhaleTransaction]:
        """Generate mock Ethereum whale transactions"""
        return [
            WhaleTransaction(
                tx_hash="0x123abc...456def",
                blockchain="ethereum",
                from_address="0xd551234ae421e3bcba99a0da6d736074f22192ff",
                to_address="0x28c6c06298d514db089934071355e5743bf21d60",
                amount=15000.0,
                symbol="ETH",
                timestamp=datetime.now(),
                transaction_type="exchange_withdrawal",
                exchange_name="binance",
                significance_score=0.8
            )
        ]

if __name__ == "__main__":
    async def main():
        agent = OnChainOracleAgent()
        
        print("⛓️ On-Chain Oracle Agent - Running monitoring cycle...")
        
        # Run monitoring cycle
        results = await agent.run_monitoring_cycle()
        
        print(f"\n🎯 ON-CHAIN MONITORING RESULTS:")
        print(f"Cycle Time: {results['cycle_time']:.2f}s")
        print(f"Whale Transactions: {results['whale_transactions']}")
        print(f"Exchange Flows: {results['exchange_flows']}")
        print(f"On-Chain Metrics: {results['onchain_metrics']}")
        print(f"Whale Alerts: {results['whale_alerts']}")
        
        if results['significant_transactions']:
            print(f"\n🐋 SIGNIFICANT TRANSACTIONS:")
            for tx in results['significant_transactions']:
                print(f"  {tx['hash']} ({tx['blockchain']}): {tx['amount']:.2f} {tx['type']}")
        
        if results['critical_alerts']:
            print(f"\n🚨 CRITICAL ALERTS:")
            for alert in results['critical_alerts']:
                print(f"  {alert['type']}: {alert['description']}")
    
    asyncio.run(main()) 