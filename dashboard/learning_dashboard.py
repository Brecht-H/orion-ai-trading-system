#!/usr/bin/env python3
"""
ORION LEARNING DASHBOARD
Visual interface for monitoring system intelligence and learning progress
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime, timedelta
import sys
import os
from pathlib import Path

# Add workspace to path
sys.path.insert(0, str(Path(__file__).parent.parent))

app = Flask(__name__)
CORS(app)

class LearningDashboard:
    """Dashboard for monitoring system learning"""
    
    @staticmethod
    def get_learning_stats():
        """Get learning statistics from databases"""
        stats = {
            'total_learnings': 0,
            'avg_confidence': 0,
            'total_strategies': 0,
            'successful_analyses': 0,
            'data_collected_today': 0,
            'events_processed': 0
        }
        
        try:
            # Research learnings
            conn = sqlite3.connect("databases/sqlite_dbs/research_learnings.db")
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM learnings")
            stats['total_learnings'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT AVG(usefulness_score) FROM learnings WHERE usefulness_score > 0")
            avg_score = cursor.fetchone()[0]
            stats['avg_usefulness'] = avg_score if avg_score else 0
            
            cursor.execute("SELECT COUNT(*) FROM analysis_history WHERE quality_score > 0.7")
            stats['successful_analyses'] = cursor.fetchone()[0]
            
            conn.close()
            
            # Knowledge base
            conn = sqlite3.connect("databases/sqlite_dbs/knowledge_base.db")
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM strategy_templates")
            stats['total_strategies'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM knowledge_items")
            stats['knowledge_items'] = cursor.fetchone()[0]
            
            conn.close()
            
            # Data collection
            conn = sqlite3.connect("data/free_sources_data.db")
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM free_data WHERE date = date('now')")
            stats['data_collected_today'] = cursor.fetchone()[0]
            
            conn.close()
            
            # Event processing
            conn = sqlite3.connect("databases/sqlite_dbs/event_store.db")
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM events WHERE processed = 1")
            stats['events_processed'] = cursor.fetchone()[0]
            
            conn.close()
            
        except Exception as e:
            print(f"Error getting stats: {e}")
            
        return stats
        
    @staticmethod
    def get_recent_learnings(limit=10):
        """Get recent learning insights"""
        learnings = []
        
        try:
            conn = sqlite3.connect("databases/sqlite_dbs/research_learnings.db")
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT timestamp, insight, usefulness_score
                FROM learnings
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
            
            for row in cursor.fetchall():
                learnings.append({
                    'timestamp': datetime.fromtimestamp(row[0]).isoformat(),
                    'insight': row[1],
                    'score': row[2]
                })
                
            conn.close()
            
        except Exception as e:
            print(f"Error getting learnings: {e}")
            
        return learnings
        
    @staticmethod
    def get_strategy_performance():
        """Get strategy performance data"""
        strategies = []
        
        try:
            conn = sqlite3.connect("databases/sqlite_dbs/knowledge_base.db")
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT name, created_timestamp, risk_parameters
                FROM strategy_templates
                ORDER BY created_timestamp DESC
                LIMIT 20
            """)
            
            for row in cursor.fetchall():
                risk_params = json.loads(row[2])
                strategies.append({
                    'name': row[0],
                    'created': datetime.fromtimestamp(row[1]).isoformat(),
                    'stop_loss': risk_params.get('stop_loss', 'N/A'),
                    'take_profit': risk_params.get('take_profit', 'N/A')
                })
                
            conn.close()
            
        except Exception as e:
            print(f"Error getting strategies: {e}")
            
        return strategies
        
    @staticmethod
    def get_event_timeline():
        """Get event processing timeline"""
        events = []
        
        try:
            conn = sqlite3.connect("databases/sqlite_dbs/event_store.db")
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT event_type, source_service, timestamp, processed
                FROM events
                ORDER BY timestamp DESC
                LIMIT 50
            """)
            
            for row in cursor.fetchall():
                events.append({
                    'type': row[0],
                    'source': row[1],
                    'timestamp': datetime.fromtimestamp(row[2]).isoformat(),
                    'processed': bool(row[3])
                })
                
            conn.close()
            
        except Exception as e:
            print(f"Error getting events: {e}")
            
        return events
        
    @staticmethod
    def get_confidence_trend():
        """Get confidence score trend over time"""
        trend_data = []
        
        try:
            conn = sqlite3.connect("databases/sqlite_dbs/research_learnings.db")
            cursor = conn.cursor()
            
            # Get daily average confidence
            cursor.execute("""
                SELECT 
                    date(timestamp, 'unixepoch') as day,
                    AVG(quality_score) as avg_confidence,
                    COUNT(*) as analysis_count
                FROM analysis_history
                WHERE timestamp > ?
                GROUP BY day
                ORDER BY day
            """, ((datetime.now() - timedelta(days=7)).timestamp(),))
            
            for row in cursor.fetchall():
                trend_data.append({
                    'date': row[0],
                    'confidence': row[1] if row[1] else 0,
                    'count': row[2]
                })
                
            conn.close()
            
        except Exception as e:
            print(f"Error getting trend: {e}")
            
        return trend_data


# Flask Routes
@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('learning_dashboard.html')

@app.route('/api/stats')
def get_stats():
    """API endpoint for dashboard stats"""
    return jsonify(LearningDashboard.get_learning_stats())

@app.route('/api/learnings')
def get_learnings():
    """API endpoint for recent learnings"""
    limit = request.args.get('limit', 10, type=int)
    return jsonify(LearningDashboard.get_recent_learnings(limit))

@app.route('/api/strategies')
def get_strategies():
    """API endpoint for strategy data"""
    return jsonify(LearningDashboard.get_strategy_performance())

@app.route('/api/events')
def get_events():
    """API endpoint for event timeline"""
    return jsonify(LearningDashboard.get_event_timeline())

@app.route('/api/confidence_trend')
def get_confidence_trend():
    """API endpoint for confidence trend"""
    return jsonify(LearningDashboard.get_confidence_trend())

@app.route('/api/system_health')
def get_system_health():
    """API endpoint for system health check"""
    health = {
        'status': 'operational',
        'services': {},
        'last_update': datetime.now().isoformat()
    }
    
    # Check each database
    databases = {
        'research': "databases/sqlite_dbs/research_learnings.db",
        'knowledge': "databases/sqlite_dbs/knowledge_base.db",
        'events': "databases/sqlite_dbs/event_store.db",
        'data': "data/free_sources_data.db"
    }
    
    for name, path in databases.items():
        if os.path.exists(path):
            size = os.path.getsize(path) / 1024  # KB
            health['services'][name] = {
                'status': 'active',
                'size_kb': round(size, 2)
            }
        else:
            health['services'][name] = {
                'status': 'missing',
                'size_kb': 0
            }
            health['status'] = 'degraded'
            
    return jsonify(health)


# Create HTML template directory and file
def create_dashboard_template():
    """Create the HTML template for the dashboard"""
    template_dir = Path(__file__).parent / 'templates'
    template_dir.mkdir(exist_ok=True)
    
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Orion Learning Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0e27;
            color: #e0e0e0;
            line-height: 1.6;
        }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: #1a1f3a;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid #2a3456;
            transition: transform 0.3s;
        }
        .stat-card:hover { transform: translateY(-5px); }
        .stat-value { font-size: 2em; font-weight: bold; color: #667eea; }
        .stat-label { color: #888; margin-top: 5px; }
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
        }
        .dashboard-card {
            background: #1a1f3a;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #2a3456;
        }
        .dashboard-card h3 {
            margin-bottom: 15px;
            color: #667eea;
            border-bottom: 1px solid #2a3456;
            padding-bottom: 10px;
        }
        .learning-item {
            padding: 10px;
            margin: 5px 0;
            background: #0a0e27;
            border-radius: 5px;
            border-left: 3px solid #667eea;
        }
        .confidence-high { border-left-color: #4caf50; }
        .confidence-medium { border-left-color: #ff9800; }
        .confidence-low { border-left-color: #f44336; }
        .event-item {
            display: flex;
            justify-content: space-between;
            padding: 8px;
            margin: 5px 0;
            background: #0a0e27;
            border-radius: 5px;
        }
        .event-processed { opacity: 0.7; }
        .strategy-item {
            padding: 10px;
            margin: 5px 0;
            background: #0a0e27;
            border-radius: 5px;
            display: grid;
            grid-template-columns: 2fr 1fr 1fr;
            gap: 10px;
        }
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 5px;
        }
        .status-active { background: #4caf50; }
        .status-inactive { background: #f44336; }
        .chart-container { position: relative; height: 300px; }
        #updateTime { text-align: center; color: #888; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 Orion Learning Dashboard</h1>
            <p>Real-time Intelligence & Learning Progress</p>
        </div>
        
        <div class="stats-grid" id="statsGrid">
            <!-- Stats will be populated here -->
        </div>
        
        <div class="dashboard-grid">
            <div class="dashboard-card">
                <h3>📊 Confidence Trend</h3>
                <div class="chart-container">
                    <canvas id="confidenceChart"></canvas>
                </div>
            </div>
            
            <div class="dashboard-card">
                <h3>🧠 Recent Learnings</h3>
                <div id="learningsList"></div>
            </div>
            
            <div class="dashboard-card">
                <h3>📈 Generated Strategies</h3>
                <div id="strategiesList"></div>
            </div>
            
            <div class="dashboard-card">
                <h3>🔄 Event Timeline</h3>
                <div id="eventsList"></div>
            </div>
        </div>
        
        <div id="updateTime"></div>
    </div>
    
    <script>
        // Initialize chart
        const ctx = document.getElementById('confidenceChart').getContext('2d');
        const confidenceChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Average Confidence',
                    data: [],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 1,
                        ticks: { color: '#888' },
                        grid: { color: '#2a3456' }
                    },
                    x: {
                        ticks: { color: '#888' },
                        grid: { color: '#2a3456' }
                    }
                },
                plugins: {
                    legend: { labels: { color: '#e0e0e0' } }
                }
            }
        });
        
        // Update functions
        async function updateStats() {
            const response = await fetch('/api/stats');
            const stats = await response.json();
            
            const statsHtml = `
                <div class="stat-card">
                    <div class="stat-value">${stats.total_learnings}</div>
                    <div class="stat-label">Total Learnings</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.total_strategies}</div>
                    <div class="stat-label">Strategies Generated</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.data_collected_today}</div>
                    <div class="stat-label">Data Points Today</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.events_processed}</div>
                    <div class="stat-label">Events Processed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.successful_analyses}</div>
                    <div class="stat-label">Successful Analyses</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${(stats.avg_usefulness * 100).toFixed(0)}%</div>
                    <div class="stat-label">Avg Usefulness</div>
                </div>
            `;
            document.getElementById('statsGrid').innerHTML = statsHtml;
        }
        
        async function updateLearnings() {
            const response = await fetch('/api/learnings');
            const learnings = await response.json();
            
            const html = learnings.map(learning => {
                const confidenceClass = learning.score > 0.7 ? 'confidence-high' : 
                                      learning.score > 0.4 ? 'confidence-medium' : 'confidence-low';
                return `
                    <div class="learning-item ${confidenceClass}">
                        <div>${learning.insight}</div>
                        <small>Score: ${(learning.score * 100).toFixed(0)}% | ${new Date(learning.timestamp).toLocaleTimeString()}</small>
                    </div>
                `;
            }).join('');
            
            document.getElementById('learningsList').innerHTML = html || '<p>No learnings yet</p>';
        }
        
        async function updateStrategies() {
            const response = await fetch('/api/strategies');
            const strategies = await response.json();
            
            const html = strategies.map(strategy => `
                <div class="strategy-item">
                    <div>${strategy.name}</div>
                    <div>SL: ${strategy.stop_loss}</div>
                    <div>TP: ${strategy.take_profit}</div>
                </div>
            `).join('');
            
            document.getElementById('strategiesList').innerHTML = html || '<p>No strategies yet</p>';
        }
        
        async function updateEvents() {
            const response = await fetch('/api/events');
            const events = await response.json();
            
            const html = events.slice(0, 10).map(event => `
                <div class="event-item ${event.processed ? 'event-processed' : ''}">
                    <div>
                        <span class="status-indicator ${event.processed ? 'status-active' : 'status-inactive'}"></span>
                        ${event.type}
                    </div>
                    <small>${new Date(event.timestamp).toLocaleTimeString()}</small>
                </div>
            `).join('');
            
            document.getElementById('eventsList').innerHTML = html || '<p>No events yet</p>';
        }
        
        async function updateConfidenceTrend() {
            const response = await fetch('/api/confidence_trend');
            const trend = await response.json();
            
            confidenceChart.data.labels = trend.map(d => d.date);
            confidenceChart.data.datasets[0].data = trend.map(d => d.confidence);
            confidenceChart.update();
        }
        
        function updateTime() {
            document.getElementById('updateTime').textContent = 
                `Last updated: ${new Date().toLocaleTimeString()}`;
        }
        
        // Update all data
        async function updateDashboard() {
            await Promise.all([
                updateStats(),
                updateLearnings(),
                updateStrategies(),
                updateEvents(),
                updateConfidenceTrend()
            ]);
            updateTime();
        }
        
        // Initial load and auto-refresh
        updateDashboard();
        setInterval(updateDashboard, 10000); // Update every 10 seconds
    </script>
</body>
</html>'''
    
    template_file = template_dir / 'learning_dashboard.html'
    template_file.write_text(html_content)
    

if __name__ == '__main__':
    # Create template
    create_dashboard_template()
    
    # Run dashboard
    print("🚀 Starting Orion Learning Dashboard...")
    print("📊 Open http://localhost:5002 in your browser")
    print("Press Ctrl+C to stop\n")
    
    app.run(host='0.0.0.0', port=5002, debug=True)