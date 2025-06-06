#!/usr/bin/env python3
"""
🧪 MCP Integration Test for Orion Project
Tests all MCP tools and database access
"""

import asyncio
import sys
import os
sys.path.append('./mcp')

from orion_mcp_server import OrionMCPServer

async def test_mcp_integration():
    """Test all MCP tools and database connections"""
    print("🧪 Testing Orion MCP Integration...")
    
    server = OrionMCPServer()
    
    # Test 1: System Health Monitor
    print("\n1️⃣ Testing System Health Monitor...")
    health_result = await server.handle_tool_call("system_health_monitor", {
        "component": "all",
        "include_recommendations": True
    })
    
    if not health_result.is_error:
        print("✅ System health check passed")
        print(health_result.content[0]['text'][:200] + "...")
    else:
        print("❌ System health check failed")
        print(health_result.content[0]['text'])
    
    # Test 2: Database Query
    print("\n2️⃣ Testing Database Query...")
    db_result = await server.handle_tool_call("query_database", {
        "database": "free_sources",
        "query": "SELECT name FROM sqlite_master WHERE type='table' LIMIT 3"
    })
    
    if not db_result.is_error:
        print("✅ Database query successful")
        print(db_result.content[0]['text'][:200] + "...")
    else:
        print("❌ Database query failed")
        print(db_result.content[0]['text'])
    
    # Test 3: Live Market Data
    print("\n3️⃣ Testing Live Market Data...")
    market_result = await server.handle_tool_call("get_live_market_data", {
        "timeframe": "1h",
        "include_sources": True
    })
    
    if not market_result.is_error:
        print("✅ Market data access successful")
        print(market_result.content[0]['text'][:200] + "...")
    else:
        print("❌ Market data access failed")
        print(market_result.content[0]['text'])
    
    # Test 4: Data Collection Trigger
    print("\n4️⃣ Testing Data Collection Trigger...")
    collection_result = await server.handle_tool_call("trigger_data_collection", {
        "sources": ["test"],
        "force_refresh": False
    })
    
    if not collection_result.is_error:
        print("✅ Data collection trigger successful")
        print(collection_result.content[0]['text'][:200] + "...")
    else:
        print("❌ Data collection trigger failed")
        print(collection_result.content[0]['text'])
    
    print("\n🎯 MCP Integration Test Complete!")
    print(f"📊 Tools Available: {len(server.tools)}")
    print(f"🗄️ Databases Configured: {len(server.databases)}")
    
    return True

if __name__ == "__main__":
    asyncio.run(test_mcp_integration()) 