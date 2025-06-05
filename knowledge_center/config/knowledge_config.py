#!/usr/bin/env python3
"""
Orion Knowledge Center Configuration
Loads API keys from environment and configures storage strategy
"""

import os
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class StorageConfig:
    """Storage configuration for hybrid approach"""
    # Local storage (MacBook Air M2)
    local_cache_dir: Path = Path("orion_core/data/knowledge_cache")
    local_cache_max_size: str = "5GB"
    local_cache_documents: int = 1000
    
    # Remote storage (Mac Mini)
    remote_host: str = "192.168.68.103"
    remote_port: str = "5000"
    remote_storage_dir: str = "/Users/admin/orion_knowledge_repository"
    remote_max_size: str = "750GB"
    
    # Database paths
    metadata_db: Path = Path("orion_core/data/knowledge_cache/metadata.db")
    vector_db: Path = Path("orion_core/data/knowledge_cache/chroma_cache")

@dataclass
class APIConfig:
    """API configuration with all available keys"""
    
    def __init__(self):
        # Load from actual environment variables based on env temp.md
        self.openai_api_key = os.getenv("API_Openai_com")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.groq_api_key = os.getenv("API_Groq")
        self.mistral_api_key = os.getenv("API_Mistral")
        self.huggingface_token = os.getenv("HUGGINGFACE_TOKEN")
        self.together_ai_key = os.getenv("TOGETHER_AI_KEY")
        self.google_gemini_api = os.getenv("Google_Gemini_API")
        
        # Data source APIs
        self.coingecko_api_key = "cg-8g2gdnxplnpm6b6nqazpejk1"
        self.newsapi_key = "f791f3b18b05439fb92d71e308faa40a"
        self.coindesk_api_key = "12112a159566b2711232ad4b650e2f8f598766bd2cb106d1587bf760d6f1732d"
        self.newsdata_io_key = "pub_0713e21f691d411eb809569c70146f05"
        self.reddit_api_key = "FIc5ohKuB2vtKNzEoHXO_-HPig7uLw"
        
        # Social media APIs
        self.twitter_api_key = "FBHbXj6Ovy1dU3HYEDXBAq0YG"
        self.twitter_api_secret = "2Dfwora07PFmhtmEYghYSVj5myKnN5BRyXROk6Ka718b59Gnfj"
        self.twitter_bearer_token = ""  # Needs to be set
        
        # Infrastructure
        self.notion_token = os.getenv("NOTION_TOKEN")
        self.github_token = os.getenv("Github_token")
        
        # Local LLM configuration
        self.ollama_host = "http://localhost:11434"
        self.ollama_models = [
            "mistral:7b", "llama2:13b", "codellama:7b", 
            "phi3:mini", "qwen2:7b", "deepseek-coder:6.7b"
        ]

@dataclass 
class IngestionConfig:
    """Configuration for knowledge ingestion sources"""
    
    # ArXiv categories for research papers
    arxiv_categories = [
        'cs.AI',      # Artificial Intelligence
        'cs.LG',      # Machine Learning  
        'cs.CL',      # Computation and Language
        'q-fin.TR',   # Trading and Market Microstructure
        'q-fin.CP',   # Computational Finance
        'q-fin.PM',   # Portfolio Management
        'stat.ML',    # Machine Learning (Statistics)
        'econ.EM'     # Econometrics
    ]
    
    # RSS feeds for news ingestion
    rss_feeds = [
        'https://cointelegraph.com/rss',
        'https://coindesk.com/arc/outboundfeeds/rss/',
        'https://decrypt.co/feed',
        'https://www.theblock.co/rss.xml',
        'https://bitcoinmagazine.com/feed'
    ]
    
    # GitHub repositories to monitor
    github_repos = [
        'ccxt/ccxt',                    # Crypto trading
        'freqtrade/freqtrade',         # Trading bot
        'jesse-ai/jesse',              # Algorithmic trading
        'microsoft/qlib',              # Quantitative trading
        'ta-lib/ta-lib-python',        # Technical analysis
        'binance/binance-connector-python',  # Binance API
        'pycaret/pycaret',             # ML automation
        'microsoft/DialoGPT',          # Conversational AI
        'openai/openai-python'         # OpenAI Python
    ]
    
    # YouTube channels for educational content
    youtube_channels = [
        'UCFCOZKTxgWhyX6oy6kBp7qw',  # MIT OpenCourseWare
        'UC7cs8q-gJRlGwj4A8OmCmXg',  # Andrew Ng
        'UCcIXc5mJsHVYTZR1maL5l9w',  # StatQuest
        'UCiT9RITQ9PW6BhXK0y2jaeg'   # Ken Jee (Data Science)
    ]

@dataclass
class ProcessingConfig:
    """Configuration for document processing"""
    
    # Quality thresholds
    min_content_length = 100
    max_content_length = 50000
    min_credibility_score = 0.3
    
    # Categorization rules
    category_keywords = {
        'trading': ['trading', 'strategy', 'backtest', 'portfolio', 'risk'],
        'research': ['paper', 'study', 'analysis', 'research', 'academic'],
        'news': ['news', 'update', 'announcement', 'market', 'price'],
        'technology': ['blockchain', 'crypto', 'defi', 'smart contract', 'protocol'],
        'regulation': ['regulation', 'legal', 'compliance', 'policy', 'government'],
        'education': ['tutorial', 'guide', 'learn', 'course', 'explanation']
    }
    
    # Priority scoring weights
    priority_weights = {
        'source_credibility': 0.3,
        'content_relevance': 0.4, 
        'recency': 0.2,
        'user_engagement': 0.1
    }

