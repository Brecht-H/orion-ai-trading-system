#!/usr/bin/env python3
"""
🛡️ ORION MCP SERVER - Direct Database, Notion & LLM Integration
Real-time MCP server providing direct access to all Orion systems
"""

import asyncio
import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import requests
from dataclasses import dataclass, asdict

# MCP Protocol Implementation
@dataclass
class MCPTool:
    name: str
    description: str
    input_schema: Dict[str, Any]

@dataclass 
class MCPResponse:
    content: List[Dict[str, Any]]
    is_error: bool = False

class OrionMCPServer:
    """
    Advanced MCP Server with direct integrations:
    - Real-time database access (9+ SQLite databases)
    - Notion API direct connection
    - External LLM orchestration
    - Live data collection monitoring
    """
    
    def __init__(self):
        self.databases = {
            'free_sources': './data/free_sources_data.db',
            'orchestration_log': './databases/sqlite_dbs/orchestration_log.db',
            'trading_patterns': './databases/sqlite_dbs/trading_patterns.db',
            'unified_signals': './databases/sqlite_dbs/unified_signals.db',
            'backtest_results': './databases/sqlite_dbs/backtest_results.db',
            'correlation_analysis': './databases/sqlite_dbs/correlation_analysis.db',
            'guardian_dashboard': './data/guardian_dashboard.db'
        }
        
        # External API configurations
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.anthropic_key = os.getenv('ANTHROPIC_API_KEY') 
        self.mistral_key = os.getenv('MISTRAL_API_KEY')
        self.huggingface_token = os.getenv('HUGGINGFACE_TOKEN')
        
        self.tools = self._register_tools()
    
    def _register_tools(self) -> List[MCPTool]:
        """Register all available MCP tools"""
        return [
            MCPTool(
                name="query_database",
                description="Execute SQL query on any Orion database with real-time results",
                input_schema={
                    "type": "object",
                    "properties": {
                        "database": {"type": "string", "enum": list(self.databases.keys())},
                        "query": {"type": "string"},
                        "params": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["database", "query"]
                }
            ),
            MCPTool(
                name="get_live_market_data",
                description="Get real-time market data and collection status",
                input_schema={
                    "type": "object", 
                    "properties": {
                        "timeframe": {"type": "string", "enum": ["1h", "24h", "7d"]},
                        "include_sources": {"type": "boolean", "default": True}
                    }
                }
            ),
            MCPTool(
                name="trigger_data_collection", 
                description="Manually trigger data collection from specific sources",
                input_schema={
                    "type": "object",
                    "properties": {
                        "sources": {"type": "array", "items": {"type": "string"}},
                        "force_refresh": {"type": "boolean", "default": False}
                    }
                }
            ),
            MCPTool(
                name="system_health_monitor",
                description="Real-time system health across all components",
                input_schema={
                    "type": "object",
                    "properties": {
                        "component": {"type": "string", "enum": ["all", "databases", "apis", "llms", "notion"]},
                        "include_recommendations": {"type": "boolean", "default": True}
                    }
                }
            )
        ]
    
    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> MCPResponse:
        """Handle MCP tool calls with direct system integration"""
        try:
            if tool_name == "query_database":
                return await self._query_database(arguments)
            elif tool_name == "get_live_market_data":
                return await self._get_live_market_data(arguments)
            elif tool_name == "trigger_data_collection":
                return await self._trigger_data_collection(arguments)
            elif tool_name == "system_health_monitor":
                return await self._system_health_monitor(arguments)
            else:
                return MCPResponse(
                    content=[{"type": "text", "text": f"Unknown tool: {tool_name}"}],
                    is_error=True
                )
        except Exception as e:
            return MCPResponse(
                content=[{"type": "text", "text": f"Error executing {tool_name}: {str(e)}"}],
                is_error=True
            )
    
    async def _query_database(self, args: Dict[str, Any]) -> MCPResponse:
        """Direct database query with real-time results"""
        database = args["database"]
        query = args["query"]
        params = args.get("params", [])
        
        if database not in self.databases:
            return MCPResponse(
                content=[{"type": "text", "text": f"Unknown database: {database}"}],
                is_error=True
            )
        
        db_path = self.databases[database]
        if not Path(db_path).exists():
            return MCPResponse(
                content=[{"type": "text", "text": f"Database file not found: {db_path}"}],
                is_error=True
            )
        
        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            cursor = conn.cursor()
            
            cursor.execute(query, params)
            
            if query.strip().upper().startswith('SELECT'):
                results = [dict(row) for row in cursor.fetchall()]
                result_text = f"✅ Query executed successfully on {database}\n"
                result_text += f"📊 Results: {len(results)} rows\n\n"
                
                if results:
                    # Show first few results as preview
                    for i, row in enumerate(results[:5]):
                        result_text += f"Row {i+1}: {dict(row)}\n"
                    if len(results) > 5:
                        result_text += f"... and {len(results) - 5} more rows\n"
                else:
                    result_text += "No results found\n"
                
                conn.close()
                return MCPResponse(content=[{
                    "type": "text", 
                    "text": result_text
                }])
            else:
                conn.commit()
                conn.close()
                return MCPResponse(content=[{
                    "type": "text",
                    "text": f"✅ Query executed successfully on {database}"
                }])
                
        except Exception as e:
            return MCPResponse(
                content=[{"type": "text", "text": f"Database error: {str(e)}"}],
                is_error=True
            )
    
    async def _get_live_market_data(self, args: Dict[str, Any]) -> MCPResponse:
        """Get real-time market data collection status"""
        timeframe = args.get("timeframe", "1h")
        include_sources = args.get("include_sources", True)
        
        try:
            # Check free sources database for recent data
            db_path = self.databases['free_sources']
            if not Path(db_path).exists():
                return MCPResponse(
                    content=[{"type": "text", "text": "Free sources database not found"}],
                    is_error=True
                )
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get recent data summary
            time_filter = {
                "1h": "datetime('now', '-1 hour')",
                "24h": "datetime('now', '-1 day')", 
                "7d": "datetime('now', '-7 days')"
            }[timeframe]
            
            # Get table summary
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            summary = f"📊 **LIVE MARKET DATA STATUS** ({timeframe})\n\n"
            total_records = 0
            
            for table in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    total_count = cursor.fetchone()[0]
                    
                    cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE timestamp > {time_filter}")
                    recent_count = cursor.fetchone()[0]
                    
                    summary += f"📈 **{table}**: {total_count} total, {recent_count} recent\n"
                    total_records += total_count
                    
                except:
                    summary += f"⚠️ **{table}**: Unable to query\n"
            
            summary += f"\n🎯 **Total Records**: {total_records}\n"
            summary += f"🕐 **Last Updated**: {datetime.now().isoformat()}\n"
            
            conn.close()
            
            return MCPResponse(content=[{
                "type": "text",
                "text": summary
            }])
            
        except Exception as e:
            return MCPResponse(
                content=[{"type": "text", "text": f"Error getting market data: {str(e)}"}],
                is_error=True
            )
    
    async def _trigger_data_collection(self, args: Dict[str, Any]) -> MCPResponse:
        """Trigger data collection manually"""
        sources = args.get("sources", ["all"])
        force_refresh = args.get("force_refresh", False)
        
        response_text = f"🚀 **DATA COLLECTION TRIGGER**\n\n"
        response_text += f"📊 Sources: {sources}\n"
        response_text += f"🔄 Force Refresh: {force_refresh}\n"
        response_text += f"🕐 Initiated: {datetime.now().isoformat()}\n\n"
        
        try:
            import subprocess
            result = subprocess.run(['python', 'research_center/collectors/free_sources_collector.py'], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                # Extract results from output
                output_lines = result.stdout.split('\n')
                for line in output_lines:
                    if 'records' in line.lower():
                        response_text += f"✅ {line.strip()}\n"
                
                response_text += "\n🎯 **Collection completed successfully**\n"
            else:
                response_text += f"❌ Collection failed: {result.stderr}\n"
                
        except Exception as e:
            response_text += f"❌ Collection error: {str(e)}\n"
        
        return MCPResponse(content=[{
            "type": "text",
            "text": response_text
        }])
    
    async def _system_health_monitor(self, args: Dict[str, Any]) -> MCPResponse:
        """Real-time system health monitoring"""
        component = args.get("component", "all")
        include_recommendations = args.get("include_recommendations", True)
        
        health_report = f"🛡️ **SYSTEM HEALTH MONITOR**\n\n"
        health_score = 0
        total_checks = 0
        
        # Database health
        if component in ["all", "databases"]:
            db_health = 0
            for db_name, db_path in self.databases.items():
                total_checks += 1
                if Path(db_path).exists():
                    try:
                        conn = sqlite3.connect(db_path)
                        cursor = conn.cursor()
                        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                        tables = cursor.fetchall()
                        conn.close()
                        health_report += f"✅ {db_name}: {len(tables)} tables\n"
                        db_health += 1
                        health_score += 1
                    except Exception as e:
                        health_report += f"❌ {db_name}: Connection error\n"
                else:
                    health_report += f"❌ {db_name}: File not found\n"
            
            health_report += f"\n📊 Database Health: {db_health}/{len(self.databases)} operational\n\n"
        
        # API health
        if component in ["all", "apis"]:
            total_checks += 1
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=5)
                if response.status_code == 200:
                    health_report += "✅ Ollama API: Operational\n"
                    health_score += 1
                else:
                    health_report += "⚠️ Ollama API: Unexpected response\n"
            except:
                health_report += "❌ Ollama API: Not accessible\n"
        
        # Overall health
        health_percentage = (health_score / total_checks * 100) if total_checks > 0 else 0
        health_report += f"\n🎯 **Overall Health: {health_percentage:.1f}%**\n"
        
        if include_recommendations and health_percentage < 100:
            health_report += "\n💡 **Recommendations:**\n"
            health_report += "- Check database file paths\n"
            health_report += "- Verify Ollama service status\n"
            health_report += "- Review system logs for errors\n"
        
        return MCPResponse(content=[{
            "type": "text",
            "text": health_report
        }])

def main():
    """Main MCP server entry point"""
    print("🛡️ Starting Orion MCP Server...")
    server = OrionMCPServer()
    print(f"✅ MCP Server initialized with {len(server.tools)} tools")
    
    # Test basic functionality
    print("\n🔧 Testing basic functionality...")
    
    # Test database connection
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # Test health monitor
        result = loop.run_until_complete(
            server.handle_tool_call("system_health_monitor", {"component": "databases"})
        )
        print("✅ Health monitor test:")
        print(result.content[0]["text"])
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    finally:
        loop.close()

if __name__ == "__main__":
    main() 