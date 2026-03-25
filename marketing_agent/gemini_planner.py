"""
Gemini-Powered Marketing Planning Assistant.

This module provides enhanced planning capabilities using Google's Gemini API.
It offers superior reasoning and more creative marketing strategies.

Setup:
1. Get Gemini API key from: https://makersuite.google.com/app/apikey
2. Set environment variable: GEMINI_API_KEY=your-key-here
3. Run this file directly or import into main.py
"""

import os
import json
from typing import Dict, List, Any
from datetime import datetime

# Try to import Gemini, fall back to mock if not available
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Note: google-generativeai not installed. Using mock mode.")
    print("Install with: pip install google-generativeai")


class GeminiMarketingPlanner:
    """
    Advanced marketing planner powered by Google's Gemini AI.
    
    Provides intelligent goal interpretation, creative task decomposition,
    and strategic marketing recommendations.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the Gemini Marketing Planner.
        
        Args:
            api_key: Gemini API key (optional, can use env var GEMINI_API_KEY)
        """
        # Try to load from environment if not provided
        if not api_key:
            try:
                from dotenv import load_dotenv
                import os
                load_dotenv()
                api_key = os.getenv("GEMINI_API_KEY")
            except:
                pass
        
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = None
        self.chat_session = None
        
        if self.api_key:
            self._initialize_gemini()
            print("✅ Gemini AI initialized with your API key!")
        else:
            print("⚠️  No GEMINI_API_KEY found. Using mock responses.")
            print("   Get your free API key from: https://makersuite.google.com/app/apikey")
    
    def _initialize_gemini(self):
        """Initialize Google's Gemini AI."""
        if not GEMINI_AVAILABLE:
            return
        
        try:
            genai.configure(api_key=self.api_key)
            # Use latest available Gemini model
            self.model = genai.GenerativeModel('models/gemini-2.5-flash')
            
            self.chat_session = self.model.start_chat(history=[])
            print("✅ Gemini AI initialized successfully!")
        except Exception as e:
            print(f"⚠️  Error initializing Gemini: {e}")
            print("   Falling back to mock mode")
    
    def interpret_goal_with_ai(self, marketing_goal: str, duration_days: int = 14, custom_instructions: str = "") -> Dict[str, Any]:
        """
        Use Gemini to intelligently interpret the marketing goal.
        
        Args:
            marketing_goal: User-provided marketing objective
            duration_days: Target duration for the plan
            custom_instructions: Any additional user constraints
            
        Returns:
            Structured interpretation dictionary
        """
        if not self.model:
            # Fallback to simple interpretation
            return self._simple_interpretation(marketing_goal)
        
        try:
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
  "custom_constraints": "{custom_instructions}"
}}
"""
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON from response (handle markdown code blocks)
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            # Parse JSON
            try:
                interpretation = json.loads(response_text)
            except json.JSONDecodeError:
                # If JSON parsing fails, use simple interpretation
                interpretation = self._simple_interpretation(marketing_goal)
            
            # Add original goal
            interpretation['original_goal'] = marketing_goal
            
            return interpretation
            
        except Exception as e:
            print(f"⚠️  AI interpretation error: {e}")
            print("   Using fallback interpretation...")
            return self._simple_interpretation(marketing_goal)
    
    def decompose_tasks_with_ai(self, interpreted_goal: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Use Gemini to create intelligent task breakdown.
        
        Args:
            interpreted_goal: Goal interpretation dictionary
            
        Returns:
            List of task dictionaries
        """
        if not self.model:
            return self._standard_task_decomposition(interpreted_goal)
        
        try:
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
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON from response
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            # Parse JSON
            try:
                tasks = json.loads(response_text)
                # Ensure task IDs are sequential
                for i, task in enumerate(tasks, 1):
                    task['task_id'] = i
                return tasks
            except json.JSONDecodeError:
                return self._standard_task_decomposition(interpreted_goal)
                
        except Exception as e:
            print(f"⚠️  Task decomposition error: {e}")
            return self._standard_task_decomposition(interpreted_goal)
    
    def generate_strategy_recommendations(self, plan: Dict[str, Any]) -> List[str]:
        """
        Use Gemini to generate strategic recommendations.
        
        Args:
            plan: Complete marketing plan
            
        Returns:
            List of strategic recommendations
        """
        if not self.model:
            return ["Review task dependencies carefully", "Monitor resource allocation", "Adjust timeline as needed"]
        
        try:
            goal = plan.get('goal', {}).get('original', 'Marketing goal')
            tasks = plan.get('tasks', [])
            
            prompt = f"""
Review this marketing plan and provide 5-7 strategic recommendations:

Goal: {goal}
Tasks: {len(tasks)} tasks planned

Consider:
- Resource optimization
- Risk mitigation
- Timeline efficiency
- Quality improvements
- Measurement and tracking

Provide recommendations as a JSON array of strings:
["Recommendation 1", "Recommendation 2", ...]
"""
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            try:
                recommendations = json.loads(response_text)
                return recommendations
            except json.JSONDecodeError:
                return ["Review and adjust plan based on feedback", "Monitor progress against milestones"]
                
        except Exception as e:
            print(f"⚠️  Recommendation generation error: {e}")
            return ["Review plan carefully", "Adjust based on stakeholder feedback"]
    
    def _simple_interpretation(self, marketing_goal: str) -> Dict[str, Any]:
        """Simple keyword-based interpretation (fallback)."""
        goal_lower = marketing_goal.lower()
        
        focus_areas = []
        if any(word in goal_lower for word in ['competitor', 'analyze', 'research']):
            focus_areas.append("Competitive Analysis")
        if any(word in goal_lower for word in ['ads', 'advertising', 'promotion']):
            focus_areas.append("Advertising Strategy")
        if any(word in goal_lower for word in ['market', 'industry']):
            focus_areas.append("Market Research")
        if any(word in goal_lower for word in ['trend', 'emerging']):
            focus_areas.append("Trend Analysis")
        if any(word in goal_lower for word in ['strategy', 'plan']):
            focus_areas.append("Strategic Planning")
        
        return {
            "original_goal": marketing_goal,
            "primary_objective": f"Execute marketing initiative focused on {focus_areas[0] if focus_areas else 'general marketing'}",
            "focus_areas": focus_areas or ["General Marketing"],
            "target_audience": "To be determined based on market research",
            "success_metrics": ["Brand awareness", "Engagement rate", "Market penetration"],
            "challenges": ["Resource allocation", "Timeline management", "Competitive dynamics"],
            "recommended_approach": "Systematic analysis followed by strategic implementation",
            "complexity": "Medium",
            "estimated_timeline": "5-7 days"
        }
    
    def _standard_task_decomposition(self, interpreted_goal: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Standard task template (fallback)."""
        return [
            {
                "task_id": 1,
                "task_name": "Identify top competitors",
                "description": "Research and identify key competitors in the market segment",
                "required_tools": ["CompetitorResearchTool"],
                "estimated_days": 1,
                "dependencies": [],
                "deliverables": ["Competitor list with market share data"]
            },
            {
                "task_id": 2,
                "task_name": "Collect competitor advertisements",
                "description": "Gather and catalog competitor ad campaigns across platforms",
                "required_tools": ["AdDatabaseTool"],
                "estimated_days": 1,
                "dependencies": [1],
                "deliverables": ["Ad collection database", "Platform distribution analysis"]
            },
            {
                "task_id": 3,
                "task_name": "Analyze ad messaging",
                "description": "Analyze themes, tone, and messaging strategies in competitor ads",
                "required_tools": ["AdDatabaseTool"],
                "estimated_days": 1,
                "dependencies": [2],
                "deliverables": ["Messaging analysis report", "Theme identification"]
            },
            {
                "task_id": 4,
                "task_name": "Identify market trends",
                "description": "Research current and emerging trends in the industry",
                "required_tools": ["MarketTrendTool"],
                "estimated_days": 1,
                "dependencies": [1],
                "deliverables": ["Trend analysis report", "Opportunity identification"]
            },
            {
                "task_id": 5,
                "task_name": "Generate strategy recommendations",
                "description": "Synthesize findings into actionable strategy recommendations",
                "required_tools": ["BudgetCheckerTool"],
                "estimated_days": 1,
                "dependencies": [3, 4],
                "deliverables": ["Comprehensive strategy document", "Implementation roadmap"]
            }
        ]
    
    def generate_complete_plan(self, marketing_goal: str) -> Dict[str, Any]:
        """
        Generate a complete AI-powered marketing plan.
        
        This is the main method that orchestrates the entire planning process.
        
        Args:
            marketing_goal: High-level marketing objective
            
        Returns:
            Complete plan dictionary with all components
        """
        from planner_agent import SimplePlanner
        from scheduler import ExecutionScheduler
        
        print("\n" + "="*70)
        print("🌟 GEMINI-POWERED MARKETING PLANNING ASSISTANT")
        print("="*70)
        
        # Step 1: AI-powered goal interpretation
        print("\n[Step 1/4] 🤖 AI analyzing your marketing goal...")
        interpreted_goal = self.interpret_goal_with_ai(marketing_goal)
        
        print(f"\n   📍 Primary Objective: {interpreted_goal.get('primary_objective', 'N/A')}")
        print(f"   🎯 Focus Areas: {', '.join(interpreted_goal.get('focus_areas', []))}")
        print(f"   ⏱️  Timeline: {interpreted_goal.get('estimated_timeline', '5-7 days')}")
        
        # Step 2: AI-powered task decomposition
        print("\n[Step 2/4] 📋 Breaking down into actionable tasks...")
        tasks = self.decompose_tasks_with_ai(interpreted_goal)
        
        print(f"\n   ✅ Generated {len(tasks)} tasks:")
        for task in tasks:
            print(f"      • {task['task_name']} ({task['estimated_days']} day(s))")
        
        # Step 3: Resource validation
        print("\n[Step 3/4] 🔧 Validating resources...")
        simple_planner = SimplePlanner()
        resource_validation = simple_planner.validate_resources(tasks)
        
        print("\n   Resource Status:")
        for tool_name, info in resource_validation['tools_status'].items():
            print(f"      ✓ {tool_name}: {info['status']}")
        
        # Step 4: Schedule generation
        print("\n[Step 4/4] 📅 Creating execution timeline...")
        scheduler = ExecutionScheduler()
        schedule = scheduler.generate_schedule(tasks)
        
        # Generate AI recommendations if available
        temp_plan = {
            'goal': interpreted_goal,
            'tasks': tasks
        }
        recommendations = self.generate_strategy_recommendations(temp_plan)
        resource_validation['recommendations'] = recommendations
        
        # Compile complete plan
        complete_plan = {
            'goal': interpreted_goal,
            'tasks': tasks,
            'resources': resource_validation,
            'schedule': schedule,
            'ai_powered': True,
            'model': 'Gemini Pro' if self.model else 'Mock Mode'
        }
        
        # Print final summary
        self._print_enhanced_summary(complete_plan)
        
        return complete_plan
    
    def _print_enhanced_summary(self, plan: Dict[str, Any]):
        """Print enhanced formatted summary."""
        print("\n" + "="*70)
        print("MARKETING PLAN OUTPUT")
        print("="*70)
        
        goal_info = plan['goal']
        print(f"\nGOAL: {goal_info['original_goal']}")
        print(f"Complexity: {goal_info.get('complexity', 'Medium')}")
        print(f"Timeline: {goal_info.get('estimated_timeline', '5-7 days')}")
        
        print("\nTASK BREAKDOWN:")
        for i, task in enumerate(plan['tasks'], 1):
            deps = f" (after task {task['dependencies']})" if task['dependencies'] else ""
            print(f"{i}. {task['task_name']}{deps}")
            print(f"   - {task['description']}")
            print(f"   - Tools: {', '.join(task['required_tools'])}")
            print(f"   - Duration: {task['estimated_days']} day(s)")
            print(f"   - Deliverable: {task['deliverables'][0]}")
        
        print("\nRESOURCES VALIDATED:")
        for tool, info in plan['resources']['tools_status'].items():
            print(f"{tool} -> {info['status']}")
        
        print("\nEXECUTION SCHEDULE:")
        schedule = plan['schedule']
        print(f"Start: {schedule['start_date']}")
        print(f"End: {schedule['end_date']}")
        print(f"Total: {schedule['total_duration_days']} days")
        
        print("\nDay-by-Day:")
        for day in schedule['timeline']:
            task_names = [t['task_name'] for t in day['tasks']]
            if task_names:
                print(f"Day {day['day']}: {', '.join(task_names)}")
        
        print("\nRECOMMENDATIONS:")
        for rec in plan['resources'].get('recommendations', []):
            print(f"- {rec}")
        
        print("\n" + "="*70)


def main():
    """Main entry point for Gemini-powered planner."""
    print("\n" + "="*70)
    print(" " * 15 + "🌟 GEMINI MARKETING PLANNER 🌟")
    print("="*70)
    print()
    print("This AI-powered assistant will create an intelligent marketing")
    print("plan using Google's advanced AI technology.")
    print()
    print("Type 'exit' or 'quit' to end the session.")
    print("-"*70)
    
    # Initialize planner
    planner = GeminiMarketingPlanner()
    
    while True:
        try:
            user_input = input("\nEnter your marketing goal: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                break
            
            if not user_input.strip():
                print("Please enter a valid marketing goal.")
                continue
            
            # Generate plan
            plan = planner.generate_complete_plan(user_input)
            
            print("\n" + "="*70)
            print("Ready for another goal! Or type 'exit' to quit.")
            print("="*70)
            
        except KeyboardInterrupt:
            print("\n\nSession terminated by user.")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again with a different goal.")
    
    print("\n" + "="*70)
    print("Thank you for using Gemini Marketing Planner!")
    print("="*70)
    print()


if __name__ == "__main__":
    main()
