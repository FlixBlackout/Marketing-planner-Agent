"""
Marketing Planning Assistant Agent - Backend API.

This module provides a FastAPI web server that exposes the planning logic
as a RESTful API.
"""

import os
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Import our project components
from openrouter_planner import OpenRouterPlanner
from gemini_planner import GeminiMarketingPlanner
from planner_agent import SimplePlanner
from scheduler import ExecutionScheduler

# Load environment variables
load_dotenv()

app = FastAPI(title="Marketing Planning Assistant API")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

class PlanningRequest(BaseModel):
    goal: str
    use_ai: bool = True
    duration_days: Optional[int] = 14
    custom_instructions: Optional[str] = ""

@app.get("/")
async def get_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"status": "online", "message": "Marketing Planning Assistant API is running (Frontend not found)"}

@app.get("/health")
async def health_check():
    return {"status": "online", "message": "Marketing Planning Assistant API is running"}

@app.post("/plan")
async def generate_plan(request: PlanningRequest):
    """
    Generate a comprehensive marketing plan based on a goal, duration, and constraints.
    
    Args:
        request (PlanningRequest): Contains the marketing goal, target duration, and custom instructions.
        
    Returns:
        dict: A structured marketing plan including interpretation, tasks, and execution schedule.
        
    Raises:
        HTTPException: If planning fails due to AI errors or invalid data.
    """
    if not request.goal:
        raise HTTPException(status_code=400, detail="Marketing goal is required")

    print(f"\n--- New Planning Request ---")
    print(f"Goal: {request.goal}")
    print(f"Target Duration: {request.duration_days} days")
    print(f"Custom Instructions: {request.custom_instructions}")
    
    # 1. Initialize Planner
    planner = None
    planner_type = "None"
    
    if request.use_ai:
        # Check for OpenRouter (Priority)
        try:
            planner = OpenRouterPlanner()
            if planner.api_key:
                planner_type = "OpenRouter"
                print("Using OpenRouter AI Planner")
            else:
                planner = None
        except Exception as e:
            print(f"⚠️ Error initializing OpenRouter planner: {e}")
            planner = None

        # Check for Gemini (Secondary)
        if not planner:
            try:
                planner = GeminiMarketingPlanner()
                if planner.api_key:
                    planner_type = "Gemini"
                    print("Using Gemini AI Planner")
                else:
                    planner = None
            except Exception as e:
                print(f"⚠️ Error initializing Gemini planner: {e}")
                planner = None

    # Fallback to SimplePlanner
    if not planner:
        planner_type = "Simple"
        print("⚠️ Falling back to SimplePlanner")
        planner = SimplePlanner()

    # 2. Interpret and Decompose
    try:
        if planner_type in ["OpenRouter", "Gemini"]:
            print(f"Interpreting goal with {planner_type}...")
            interpretation = planner.interpret_goal_with_ai(
                request.goal, 
                duration_days=request.duration_days,
                custom_instructions=request.custom_instructions
            )
            print(f"Decomposing tasks with {planner_type}...")
            tasks = planner.decompose_tasks_with_ai(interpretation)
        else:
            print("Interpreting goal with SimplePlanner...")
            interpretation = planner.interpret_goal(request.goal)
            print("Decomposing tasks with SimplePlanner...")
            tasks = planner.decompose_tasks(interpretation)
        
        # 3. Schedule
        print("Generating execution schedule...")
        scheduler = ExecutionScheduler()
        # Pass target duration to scheduler to ensure the timeline respects it
        schedule = scheduler.generate_schedule(tasks, target_duration=request.duration_days)
        
        print("Plan generation successful!")
        return {
            "goal": request.goal,
            "interpretation": interpretation,
            "tasks": tasks,
            "schedule": schedule
        }
    except Exception as e:
        print(f"❌ Planning error: {e}")
        import traceback
        traceback.print_exc()
        
        # Return a more structured error detail if possible
        error_msg = str(e)
        if "JSONDecodeError" in error_msg:
            error_msg = "The AI agent failed to generate a valid JSON plan. Please try again with a more specific goal."
            
        raise HTTPException(status_code=500, detail=error_msg)

if __name__ == "__main__":
    import uvicorn
    # Use direct uvicorn call to avoid potential issues with __name__ in some environments
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=False)
