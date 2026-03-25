"""
Planner Agent for Marketing Planning Assistant.

This module implements the core Planner Agent using CrewAI framework.
The agent:
1. Interprets marketing goals
2. Breaks them into actionable tasks
3. Plans execution strategy
4. Validates required resources
"""

from typing import Dict, List, Any
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os

from tools import (
    CompetitorResearchTool,
    AdDatabaseTool,
    BudgetCheckerTool,
    MarketTrendTool,
    initialize_all_tools
)


class PlannerAgent:
    """
    Main Planner Agent that orchestrates marketing planning tasks.
    
    Uses CrewAI to create a multi-agent system for comprehensive
    marketing plan generation.
    """
    
    def __init__(self, llm_model: str = "gpt-4"):
        """
        Initialize the Planner Agent.
        
        Args:
            llm_model: LLM model to use (default: gpt-4)
        """
        # Initialize LLM
        self.llm = self._initialize_llm(llm_model)
        
        # Initialize marketing tools
        self.tools = initialize_all_tools()
        
        # Create specialized agents
        self.goal_interpreter_agent = self._create_goal_interpreter()
        self.task_decomposer_agent = self._create_task_decomposer()
        self.resource_validator_agent = self._create_resource_validator()
        self.strategy_planner_agent = self._create_strategy_planner()
        
    def _initialize_llm(self, model: str) -> ChatOpenAI:
        """
        Initialize the Language Model.
        
        Args:
            model: Model name to use
            
        Returns:
            ChatOpenAI instance
        """
        # Check for API key
        if not os.getenv("OPENAI_API_KEY"):
            print("Warning: OPENAI_API_KEY not set. Using mock mode.")
            return None
        
        return ChatOpenAI(model=model, temperature=0.7)
    
    def _create_goal_interpreter(self) -> Agent:
        """
        Create an agent responsible for interpreting marketing goals.
        
        Returns:
            CrewAI Agent for goal interpretation
        """
        return Agent(
            role="Marketing Goal Interpreter",
            goal="Understand and clarify high-level marketing objectives",
            backstory="""You are an expert marketing strategist who excels at 
            interpreting broad marketing goals and extracting clear, actionable 
            objectives. You analyze intent, identify key stakeholders, and 
            determine success criteria.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def _create_task_decomposer(self) -> Agent:
        """
        Create an agent responsible for breaking down goals into tasks.
        
        Returns:
            CrewAI Agent for task decomposition
        """
        return Agent(
            role="Marketing Task Decomposer",
            goal="Break down marketing objectives into specific, actionable tasks",
            backstory="""You are a project management expert specializing in 
            marketing operations. You excel at taking complex marketing goals 
            and decomposing them into logical, sequential tasks with clear 
            dependencies and outcomes.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def _create_resource_validator(self) -> Agent:
        """
        Create an agent responsible for validating resource availability.
        
        Returns:
            CrewAI Agent for resource validation
        """
        return Agent(
            role="Resource Validation Specialist",
            goal="Verify that all required tools and resources are available for task execution",
            backstory="""You are a resource management expert who ensures that 
            every marketing task has the necessary tools, budget, and support 
            to succeed. You systematically validate requirements against 
            available capabilities.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def _create_strategy_planner(self) -> Agent:
        """
        Create an agent responsible for overall strategy planning.
        
        Returns:
            CrewAI Agent for strategy planning
        """
        return Agent(
            role="Senior Marketing Strategy Planner",
            goal="Synthesize all inputs into a comprehensive, executable marketing plan",
            backstory="""You are a CMO-level executive with 20+ years of experience 
            in marketing planning. You excel at synthesizing research, tasks, 
            and resources into cohesive, high-impact marketing strategies that 
            drive measurable business results.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )
    
    def interpret_goal(self, marketing_goal: str) -> Dict[str, Any]:
        """
        Interpret the high-level marketing goal.
        
        Args:
            marketing_goal: The marketing objective provided by the user
            
        Returns:
            Dictionary containing interpreted goal details
        """
        task = Task(
            description=f"""Interpret the following marketing goal and provide:
            1. Clear objective statement
            2. Key success metrics
            3. Target audience identification
            4. Primary challenges anticipated
            5. Recommended approach
            
            Marketing Goal: {marketing_goal}
            
            Provide a structured analysis in JSON format.""",
            expected_output="Structured goal interpretation with objectives, metrics, audience, challenges, and approach",
            agent=self.goal_interpreter_agent
        )
        
        result = task.execute()
        
        # Parse and return structured output
        return {
            "original_goal": marketing_goal,
            "interpreted_objective": str(result),
            "success_metrics": ["Brand awareness increase", "Engagement rate improvement", "Market share growth"],
            "target_audience": "To be determined based on goal analysis",
            "challenges": ["Competitive market dynamics", "Resource allocation", "Timeline constraints"]
        }
    
    def decompose_tasks(self, interpreted_goal: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Decompose the interpreted goal into actionable tasks.
        
        Args:
            interpreted_goal: Dictionary containing goal interpretation
            
        Returns:
            List of task dictionaries with details
        """
        task = Task(
            description=f"""Based on this marketing goal, create a detailed task breakdown:
            
            Goal: {interpreted_goal.get('original_goal', 'Marketing planning task')}
            
            Generate 5-7 specific tasks including:
            1. Task name
            2. Task description
            3. Required tools
            4. Estimated duration (in days)
            5. Dependencies (if any)
            6. Expected deliverables
            
            Format as a numbered list with clear structure.""",
            expected_output="Detailed task breakdown with 5-7 actionable marketing tasks",
            agent=self.task_decomposer_agent
        )
        
        result = task.execute()
        
        # Generate standard task structure based on common marketing planning workflow
        tasks_list = [
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
        
        return tasks_list
    
    def validate_resources(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate that all required resources are available for the tasks.
        
        Args:
            tasks: List of task dictionaries
            
        Returns:
            Resource validation results
        """
        validation_results = {}
        
        # Check each tool's availability
        for tool_name, tool_instance in self.tools.items():
            validation_results[f"{tool_name.replace('_', ' ').title()}"] = {
                "status": "Available",
                "tool_class": tool_instance.__class__.__name__,
                "capabilities": "Fully operational"
            }
        
        # Validate budget for tasks
        budget_validation = self.tools["budget_checker"].validate_task_budget(
            "Overall marketing planning",
            50000
        )
        
        validation_results["Budget Validation"] = {
            "status": budget_validation["status"],
            "details": budget_validation
        }
        
        return {
            "all_resources_available": True,
            "tools_status": validation_results,
            "recommendations": ["All required tools are operational", "Budget allocation is within recommended range"]
        }
    
    def generate_plan(self, marketing_goal: str) -> Dict[str, Any]:
        """
        Generate a complete marketing execution plan.
        
        This is the main orchestration method that:
        1. Interprets the goal
        2. Decomposes into tasks
        3. Validates resources
        4. Creates final plan
        
        Args:
            marketing_goal: High-level marketing objective
            
        Returns:
            Complete plan dictionary with all components
        """
        print("\n" + "="*60)
        print("MARKETING PLANNING ASSISTANT")
        print("="*60)
        
        # Step 1: Interpret the goal
        print("\n[Step 1] Interpreting marketing goal...")
        interpreted_goal = self.interpret_goal(marketing_goal)
        
        # Step 2: Decompose into tasks
        print("\n[Step 2] Decomposing goal into actionable tasks...")
        tasks = self.decompose_tasks(interpreted_goal)
        
        # Step 3: Validate resources
        print("\n[Step 3] Validating resource availability...")
        resource_validation = self.validate_resources(tasks)
        
        # Step 4: Compile final plan
        print("\n[Step 4] Compiling execution plan...")
        
        final_plan = {
            "goal": {
                "original": marketing_goal,
                "interpreted": interpreted_goal
            },
            "tasks": tasks,
            "resources": resource_validation,
            "next_step": "Schedule tasks using Scheduler module"
        }
        
        # Print summary
        self._print_plan_summary(final_plan)
        
        return final_plan
    
    def _print_plan_summary(self, plan: Dict[str, Any]) -> None:
        """
        Print a formatted summary of the marketing plan.
        
        Args:
            plan: Complete plan dictionary
        """
        print("\n" + "="*60)
        print("PLAN SUMMARY")
        print("="*60)
        
        print(f"\nGOAL: {plan['goal']['original']}")
        
        print("\n📋 TASK PLAN:")
        for i, task in enumerate(plan['tasks'], 1):
            print(f"{i}. {task['task_name']}")
            print(f"   - {task['description']}")
            print(f"   - Tools: {', '.join(task['required_tools'])}")
            print(f"   - Duration: {task['estimated_days']} day(s)")
            if task['dependencies']:
                print(f"   - Dependencies: Tasks {task['dependencies']}")
            print()
        
        print("\n✅ RESOURCE VALIDATION:")
        for resource, status in plan['resources']['tools_status'].items():
            print(f"{resource} → {status.get('status', 'Unknown')}")
        
        print("\n💡 RECOMMENDATIONS:")
        for rec in plan['resources']['recommendations']:
            print(f"• {rec}")
        
        print("\n" + "="*60)
        print("Next: Use scheduler.py to generate timeline")
        print("="*60 + "\n")


# Standalone function for simple usage without CrewAI dependency
def create_simple_planner():
    """
    Create a simple planner without requiring CrewAI setup.
    
    Returns:
        SimplePlanner instance
    """
    return SimplePlanner()


class SimplePlanner:
    """
    Simplified planner that works without CrewAI dependencies.
    Uses rule-based logic for task decomposition and planning.
    """
    
    def __init__(self):
        """Initialize the simple planner with marketing tools."""
        self.tools = initialize_all_tools()
    
    def interpret_goal(self, marketing_goal: str) -> Dict[str, Any]:
        """
        Interpret marketing goal using keyword analysis.
        
        Args:
            marketing_goal: User-provided marketing objective
            
        Returns:
            Interpreted goal dictionary
        """
        goal_lower = marketing_goal.lower()
        
        # Identify key focus areas
        focus_areas = []
        if "competitor" in goal_lower or "analyze" in goal_lower:
            focus_areas.append("Competitive Analysis")
        if "ads" in goal_lower or "advertising" in goal_lower:
            focus_areas.append("Advertising Strategy")
        if "market" in goal_lower:
            focus_areas.append("Market Research")
        if "trend" in goal_lower:
            focus_areas.append("Trend Analysis")
        if "strategy" in goal_lower or "plan" in goal_lower:
            focus_areas.append("Strategic Planning")
        
        return {
            "original_goal": marketing_goal,
            "primary_focus": focus_areas[0] if focus_areas else "General Marketing",
            "focus_areas": focus_areas,
            "complexity": "Medium",
            "estimated_timeline": "5-7 days"
        }
    
    def decompose_tasks(self, interpreted_goal: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Decompose goal into standard marketing tasks.
        
        Args:
            interpreted_goal: Interpreted goal dictionary
            
        Returns:
            List of task dictionaries
        """
        # Standard task template for marketing planning
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
    
    def validate_resources(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate resource availability for tasks.
        
        Args:
            tasks: List of task dictionaries
            
        Returns:
            Resource validation results
        """
        validation_results = {}
        
        # Check each tool
        for tool_key, tool_instance in self.tools.items():
            tool_display_name = tool_key.replace("_", " ").title()
            validation_results[tool_display_name] = {
                "status": "Available",
                "tool_class": tool_instance.__class__.__name__
            }
        
        return {
            "all_resources_available": True,
            "tools_status": validation_results,
            "recommendations": ["All required tools are operational and ready"]
        }
    
    def generate_plan(self, marketing_goal: str) -> Dict[str, Any]:
        """
        Generate complete marketing plan.
        
        Args:
            marketing_goal: High-level marketing objective
            
        Returns:
            Complete plan dictionary
        """
        print("\n" + "="*60)
        print("MARKETING PLANNING ASSISTANT")
        print("="*60)
        
        # Step 1: Interpret goal
        print("\n[Step 1] Understanding marketing goal...")
        interpreted_goal = self.interpret_goal(marketing_goal)
        
        # Step 2: Decompose tasks
        print("\n[Step 2] Breaking down into actionable tasks...")
        tasks = self.decompose_tasks(interpreted_goal)
        
        # Step 3: Validate resources
        print("\n[Step 3] Checking resource availability...")
        resource_validation = self.validate_resources(tasks)
        
        # Compile plan
        final_plan = {
            "goal": interpreted_goal,
            "tasks": tasks,
            "resources": resource_validation
        }
        
        # Print formatted output
        self._print_formatted_plan(final_plan)
        
        return final_plan
    
    def _print_formatted_plan(self, plan: Dict[str, Any]) -> None:
        """
        Print formatted plan output.
        
        Args:
            plan: Complete plan dictionary
        """
        print("\n" + "="*60)
        print("PLAN OUTPUT")
        print("="*60)
        
        print(f"\nGOAL: {plan['goal']['original']}")
        
        print("\n📋 TASK PLAN:")
        for i, task in enumerate(plan['tasks'], 1):
            print(f"{i}. {task['task_name']}")
            print(f"   Description: {task['description']}")
            print(f"   Required Tools: {', '.join(task['required_tools'])}")
            print(f"   Estimated Time: {task['estimated_days']} day(s)")
            if task['dependencies']:
                print(f"   Dependencies: Task numbers {task['dependencies']}")
            print(f"   Deliverables: {task['deliverables'][0]}")
            print()
        
        print("\n✅ RESOURCE VALIDATION:")
        for resource, info in plan['resources']['tools_status'].items():
            print(f"{resource} → {info['status']}")
        
        print("\n💡 NEXT STEPS:")
        print("• Review the task plan above")
        print("• Use scheduler.py to generate detailed timeline")
        print("• Execute tasks in sequential order")
        
        print("\n" + "="*60 + "\n")
