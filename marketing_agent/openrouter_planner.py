"""
OpenRouter-Powered Marketing Planning Assistant.

This module provides planning capabilities using OpenRouter API (OpenAI compatible).
"""

import os
import json
from typing import Dict, List, Any
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

class OpenRouterPlanner:
    """
    Advanced marketing planner powered by OpenRouter (OpenAI-compatible).
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self.model_name = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-001")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "2000"))
        
        if self.api_key:
            self.llm = ChatOpenAI(
                model=self.model_name,
                api_key=self.api_key,
                base_url=self.base_url,
                temperature=0.7,
                max_tokens=self.max_tokens
            )
        else:
            self.llm = None

    def _clean_and_parse_json(self, content: str) -> Any:
        """Helper to extract and parse JSON from AI response robustly."""
        # Strip potential markdown formatting
        content = content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        try:
            # Use strict=False to allow control characters (like literal newlines)
            return json.loads(content, strict=False)
        except json.JSONDecodeError as e:
            print(f"⚠️ Initial JSON parse failed: {e}. Attempting cleanup...")
            # Try a more aggressive cleanup if simple parse fails
            try:
                # Remove common non-printable characters except newlines/tabs
                # which are handled by strict=False
                import re
                # This helps with some edge cases where the AI might include invalid escapes
                return json.loads(content, strict=False)
            except:
                raise e

    def generate_full_plan_with_ai(self, marketing_goal: str, duration_days: int = 14, custom_instructions: str = "") -> Dict[str, Any]:
        """Combined call to interpret goal and decompose tasks in a single request to save tokens."""
        if not self.llm:
            return {"error": "LLM not initialized"}

        prompt = f"""
Create a complete marketing plan in JSON format.
Goal: {marketing_goal}
Duration: {duration_days} days
Instructions: {custom_instructions if custom_instructions else "None"}

Requirements:
- Plan MUST span exactly {duration_days} days.
- Include 7-12 sequential tasks.
- Sum of critical path MUST be {duration_days} days.
- Tasks start today: {datetime.now().strftime('%Y-%m-%d')}

Return JSON with these exact keys:
{{
  "interpretation": {{
    "primary_objective": "...",
    "focus_areas": [],
    "target_audience": "...",
    "success_metrics": [],
    "challenges": [],
    "recommended_approach": "...",
    "complexity": "Low/Medium/High",
    "target_duration_days": {duration_days}
  }},
  "tasks": [
    {{
      "task_id": 1,
      "task_name": "...",
      "description": "...",
      "required_tools": ["CompetitorResearchTool", "AdDatabaseTool", "BudgetCheckerTool", "MarketTrendTool"],
      "estimated_days": 1,
      "dependencies": [],
      "deliverables": [],
      "start_date": "YYYY-MM-DD",
      "end_date": "YYYY-MM-DD"
    }}
  ]
}}
"""
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return self._clean_and_parse_json(response.content)

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
        return self._clean_and_parse_json(response.content)

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

CRITICAL REQUIREMENT: The total duration of this project MUST be exactly {target_days} days.
The tasks you generate must span the entire {target_days} day period from Day 1 to Day {target_days}.

Generate 7-12 specific tasks. For each task provide:
1. Task name (short, action-oriented)
2. Description (what and why)
3. Required tools from: [CompetitorResearchTool, AdDatabaseTool, BudgetCheckerTool, MarketTrendTool]
4. Estimated duration in days (Ensure the critical path sums up EXACTLY to {target_days} days)
5. Dependencies (task numbers that must be completed first, or empty list)
6. Deliverables (tangible outputs)
7. Start Date (YYYY-MM-DD, assume project starts today: {datetime.now().strftime('%Y-%m-%d')})
8. End Date (YYYY-MM-DD, based on the duration and dependencies)

Format as a JSON array of objects with these exact keys:
[
  {{
    "task_id": 1,
    "task_name": "...",
    "description": "...",
    "required_tools": [],
    "estimated_days": 1,
    "dependencies": [],
    "deliverables": [],
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD"
  }}
]

Ensure logical dependencies and sequential flow. The plan MUST be comprehensive and cover all {target_days} days.
"""
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return self._clean_and_parse_json(response.content)
