"""
Execution Scheduler for Marketing Planning Assistant.

This module generates a timeline/schedule for marketing tasks based on:
- Task dependencies
- Estimated durations
- Resource availability
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta


class ExecutionScheduler:
    """
    Generates execution schedules for marketing task plans.
    
    Creates day-by-day timelines with task assignments and milestones.
    """
    
    def __init__(self, start_date: datetime = None):
        """
        Initialize the scheduler.
        
        Args:
            start_date: Project start date (default: today)
        """
        self.start_date = start_date or datetime.now()
    
    def generate_schedule(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a complete execution schedule from task list.
        
        Args:
            tasks: List of task dictionaries with dependencies and durations
            
        Returns:
            Complete schedule dictionary with timeline
        """
        # Sort tasks by dependencies to ensure proper ordering
        sorted_tasks = self._topological_sort(tasks)
        
        # Calculate start and end dates for each task
        scheduled_tasks = self._calculate_schedule(sorted_tasks)
        
        # Generate day-by-day timeline
        timeline = self._generate_timeline(scheduled_tasks)
        
        # Identify critical path and milestones
        critical_path = self._identify_critical_path(scheduled_tasks)
        milestones = self._identify_milestones(scheduled_tasks)
        
        return {
            "scheduled_tasks": scheduled_tasks,
            "timeline": timeline,
            "critical_path": critical_path,
            "milestones": milestones,
            "total_duration_days": len(timeline),
            "start_date": self.start_date.strftime("%Y-%m-%d"),
            "end_date": (self.start_date + timedelta(days=len(timeline))).strftime("%Y-%m-%d")
        }
    
    def _topological_sort(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sort tasks based on dependencies using topological sorting.
        
        Args:
            tasks: List of task dictionaries
            
        Returns:
            Sorted list of tasks respecting dependencies
        """
        # Build adjacency list
        task_map = {task['task_id']: task for task in tasks}
        visited = set()
        result = []
        
        def visit(task_id: int):
            if task_id in visited:
                return
            
            visited.add(task_id)
            task = task_map[task_id]
            
            # Visit dependencies first
            for dep_id in task.get('dependencies', []):
                visit(dep_id)
            
            result.append(task)
        
        # Visit all tasks
        for task in tasks:
            visit(task['task_id'])
        
        return result
    
    def _calculate_schedule(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Calculate start and end dates for each task.
        
        Args:
            tasks: Topologically sorted list of tasks
            
        Returns:
            List of tasks with schedule information
        """
        scheduled_tasks = []
        task_end_dates = {}  # task_id -> end_day
        
        current_day = 0
        
        for task in tasks:
            # Determine earliest start day based on dependencies
            dependencies = task.get('dependencies', [])
            if dependencies:
                # Start after all dependencies are complete
                earliest_start = max(task_end_dates.get(dep_id, 0) for dep_id in dependencies)
            else:
                earliest_start = current_day
            
            # Calculate task duration
            duration = task.get('estimated_days', 1)
            end_day = earliest_start + duration - 1
            
            # Update task with schedule info
            scheduled_task = task.copy()
            scheduled_task['start_day'] = earliest_start + 1  # 1-indexed
            scheduled_task['end_day'] = end_day + 1  # 1-indexed
            scheduled_task['duration'] = duration
            
            task_end_dates[task['task_id']] = end_day + 1
            
            scheduled_tasks.append(scheduled_task)
        
        return scheduled_tasks
    
    def _generate_timeline(self, scheduled_tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate day-by-day timeline view.
        
        Args:
            scheduled_tasks: Tasks with schedule information
            
        Returns:
            List of day entries with assigned tasks
        """
        if not scheduled_tasks:
            return []
        
        total_days = max(task['end_day'] for task in scheduled_tasks)
        timeline = []
        
        for day in range(1, total_days + 1):
            day_entry = {
                "day": day,
                "date": (self.start_date + timedelta(days=day-1)).strftime("%Y-%m-%d"),
                "tasks": [],
                "milestones": []
            }
            
            # Find tasks active on this day
            for task in scheduled_tasks:
                if task['start_day'] <= day <= task['end_day']:
                    day_entry['tasks'].append({
                        "task_id": task['task_id'],
                        "task_name": task['task_name'],
                        "is_start": day == task['start_day'],
                        "is_end": day == task['end_day']
                    })
                
                # Check for milestone completions
                if day == task['end_day']:
                    day_entry['milestones'].append(f"Complete: {task['task_name']}")
            
            timeline.append(day_entry)
        
        return timeline
    
    def _identify_critical_path(self, scheduled_tasks: List[Dict[str, Any]]) -> List[int]:
        """
        Identify the critical path (longest dependency chain).
        
        Args:
            scheduled_tasks: Tasks with schedule information
            
        Returns:
            List of task IDs on the critical path
        """
        if not scheduled_tasks:
            return []
        
        # Find tasks with no dependents (end tasks)
        all_task_ids = {task['task_id'] for task in scheduled_tasks}
        dependent_tasks = set()
        
        for task in scheduled_tasks:
            dependent_tasks.update(task.get('dependencies', []))
        
        end_tasks = all_task_ids - dependent_tasks
        
        # Backtrack from end tasks to find critical path
        critical_path = []
        task_map = {task['task_id']: task for task in scheduled_tasks}
        
        def backtrack(task_id: int):
            critical_path.insert(0, task_id)
            task = task_map[task_id]
            dependencies = task.get('dependencies', [])
            
            if dependencies:
                # Choose the dependency with latest end time
                latest_dep = max(dependencies, key=lambda x: task_map[x]['end_day'])
                backtrack(latest_dep)
        
        if end_tasks:
            # Start from the task with latest end time
            latest_end_task = max(end_tasks, key=lambda x: task_map[x]['end_day'])
            backtrack(latest_end_task)
        
        return critical_path
    
    def _identify_milestones(self, scheduled_tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Identify key project milestones.
        
        Args:
            scheduled_tasks: Tasks with schedule information
            
        Returns:
            List of milestone dictionaries
        """
        milestones = []
        
        for task in scheduled_tasks:
            milestones.append({
                "milestone_id": f"M{task['task_id']}",
                "name": f"Complete: {task['task_name']}",
                "day": task['end_day'],
                "date": (self.start_date + timedelta(days=task['end_day']-1)).strftime("%Y-%m-%d"),
                "deliverables": task.get('deliverables', [])
            })
        
        return milestones
    
    def print_schedule(self, schedule: Dict[str, Any]) -> None:
        """
        Print formatted schedule output.
        
        Args:
            schedule: Complete schedule dictionary
        """
        print("\n" + "="*60)
        print("EXECUTION SCHEDULE")
        print("="*60)
        
        print(f"\n📅 Project Timeline:")
        print(f"   Start Date: {schedule['start_date']}")
        print(f"   End Date: {schedule['end_date']}")
        print(f"   Total Duration: {schedule['total_duration_days']} days")
        
        print("\n📋 DAY-BY-DAY SCHEDULE:")
        print("-" * 60)
        
        for day_info in schedule['timeline']:
            print(f"\nDay {day_info['day']} ({day_info['date']}):")
            
            if day_info['tasks']:
                for task in day_info['tasks']:
                    status = ""
                    if task['is_start'] and task['is_end']:
                        status = "⚡ START & COMPLETE"
                    elif task['is_start']:
                        status = "▶️  START"
                    elif task['is_end']:
                        status = "✅ COMPLETE"
                    else:
                        status = "⏩ IN PROGRESS"
                    
                    print(f"   • {task['task_name']} [{status}]")
            
            if day_info['milestones']:
                print(f"   🎯 Milestones:")
                for milestone in day_info['milestones']:
                    print(f"      ✓ {milestone}")
        
        print("\n" + "-" * 60)
        print("\n🎯 KEY MILESTONES:")
        
        for milestone in schedule['milestones']:
            print(f"   Day {milestone['day']}: {milestone['name']}")
            for deliverable in milestone.get('deliverables', []):
                print(f"      → {deliverable}")
        
        print("\n🔴 CRITICAL PATH:")
        critical_task_ids = schedule['critical_path']
        task_map = {task['task_id']: task for task in schedule['scheduled_tasks']}
        
        for i, task_id in enumerate(critical_task_ids, 1):
            task = task_map[task_id]
            connector = "→" if i < len(critical_task_ids) else "✓"
            print(f"   {i}. {task['task_name']} {connector}")
        
        print("\n💡 SCHEDULING NOTES:")
        print("   • Tasks are scheduled sequentially based on dependencies")
        print("   • Critical path indicates minimum project duration")
        print("   • Non-critical tasks may have scheduling flexibility")
        print("   • Resource conflicts should be monitored during execution")
        
        print("\n" + "="*60 + "\n")
    
    def export_to_text(self, schedule: Dict[str, Any]) -> str:
        """
        Export schedule as formatted text string.
        
        Args:
            schedule: Complete schedule dictionary
            
        Returns:
            Formatted text representation of schedule
        """
        lines = []
        lines.append("="*60)
        lines.append("EXECUTION SCHEDULE")
        lines.append("="*60)
        
        lines.append(f"\nProject Timeline: {schedule['start_date']} to {schedule['end_date']}")
        lines.append(f"Total Duration: {schedule['total_duration_days']} days\n")
        
        lines.append("DAY-BY-DAY SCHEDULE:")
        lines.append("-"*60)
        
        for day_info in schedule['timeline']:
            task_names = [t['task_name'] for t in day_info['tasks']]
            if task_names:
                lines.append(f"Day {day_info['day']}: {', '.join(task_names)}")
            else:
                lines.append(f"Day {day_info['day']}: (No tasks scheduled)")
        
        lines.append("-"*60)
        lines.append("")
        
        return "\n".join(lines)


def create_schedule_from_plan(plan: Dict[str, Any], start_date: datetime = None) -> Dict[str, Any]:
    """
    Create execution schedule from a marketing plan.
    
    Args:
        plan: Marketing plan dictionary containing tasks
        start_date: Optional start date for the project
        
    Returns:
        Complete schedule dictionary
    """
    scheduler = ExecutionScheduler(start_date)
    tasks = plan.get('tasks', [])
    
    schedule = scheduler.generate_schedule(tasks)
    
    return schedule


# Example usage and demonstration
if __name__ == "__main__":
    # Sample tasks for testing
    sample_tasks = [
        {
            "task_id": 1,
            "task_name": "Identify top competitors",
            "description": "Research competitors",
            "required_tools": ["CompetitorResearchTool"],
            "estimated_days": 1,
            "dependencies": [],
            "deliverables": ["Competitor list"]
        },
        {
            "task_id": 2,
            "task_name": "Collect competitor ads",
            "description": "Gather ad campaigns",
            "required_tools": ["AdDatabaseTool"],
            "estimated_days": 1,
            "dependencies": [1],
            "deliverables": ["Ad database"]
        },
        {
            "task_id": 3,
            "task_name": "Analyze ad messaging",
            "description": "Analyze messaging",
            "required_tools": ["AdDatabaseTool"],
            "estimated_days": 1,
            "dependencies": [2],
            "deliverables": ["Analysis report"]
        },
        {
            "task_id": 4,
            "task_name": "Identify market trends",
            "description": "Research trends",
            "required_tools": ["MarketTrendTool"],
            "estimated_days": 1,
            "dependencies": [1],
            "deliverables": ["Trend report"]
        },
        {
            "task_id": 5,
            "task_name": "Generate strategy recommendations",
            "description": "Create strategy",
            "required_tools": ["BudgetCheckerTool"],
            "estimated_days": 1,
            "dependencies": [3, 4],
            "deliverables": ["Strategy document"]
        }
    ]
    
    # Generate and print schedule
    scheduler = ExecutionScheduler()
    schedule = scheduler.generate_schedule(sample_tasks)
    scheduler.print_schedule(schedule)
