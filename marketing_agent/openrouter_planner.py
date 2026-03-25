"""
OpenRouter-Powered Marketing Planning Assistant.

This module provides planning capabilities using OpenRouter API (OpenAI compatible).
"""

import os
import json
from typing import Dict, List, Any
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

class OpenRouterPlanner:
    """
    Advanced marketing planner powered by OpenRouter (OpenAI-compatible).
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self.model_name = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-001")
        
        if self.api_key:
            self.llm = ChatOpenAI(
                model=self.model_name,
                api_key=self.api_key,
                base_url=self.base_url,
                temperature=0.7
            )
        else:
            self.llm = None

    def interpret_goal_with_ai(self, marketing_goal: str, duration_days: int = 14, custom_instructions: str = "") -> Dict[str, Any]:
        if not self.llm:
            return {"error": "LLM not initialized"}
            
        prompt = f"""
Analyze this marketing goal and provide a structured analysis in JSON format:

Marketing Goal: "{marketing_goal}"
Target Duration: {duration_days} days
Custom Instructions: "{custom_instructions if custom_instructions else "None provided"}"

Provide:
1. Primary objective (one sentence)
2. Focus areas (list of 3-5 key areas)
3. Target audience (description)
4. Success metrics (list of 3-5 measurable KPIs)
5. Anticipated challenges (list of 2-3 potential obstacles)
6. Recommended approach (brief strategy description)
7. Complexity level (Low/Medium/High)
8. Estimated timeline (Must respect the target of {duration_days} days)

Format as valid JSON with these exact keys:
{{
  "primary_objective": "...",
  "focus_areas": [],
  "target_audience": "...",
  "success_metrics": [],
  "challenges": [],
  "recommended_approach": "...",
  "complexity": "...",
  "estimated_timeline": "{duration_days} days",
  "target_duration_days": {duration_days},
  "custom_constraints": "{custom_instructions}",
  "original_goal": "{marketing_goal}"
}}
"""
        response = self.llm.invoke([HumanMessage(content=prompt)])
        content = response.content
        
        # Strip potential markdown formatting
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()
            
        return json.loads(content)

    def decompose_tasks_with_ai(self, interpreted_goal: Dict[str, Any]) -> List[Dict[str, Any]]:
        if not self.llm:
            return []
            
        goal_text = interpreted_goal.get('original_goal', 'Marketing planning')
        target_days = interpreted_goal.get('target_duration_days', 14)
        constraints = interpreted_goal.get('custom_constraints', 'None')
        
        prompt = f"""
Based on this marketing goal, create a detailed task breakdown:

Goal: {goal_text}
Target Duration: {target_days} days
Focus Areas: {interpreted_goal.get('focus_areas', [])}
Custom Constraints: {constraints}

Generate 5-10 specific tasks. For each task provide:
1. Task name (short, action-oriented)
2. Description (what and why)
3. Required tools from: [CompetitorResearchTool, AdDatabaseTool, BudgetCheckerTool, MarketTrendTool]
4. Estimated duration in days (Must sum up logically to approx {target_days} days)
5. Dependencies (task numbers that must be completed first, or empty list)
6. Deliverables (tangible outputs)

Format as a JSON array of objects with these exact keys:
[
  {{
    "task_id": 1,
    "task_name": "...",
    "description": "...",
    "required_tools": [],
    "estimated_days": 1,
    "dependencies": [],
    "deliverables": []
  }}
]

Ensure logical dependencies and sequential flow. The total critical path duration should be around {target_days} days.
"""
        response = self.llm.invoke([HumanMessage(content=prompt)])
        content = response.content
        
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()
            
        return json.loads(content)