@dataclass
class LLMConfig:
    """LLM orchestration configuration"""
    
    # Model routing based on task complexity and cost
    model_routing = {
        'classification': 'ollama_mistral',      # Fast, local
        'summarization': 'ollama_llama2',        # Good quality, local
        'analysis': 'groq_mixtral',              # Fast API, good balance
        'complex_reasoning': 'anthropic_claude', # High quality, expensive
        'critical_decisions': 'openai_gpt4',     # Highest quality, most expensive
        'code_analysis': 'ollama_codellama',     # Specialized, local
        'embeddings': 'huggingface_local'       # Local sentence transformers
    }
    
    # Cost limits (monthly)
    cost_limits = {
        'openai': 100.0,      # €100/month limit
        'anthropic': 50.0,    # €50/month limit  
        'groq': 25.0,         # €25/month limit
        'mistral': 25.0,      # €25/month limit
        'together': 25.0,     # €25/month limit
        'total_monthly': 225.0 # €225/month total limit
    }
    
    # Fallback chain
    fallback_chain = [
        'ollama_mistral',     # Primary fallback (local)
        'groq_mixtral',       # Secondary fallback (API)
        'huggingface_local'   # Final fallback (local)
    ]

class KnowledgeCenterMainConfig:
    """Main configuration class combining all components"""
    
    def __init__(self):
        self.storage = StorageConfig()
        self.apis = APIConfig()
        self.ingestion = IngestionConfig()
        self.processing = ProcessingConfig()
        self.llm = LLMConfig()
        
        # Ensure directories exist
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories"""
        directories = [
            self.storage.local_cache_dir,
            self.storage.local_cache_dir / "chroma_cache",
            self.storage.local_cache_dir / "remote_sync",
            Path("orion_core/data/logs"),
            Path("orion_core/data/knowledge_base/input_queue/pdf"),
            Path("orion_core/data/knowledge_base/input_queue/docx"),
            Path("orion_core/data/knowledge_base/input_queue/txt"),
            Path("orion_core/data/knowledge_base/input_queue/urls"),
            Path("orion_core/data/knowledge_base/processed"),
            Path("orion_core/data/knowledge_base/archive")
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_api_status(self) -> Dict[str, str]:
        """Get status of all configured APIs"""
        api_status = {}
        
        # Check LLM APIs
        llm_apis = {
            'OpenAI': self.apis.openai_api_key,
            'Anthropic': self.apis.anthropic_api_key,
            'Groq': self.apis.groq_api_key,
            'Mistral': self.apis.mistral_api_key,
            'HuggingFace': self.apis.huggingface_token,
            'Together.ai': self.apis.together_ai_key,
            'Google Gemini': self.apis.google_gemini_api
        }
        
        # Check data source APIs
        data_apis = {
            'CoinGecko': self.apis.coingecko_api_key,
            'NewsAPI': self.apis.newsapi_key,
            'CoinDesk': self.apis.coindesk_api_key,
            'NewsData.io': self.apis.newsdata_io_key,
            'Reddit': self.apis.reddit_api_key,
            'Twitter': self.apis.twitter_api_key
        }
        
        # Check infrastructure APIs
        infra_apis = {
            'Notion': self.apis.notion_token,
            'GitHub': self.apis.github_token
        }
        
        all_apis = {**llm_apis, **data_apis, **infra_apis}
        
        for api_name, api_key in all_apis.items():
            if api_key and len(api_key) > 10:
                api_status[api_name] = "✅ Configured"
            else:
                api_status[api_name] = "❌ Missing"
        
        return api_status
    
    def get_storage_info(self) -> Dict[str, Any]:
        """Get storage configuration info"""
        return {
            'local_cache': {
                'path': str(self.storage.local_cache_dir),
                'max_size': self.storage.local_cache_max_size,
                'max_documents': self.storage.local_cache_documents
            },
            'remote_repository': {
                'host': self.storage.remote_host,
                'port': self.storage.remote_port,
                'path': self.storage.remote_storage_dir,
                'max_size': self.storage.remote_max_size
            }
        }
    
    def get_configuration_summary(self) -> Dict[str, Any]:
        """Get complete configuration summary"""
        return {
            'api_status': self.get_api_status(),
            'storage_info': self.get_storage_info(),
            'ingestion_sources': {
                'arxiv_categories': len(self.ingestion.arxiv_categories),
                'rss_feeds': len(self.ingestion.rss_feeds),
                'github_repos': len(self.ingestion.github_repos),
                'youtube_channels': len(self.ingestion.youtube_channels)
            },
            'llm_models': {
                'routing_strategies': len(self.llm.model_routing),
                'monthly_cost_limit': f"€{self.llm.cost_limits['total_monthly']}",
                'fallback_chain': self.llm.fallback_chain
            },
            'processing_config': {
                'categories': list(self.processing.category_keywords.keys()),
                'min_credibility': self.processing.min_credibility_score
            }
        }

# Singleton instance
config = KnowledgeCenterMainConfig()

if __name__ == "__main__":
    # Test configuration
    import json
    summary = config.get_configuration_summary()
    print(json.dumps(summary, indent=2)) 