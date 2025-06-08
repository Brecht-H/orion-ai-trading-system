#!/usr/bin/env python3
"""
🎯 COMPLETE SYSTEM INTEGRATION TEST
Comprehensive test of all four high-priority components working together
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json

# Import all our components
from research_center.ml_models.news_price_correlation import NewsPriceCorrelationModel
from strategy_center.backtesting.strategy_backtester import StrategyBacktester
from risk_management_center.core.risk_manager import RiskManager
from strategy_center.validation.signal_validator import SignalValidator
from technical_analysis_center.indicators.basic_indicators import BasicIndicators

class CompleteSystemTest:
    """Integration test for the complete Orion trading system"""
    
    def __init__(self, initial_capital: float = 50000.0):
        self.initial_capital = initial_capital
        self.test_results = {}
        
        print("🚀 Initializing Complete Orion System Test...")
        print(f"💰 Initial Capital: ${initial_capital:,.2f}")
        
        # Initialize all components
        self.ml_model = NewsPriceCorrelationModel()
        self.backtester = StrategyBacktester(initial_capital)
        self.risk_manager = RiskManager(initial_capital)
        self.signal_validator = SignalValidator(initial_capital)
        self.technical_indicators = BasicIndicators()
        
        print("✅ All components initialized successfully")
    
    def generate_realistic_market_scenario(self, days: int = 90) -> tuple:
        """Generate realistic market data with corresponding news events"""
        
        print(f"📊 Generating {days}-day market scenario...")
        
        # Generate price data with realistic volatility and trends
        start_date = datetime.now() - timedelta(days=days)
        dates = [start_date + timedelta(days=i) for i in range(days)]
        
        # Bitcoin-like price movements
        base_price = 45000
        prices = []
        volumes = []
        current_price = base_price
        
        # Market phases: accumulation, bull run, correction, recovery
        phase_length = days // 4
        
        for i, date in enumerate(dates):
            phase = i // phase_length
            
            if phase == 0:  # Accumulation phase
                trend = 0.0005
                volatility = 0.02
            elif phase == 1:  # Bull run
                trend = 0.003
                volatility = 0.04
            elif phase == 2:  # Correction
                trend = -0.002
                volatility = 0.06
            else:  # Recovery
                trend = 0.001
                volatility = 0.03
            
            # Add noise and trend
            price_change = np.random.normal(trend, volatility)
            current_price *= (1 + price_change)
            current_price = max(current_price, base_price * 0.3)  # Floor at 30% of base
            
            prices.append(current_price)
            volumes.append(np.random.uniform(1000000, 5000000))  # Random volume
        
        # Create market data DataFrame
        market_data = pd.DataFrame({
            'timestamp': dates,
            'symbol': 'BTC',
            'open': [p * np.random.uniform(0.995, 1.005) for p in prices],
            'high': [p * np.random.uniform(1.01, 1.05) for p in prices],
            'low': [p * np.random.uniform(0.95, 0.99) for p in prices],
            'close': prices,
            'volume': volumes
        })
        
        # Generate corresponding news events
        news_events = self._generate_news_events(dates, prices)
        
        print(f"✅ Generated market data: ${prices[0]:,.0f} → ${prices[-1]:,.0f}")
        print(f"✅ Generated {len(news_events)} news events")
        
        return market_data, news_events
    
    def _generate_news_events(self, dates: list, prices: list) -> list:
        """Generate realistic news events correlated with price movements"""
        
        news_events = []
        
        for i, (date, price) in enumerate(zip(dates, prices)):
            # Calculate price momentum
            if i > 0:
                price_change = (price - prices[i-1]) / prices[i-1]
            else:
                price_change = 0
            
            # Generate news based on price movement
            if price_change > 0.05:  # Strong positive movement
                titles = [
                    "Bitcoin surges as institutional adoption accelerates",
                    "Major cryptocurrency exchange reports record trading volume",
                    "Regulatory clarity boosts crypto market confidence"
                ]
                sentiment = np.random.uniform(0.6, 0.9)
            elif price_change < -0.05:  # Strong negative movement
                titles = [
                    "Cryptocurrency markets face selling pressure amid concerns",
                    "Bitcoin drops as regulatory uncertainty increases",
                    "Market correction continues as investors take profits"
                ]
                sentiment = np.random.uniform(-0.9, -0.6)
            else:  # Normal movement
                titles = [
                    "Bitcoin trading sideways as market awaits direction",
                    "Cryptocurrency market shows mixed signals",
                    "Analysts divided on short-term price outlook"
                ]
                sentiment = np.random.uniform(-0.3, 0.3)
            
            # Add some random news events
            if np.random.random() < 0.3:  # 30% chance of news each day
                news_events.append({
                    'title': np.random.choice(titles),
                    'content': f"Market analysis for {date.strftime('%Y-%m-%d')}",
                    'sentiment': sentiment,
                    'source': np.random.choice(['CoinDesk', 'CoinTelegraph', 'Bloomberg', 'Reuters']),
                    'timestamp': date.timestamp(),
                    'symbol': 'BTC'
                })
        
        return news_events
    
    def test_ml_model_training(self, news_events: list) -> dict:
        """Test ML model training and prediction capabilities"""
        
        print("\n🤖 Testing ML Model Training...")
        
        # Generate training data
        news_df, price_df = self.ml_model._generate_sample_data(days_back=60)
        
        # Add real news events to training data
        real_news_df = pd.DataFrame(news_events)
        if not real_news_df.empty:
            combined_news = pd.concat([news_df, real_news_df], ignore_index=True)
        else:
            combined_news = news_df
        
        # Prepare training data
        X, y = self.ml_model.prepare_training_data(combined_news, price_df)
        
        # Train model
        training_results = self.ml_model.train_model(X, y)
        
        # Test predictions
        sample_news = news_events[:5] if news_events else [
            {
                'title': 'Bitcoin shows strong momentum',
                'sentiment': 0.7,
                'source': 'CoinDesk',
                'timestamp': time.time()
            }
        ]
        
        prediction = self.ml_model.predict_price_impact(sample_news)
        
        results = {
            'training_samples': len(X),
            'features': len(X.columns),
            'r2_score': training_results['r2'],
            'mae': training_results['mae'],
            'sample_prediction': prediction['prediction'],
            'prediction_confidence': prediction['confidence']
        }
        
        print(f"✅ ML Model trained on {results['training_samples']} samples")
        print(f"✅ R² Score: {results['r2_score']:.3f}")
        print(f"✅ Sample prediction: {results['sample_prediction']:.4f} ({results['prediction_confidence']:.1f}% confidence)")
        
        return results
    
    def test_backtesting_engine(self, market_data: pd.DataFrame) -> dict:
        """Test backtesting engine with realistic market data"""
        
        print("\n📊 Testing Backtesting Engine...")
        
        # Add technical signals to market data
        market_data_with_signals = self.backtester.calculate_technical_signals(market_data)
        
        # Run backtest
        backtest_result = self.backtester.execute_strategy(
            market_data_with_signals, 
            "Complete_System_Strategy"
        )
        
        results = {
            'strategy_name': backtest_result.strategy_name,
            'total_return': backtest_result.total_return,
            'total_return_pct': backtest_result.total_return_pct,
            'sharpe_ratio': backtest_result.sharpe_ratio,
            'max_drawdown': backtest_result.max_drawdown,
            'total_trades': backtest_result.total_trades,
            'win_rate': backtest_result.win_rate,
            'profitable_trades': backtest_result.profitable_trades,
            'sortino_ratio': backtest_result.sortino_ratio
        }
        
        print(f"✅ Strategy: {results['strategy_name']}")
        print(f"✅ Total Return: ${results['total_return']:,.2f} ({results['total_return_pct']:.2f}%)")
        print(f"✅ Sharpe Ratio: {results['sharpe_ratio']:.3f}")
        print(f"✅ Max Drawdown: ${results['max_drawdown']:,.2f}")
        print(f"✅ Total Trades: {results['total_trades']}, Win Rate: {results['win_rate']:.1f}%")
        
        return results
    
    def test_risk_management(self, market_data: pd.DataFrame) -> dict:
        """Test risk management system with realistic scenarios"""
        
        print("\n🛡️ Testing Risk Management System...")
        
        # Test position sizing for different scenarios
        current_price = market_data['close'].iloc[-1]
        
        # Test normal position sizing
        position_calc = self.risk_manager.calculate_position_size(
            symbol='BTC',
            entry_price=current_price,
            signal_strength=0.8,
            current_portfolio_value=self.risk_manager.current_capital
        )
        
        # Add position to portfolio
        self.risk_manager.add_position('BTC', current_price, position_calc['recommended_quantity'])
        
        # Test risk assessment
        risk_assessment = self.risk_manager.assess_portfolio_risk()
        
        # Test stop loss scenarios
        stop_loss_price = current_price * 0.95  # 5% stop loss
        exit_signals = self.risk_manager.update_positions({'BTC': stop_loss_price})
        
        results = {
            'position_size': position_calc['recommended_quantity'],
            'position_value': position_calc['position_value'],
            'stop_loss': position_calc['stop_loss'],
            'take_profit': position_calc['take_profit'],
            'portfolio_risk_pct': risk_assessment.portfolio_risk_pct,
            'risk_score': risk_assessment.risk_score,
            'risk_level': risk_assessment.risk_level,
            'exit_signals': len(exit_signals)
        }
        
        print(f"✅ Position Size: {results['position_size']:.6f} BTC (${results['position_value']:,.2f})")
        print(f"✅ Stop Loss: ${results['stop_loss']:,.2f}, Take Profit: ${results['take_profit']:,.2f}")
        print(f"✅ Portfolio Risk: {results['portfolio_risk_pct']:.2f}%")
        print(f"✅ Risk Score: {results['risk_score']:.1f}/100 ({results['risk_level']})")
        
        return results
    
    def test_signal_validation(self, market_data: pd.DataFrame, news_events: list) -> dict:
        """Test signal validation system"""
        
        print("\n🎯 Testing Signal Validation System...")
        
        # Run signal validation
        validation_result = self.signal_validator.validate_signals_historical(
            symbol='BTC',
            days=len(market_data)
        )
        
        # Test with shorter timeframe for comparison
        short_validation = self.signal_validator.validate_signals_historical(
            symbol='BTC',
            days=30
        )
        
        results = {
            'signal_type': validation_result.signal_type,
            'total_signals': validation_result.total_signals,
            'signal_accuracy': validation_result.signal_accuracy,
            'avg_signal_return': validation_result.avg_signal_return,
            'validation_score': validation_result.validation_score,
            'backtest_return': validation_result.backtest_total_return,
            'short_term_score': short_validation.validation_score
        }
        
        print(f"✅ Signal Type: {results['signal_type']}")
        print(f"✅ Total Signals: {results['total_signals']}")
        print(f"✅ Signal Accuracy: {results['signal_accuracy']:.1f}%")
        print(f"✅ Avg Signal Return: {results['avg_signal_return']:.2f}%")
        print(f"✅ Validation Score: {results['validation_score']:.1f}/100")
        
        return results
    
    def run_complete_integration_test(self) -> dict:
        """Run the complete integration test"""
        
        print("🎯 STARTING COMPLETE ORION SYSTEM INTEGRATION TEST")
        print("=" * 60)
        
        start_time = time.time()
        
        # Step 1: Generate realistic market scenario
        market_data, news_events = self.generate_realistic_market_scenario(90)
        
        # Step 2: Test ML Model
        ml_results = self.test_ml_model_training(news_events)
        
        # Step 3: Test Backtesting Engine
        backtest_results = self.test_backtesting_engine(market_data)
        
        # Step 4: Test Risk Management
        risk_results = self.test_risk_management(market_data)
        
        # Step 5: Test Signal Validation
        validation_results = self.test_signal_validation(market_data, news_events)
        
        # Calculate overall system performance
        execution_time = time.time() - start_time
        
        # Compile comprehensive results
        complete_results = {
            'test_metadata': {
                'execution_time': execution_time,
                'test_date': datetime.now().isoformat(),
                'initial_capital': self.initial_capital,
                'market_days': len(market_data),
                'news_events': len(news_events)
            },
            'ml_model': ml_results,
            'backtesting': backtest_results,
            'risk_management': risk_results,
            'signal_validation': validation_results
        }
        
        # Calculate system health score
        system_score = self._calculate_system_health_score(complete_results)
        complete_results['system_health_score'] = system_score
        
        self._print_final_report(complete_results)
        
        return complete_results
    
    def _calculate_system_health_score(self, results: dict) -> dict:
        """Calculate overall system health score"""
        
        # ML Model Score (0-25 points)
        ml_score = min(25, max(0, (results['ml_model']['r2_score'] + 1) * 12.5))
        
        # Backtesting Score (0-25 points)
        backtest_score = min(25, max(0, 
            (results['backtesting']['sharpe_ratio'] + 2) * 6.25 + 
            (results['backtesting']['win_rate'] / 4)
        ))
        
        # Risk Management Score (0-25 points)
        risk_score = min(25, max(0, 25 - (results['risk_management']['risk_score'] / 4)))
        
        # Signal Validation Score (0-25 points)
        validation_score = results['signal_validation']['validation_score'] / 4
        
        total_score = ml_score + backtest_score + risk_score + validation_score
        
        return {
            'ml_model_score': ml_score,
            'backtesting_score': backtest_score,
            'risk_management_score': risk_score,
            'signal_validation_score': validation_score,
            'total_score': total_score,
            'grade': self._get_grade(total_score)
        }
    
    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 90:
            return "A+ (Excellent)"
        elif score >= 80:
            return "A (Very Good)"
        elif score >= 70:
            return "B (Good)"
        elif score >= 60:
            return "C (Fair)"
        elif score >= 50:
            return "D (Poor)"
        else:
            return "F (Failing)"
    
    def _print_final_report(self, results: dict):
        """Print comprehensive final report"""
        
        print("\n" + "=" * 60)
        print("🎯 COMPLETE SYSTEM INTEGRATION TEST RESULTS")
        print("=" * 60)
        
        metadata = results['test_metadata']
        print(f"⏱️ Execution Time: {metadata['execution_time']:.2f} seconds")
        print(f"💰 Test Capital: ${metadata['initial_capital']:,.2f}")
        print(f"📊 Market Period: {metadata['market_days']} days")
        print(f"📰 News Events: {metadata['news_events']}")
        
        print("\n📊 COMPONENT PERFORMANCE:")
        print("-" * 40)
        
        # ML Model
        ml = results['ml_model']
        print(f"🤖 ML Model:")
        print(f"   Training Samples: {ml['training_samples']}")
        print(f"   R² Score: {ml['r2_score']:.3f}")
        print(f"   Prediction Confidence: {ml['prediction_confidence']:.1f}%")
        
        # Backtesting
        bt = results['backtesting']
        print(f"📈 Backtesting:")
        print(f"   Total Return: {bt['total_return_pct']:.2f}%")
        print(f"   Sharpe Ratio: {bt['sharpe_ratio']:.3f}")
        print(f"   Win Rate: {bt['win_rate']:.1f}%")
        
        # Risk Management
        rm = results['risk_management']
        print(f"🛡️ Risk Management:")
        print(f"   Portfolio Risk: {rm['portfolio_risk_pct']:.2f}%")
        print(f"   Risk Level: {rm['risk_level']}")
        print(f"   Position Value: ${rm['position_value']:,.2f}")
        
        # Signal Validation
        sv = results['signal_validation']
        print(f"🎯 Signal Validation:")
        print(f"   Signal Accuracy: {sv['signal_accuracy']:.1f}%")
        print(f"   Validation Score: {sv['validation_score']:.1f}/100")
        print(f"   Avg Signal Return: {sv['avg_signal_return']:.2f}%")
        
        # Overall Score
        score = results['system_health_score']
        print(f"\n🏆 OVERALL SYSTEM HEALTH:")
        print("-" * 40)
        print(f"ML Model Score: {score['ml_model_score']:.1f}/25")
        print(f"Backtesting Score: {score['backtesting_score']:.1f}/25")
        print(f"Risk Management Score: {score['risk_management_score']:.1f}/25")
        print(f"Signal Validation Score: {score['signal_validation_score']:.1f}/25")
        print(f"TOTAL SCORE: {score['total_score']:.1f}/100")
        print(f"GRADE: {score['grade']}")
        
        print("\n✅ INTEGRATION TEST COMPLETED SUCCESSFULLY!")
        print("🚀 All four high-priority components are operational and integrated!")

def main():
    """Run the complete system integration test"""
    
    # Initialize and run test
    test_system = CompleteSystemTest(initial_capital=50000.0)
    results = test_system.run_complete_integration_test()
    
    # Save results to file
    output_file = f"tests/integration_tests/complete_system_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    return results

if __name__ == "__main__":
    main() 