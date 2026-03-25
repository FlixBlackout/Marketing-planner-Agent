"""
Marketing Planning Assistant Agent - Main Entry Point.

This module provides the main interface for the Marketing Planning Assistant.
It accepts user input marketing goals and orchestrates the complete planning process:
1. Goal interpretation
2. Task decomposition
3. Resource validation
4. Schedule generation

Usage:
    python main.py
    # Then enter your marketing goal when prompted
    
Example:
    Input: "Analyze competitor ads for a smartphone brand"
    Output: Complete marketing plan with tasks, resources, and schedule
"""

import sys
from datetime import datetime
from typing import Optional

from planner_agent import SimplePlanner, PlannerAgent
from scheduler import ExecutionScheduler


def print_banner():
    """Print application banner."""
    print("\n" + "="*70)
    print(" " * 20 + "MARKETING PLANNING ASSISTANT")
    print(" " * 25 + "Agentic AI System")
    print("="*70)
    print()


def print_welcome():
    """Print welcome message and instructions."""
    print("Welcome! This AI agent will help you create a comprehensive")
    print("marketing execution plan from your high-level goals.")
    print()
    print("How it works:")
    print("  1. Enter your marketing goal (e.g., 'Analyze competitor ads')")
    print("  2. The agent will interpret and decompose your goal into tasks")
    print("  3. Resources are validated for each task")
    print("  4. A detailed execution schedule is generated")
    print()
    print("Type 'exit' or 'quit' to end the session.")
    print("-"*70)
    print()


def get_user_input() -> Optional[str]:
    """
    Get marketing goal from user input.
    
    Returns:
        User input string or None if user wants to exit
    """
    try:
        user_input = input("\nEnter your marketing goal: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'q']:
            return None
        
        return user_input
    
    except (EOFError, KeyboardInterrupt):
        print("\n\nSession terminated by user.")
        return None


def run_planning_process(marketing_goal: str, use_gemini: bool = True) -> dict:
    """
    Execute the complete planning process for a marketing goal.
    
    Args:
        marketing_goal: The marketing objective to plan
        use_gemini: Whether to use Gemini-powered planner (recommended)
        
    Returns:
        Complete plan dictionary
    """
    print("\n" + "="*70)
    print("PROCESSING YOUR MARKETING GOAL")
    print("="*70)
    print(f"\nGoal: {marketing_goal}")
    print()
    
    # Use Gemini-powered planner
    if use_gemini:
        print("🌟 Using Gemini-Powered Planner Agent...")
        try:
            from gemini_planner import GeminiMarketingPlanner
            planner = GeminiMarketingPlanner()
        except ImportError as e:
            print(f"⚠️  Could not import Gemini planner: {e}")
            print("   Falling back to Simple Planner...")
            planner = SimplePlanner()
    else:
        print("🤖 Using Simple Planner Agent...")
        planner = SimplePlanner()
    
    # Generate plan using Gemini or Simple planner
    plan = planner.generate_complete_plan(marketing_goal) if hasattr(planner, 'generate_complete_plan') else planner.generate_plan(marketing_goal)
    
    # Step 4: Generate execution schedule
    print("\n[Step 4] Creating execution timeline...")
    scheduler = ExecutionScheduler()
    schedule = scheduler.generate_schedule(plan['tasks'])
    
    # Print the detailed schedule
    scheduler.print_schedule(schedule)
    
    # Add schedule to plan
    plan['schedule'] = schedule
    
    return plan


def print_final_summary(plan: dict):
    """
    Print final summary of the complete marketing plan.
    
    Args:
        plan: Complete plan dictionary with schedule
    """
    print("\n" + "="*70)
    print("COMPLETE MARKETING PLAN")
    print("="*70)
    
    goal_info = plan.get('goal', {})
    print(f"\nGOAL: {goal_info.get('original', 'N/A')}")
    
    if isinstance(goal_info, dict):
        print(f"Focus Areas: {goal_info.get('focus_areas', [])}")
    
    print("\nTASK PLAN:")
    for i, task in enumerate(plan.get('tasks', []), 1):
        deps = f" (after tasks {task['dependencies']})" if task['dependencies'] else ""
        print(f"{i}. {task['task_name']}{deps}")
        print(f"   - {task['description']}")
        print(f"   - Tools: {', '.join(task['required_tools'])}")
        print(f"   - Duration: {task['estimated_days']} day(s)")
    
    print("\nRESOURCE VALIDATION:")
    resources = plan.get('resources', {})
    for tool_name, tool_info in resources.get('tools_status', {}).items():
        status = tool_info.get('status', 'Unknown')
        print(f"{tool_name} -> {status}")
    
    print("\nEXECUTION SCHEDULE:")
    schedule = plan.get('schedule', {})
    for day_entry in schedule.get('timeline', []):
        day_num = day_entry['day']
        tasks_active = [t['task_name'] for t in day_entry['tasks']]
        if tasks_active:
            print(f"Day {day_num} -> {', '.join(tasks_active)}")
    
    print("\n" + "="*70)
    print("="*70)
    print()
    print("Next Steps:")
    print("  1. Review the task breakdown and timeline above")
    print("  2. Adjust resource allocation as needed")
    print("  3. Begin execution starting with Task 1")
    print("  4. Monitor progress against milestones")
    print()
    print("You can now enter another marketing goal or type 'exit' to quit.")
    print("-"*70)


def main():
    """Main entry point for the Marketing Planning Assistant."""
    print_banner()
    print_welcome()
    
    # Configuration
    USE_GEMINI = True  # Always use Gemini for better results
    
    # Check for Gemini API key
    if USE_GEMINI:
        import os
        from dotenv import load_dotenv
        
        # Load environment variables from .env file
        load_dotenv()
        
        gemini_key = os.getenv("GEMINI_API_KEY")
        if not gemini_key:
            print("[WARNING] GEMINI_API_KEY not found in environment variables.")
            print("   The system will work in mock mode without AI enhancements.")
            print()
            print("   To get FREE Gemini API key:")
            print("   https://makersuite.google.com/app/apikey")
            print()
        else:
            print("[SUCCESS] Gemini API key loaded successfully!")
            print()
    
    # Store plans generated in this session
    session_plans = []
    
    # Main interaction loop
    while True:
        user_input = get_user_input()
        
        if user_input is None:
            break
        
        if not user_input.strip():
            print("Please enter a valid marketing goal.")
            continue
        
        # Process the marketing goal
        plan = run_planning_process(user_input, use_gemini=USE_GEMINI)
        session_plans.append(plan)
        
        # Print final summary
        print_final_summary(plan)
    
    # Exit message
    print("\nThank you for using Marketing Planning Assistant!")
    print(f"Total plans generated in this session: {len(session_plans)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {str(e)}")
        print("Please check that all dependencies are installed correctly.")
        print("See README.md for setup instructions.")
        sys.exit(1)
