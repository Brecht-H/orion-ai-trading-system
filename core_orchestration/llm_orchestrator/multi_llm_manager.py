from typing import Dict, List, Any, Optional
import os
from enum import Enum
from anthropic import Anthropic
import google.generativeai as genai
from openai import OpenAI
import replicate
from dotenv import load_dotenv

class ModelType(Enum):
    CLAUDE = "claude"
    MISTRAL = "mistral"
    GEMINI = "gemini"
    GPT4 = "gpt4"
    OLLAMA = "ollama"

class TaskType(Enum):
    ARCHITECTURE_DESIGN = "architecture_design"
    CODE_IMPLEMENTATION = "code_implementation"
    CODE_REVIEW = "code_review"
    MARKET_ANALYSIS = "market_analysis"
    STRATEGY_OPTIMIZATION = "strategy_optimization"
    RISK_ASSESSMENT = "risk_assessment"

class LLMOrchestrator:
    def __init__(self):
        load_dotenv()
        
        # Initialize API clients
        self.anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        
        # Model specializations
        self.model_specializations = {
            ModelType.CLAUDE: [
                TaskType.ARCHITECTURE_DESIGN,
                TaskType.CODE_REVIEW,
                TaskType.RISK_ASSESSMENT
            ],
            ModelType.GPT4: [
                TaskType.CODE_IMPLEMENTATION,
                TaskType.STRATEGY_OPTIMIZATION
            ],
            ModelType.GEMINI: [
                TaskType.MARKET_ANALYSIS
            ]
        }
        
    def get_best_model_for_task(self, task_type: TaskType) -> ModelType:
        """Determines the best model for a specific task type."""
        for model, tasks in self.model_specializations.items():
            if task_type in tasks:
                return model
        return ModelType.CLAUDE  # Default to Claude for unknown tasks
    
    async def execute_task(self, task_type: TaskType, prompt: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Executes a task using the most appropriate AI model
        
        Args:
            task_type: Type of task to execute
            prompt: The prompt for the AI model
            context: Additional context for the task
            
        Returns:
            Dictionary containing the task results
        """
        model = self.get_best_model_for_task(task_type)
        
        try:
            if model == ModelType.CLAUDE:
                response = await self._execute_claude_task(prompt, context)
            elif model == ModelType.GPT4:
                response = await self._execute_gpt4_task(prompt, context)
            elif model == ModelType.GEMINI:
                response = await self._execute_gemini_task(prompt, context)
            else:
                raise ValueError(f"Unsupported model type: {model}")
                
            return {
                "success": True,
                "model_used": model.value,
                "task_type": task_type.value,
                "response": response
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model_used": model.value,
                "task_type": task_type.value
            }
    
    async def _execute_claude_task(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Execute a task using Claude"""
        message = self.anthropic.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        return message.content
    
    async def _execute_gpt4_task(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Execute a task using GPT-4"""
        response = self.openai.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        return response.choices[0].message.content
    
    async def _execute_gemini_task(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Execute a task using Gemini"""
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    
    def create_task_prompt(self, task_type: TaskType, **kwargs) -> str:
        """Creates a specialized prompt based on task type"""
        if task_type == TaskType.ARCHITECTURE_DESIGN:
            return self._create_architecture_prompt(**kwargs)
        elif task_type == TaskType.CODE_IMPLEMENTATION:
            return self._create_implementation_prompt(**kwargs)
        elif task_type == TaskType.MARKET_ANALYSIS:
            return self._create_market_analysis_prompt(**kwargs)
        # Add more specialized prompt creators as needed
        
    def _create_architecture_prompt(self, **kwargs) -> str:
        return f"""
        Please design a scalable architecture for the following components:
        
        Requirements:
        {kwargs.get('requirements', '')}
        
        Existing Components:
        {kwargs.get('existing_components', '')}
        
        Focus on:
        1. Modularity and extensibility
        2. Clear separation of concerns
        3. Efficient data flow
        4. Error handling and monitoring
        5. Security considerations
        """
    
    def _create_implementation_prompt(self, **kwargs) -> str:
        return f"""
        Please implement the following component:
        
        Specification:
        {kwargs.get('specification', '')}
        
        Requirements:
        {kwargs.get('requirements', '')}
        
        Please provide:
        1. Complete implementation code
        2. Unit tests
        3. Documentation
        4. Error handling
        5. Performance considerations
        """
    
    def _create_market_analysis_prompt(self, **kwargs) -> str:
        return f"""
        Please analyze the following market data:
        
        Data:
        {kwargs.get('market_data', '')}
        
        Timeframe:
        {kwargs.get('timeframe', '')}
        
        Focus on:
        1. Key trends and patterns
        2. Risk factors
        3. Trading opportunities
        4. Market sentiment
        5. Technical indicators
        """ 