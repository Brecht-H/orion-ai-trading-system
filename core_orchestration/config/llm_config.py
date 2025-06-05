from typing import Dict, Any
from enum import Enum

class ModelProvider(Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GOOGLE = "google"
    MISTRAL = "mistral"
    OLLAMA = "ollama"

# Model configurations
MODEL_CONFIGS: Dict[str, Dict[str, Any]] = {
    "claude-3-opus": {
        "provider": ModelProvider.ANTHROPIC,
        "model_name": "claude-3-opus-20240229",
        "max_tokens": 4000,
        "temperature": 0.7,
        "specializations": [
            "architecture_design",
            "code_review",
            "risk_assessment"
        ]
    },
    "gpt-4-turbo": {
        "provider": ModelProvider.OPENAI,
        "model_name": "gpt-4-turbo-preview",
        "max_tokens": 4000,
        "temperature": 0.7,
        "specializations": [
            "code_implementation",
            "strategy_optimization"
        ]
    },
    "gemini-pro": {
        "provider": ModelProvider.GOOGLE,
        "model_name": "gemini-pro",
        "temperature": 0.7,
        "specializations": [
            "market_analysis",
            "data_analysis"
        ]
    },
    "mistral-large": {
        "provider": ModelProvider.MISTRAL,
        "model_name": "mistral-large-latest",
        "max_tokens": 4000,
        "temperature": 0.7,
        "specializations": [
            "code_generation",
            "technical_analysis"
        ]
    }
}

# Task-specific configurations
TASK_CONFIGS: Dict[str, Dict[str, Any]] = {
    "architecture_design": {
        "preferred_model": "claude-3-opus",
        "fallback_model": "gpt-4-turbo",
        "max_retries": 3,
        "timeout": 30
    },
    "code_implementation": {
        "preferred_model": "gpt-4-turbo",
        "fallback_model": "claude-3-opus",
        "max_retries": 3,
        "timeout": 30
    },
    "market_analysis": {
        "preferred_model": "gemini-pro",
        "fallback_model": "gpt-4-turbo",
        "max_retries": 3,
        "timeout": 20
    },
    "risk_assessment": {
        "preferred_model": "claude-3-opus",
        "fallback_model": "gpt-4-turbo",
        "max_retries": 3,
        "timeout": 20
    },
    "strategy_optimization": {
        "preferred_model": "gpt-4-turbo",
        "fallback_model": "claude-3-opus",
        "max_retries": 3,
        "timeout": 30
    },
    "code_review": {
        "preferred_model": "claude-3-opus",
        "fallback_model": "gpt-4-turbo",
        "max_retries": 3,
        "timeout": 30
    },
    "technical_analysis": {
        "preferred_model": "mistral-large",
        "fallback_model": "gemini-pro",
        "max_retries": 3,
        "timeout": 20
    }
}

# Prompt templates for different tasks
PROMPT_TEMPLATES: Dict[str, str] = {
    "architecture_design": """
    Please design a scalable architecture for the following component:
    
    Component: {component_name}
    Requirements:
    {requirements}
    
    Existing Components:
    {existing_components}
    
    Focus on:
    1. Modularity and extensibility
    2. Clear separation of concerns
    3. Efficient data flow
    4. Error handling and monitoring
    5. Security considerations
    """,
    
    "market_analysis": """
    Please analyze the following market data:
    
    Asset: {asset}
    Timeframe: {timeframe}
    
    Market Data:
    {market_data}
    
    Current Positions:
    {current_positions}
    
    Focus on:
    1. Key trends and patterns
    2. Support and resistance levels
    3. Volume analysis
    4. Market sentiment
    5. Risk factors
    """,
    
    "risk_assessment": """
    Please assess the risk for the following trading scenario:
    
    Asset: {asset}
    Position Size: {position_size}
    Current Market Conditions:
    {market_conditions}
    
    Portfolio Context:
    {portfolio_context}
    
    Focus on:
    1. Position sizing risks
    2. Market volatility risks
    3. Correlation risks
    4. Liquidity risks
    5. Overall portfolio impact
    """
}

# Error handling and retry configurations
ERROR_HANDLING_CONFIG = {
    "max_retries": 3,
    "retry_delay": 1,  # seconds
    "exponential_backoff": True,
    "fallback_strategy": "use_alternative_model",  # or "skip_task"
    "error_notification_threshold": 5  # number of errors before notification
}

# Rate limiting configurations
RATE_LIMITING_CONFIG = {
    ModelProvider.ANTHROPIC: {
        "requests_per_minute": 50,
        "tokens_per_minute": 100000
    },
    ModelProvider.OPENAI: {
        "requests_per_minute": 60,
        "tokens_per_minute": 90000
    },
    ModelProvider.GOOGLE: {
        "requests_per_minute": 60,
        "tokens_per_minute": 100000
    },
    ModelProvider.MISTRAL: {
        "requests_per_minute": 50,
        "tokens_per_minute": 80000
    }
} 