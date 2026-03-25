# 🎯 Marketing Agent: Setup & Development

This folder contains the core logic for the Marketing Planning Assistant. It includes the backend API, AI-powered planning engines, and the professional React-based web dashboard.

## 📁 Folder Structure

- `api.py`: FastAPI server that orchestrates the planning process.
- `gemini_planner.py`: Advanced planning logic powered by Google Gemini.
- `planner_agent.py`: Multi-agent system using CrewAI/LangChain and fallback modes.
- `scheduler.py`: A dependency-aware task scheduling engine.
- `tools.py`: Mock marketing tools for resource validation and competitor analysis.
- `static/`: Contains the React-based frontend (`index.html`).

## 🛠️ Detailed Setup

### 1. Environment Variables
Create a `.env` file in this directory with your API keys:
```env
GEMINI_API_KEY=your_google_gemini_api_key
OPENAI_API_KEY=your_openai_api_key (Optional)
```
*Note: If no API keys are provided, the system will fall back to its rule-based `SimplePlanner` mode.*

### 2. Manual Installation
If you prefer not to use `setup.bat`, you can install dependencies manually:
```bash
pip install -r requirements.txt
```

### 3. Running the Backend
To start only the backend API:
```bash
py api.py
```
By default, the API runs on `http://localhost:8001`.

## 🌐 API Endpoints

- **GET /health**: Check the API status.
- **POST /plan**: Generate a marketing plan from a goal.
  - **Payload**:
    ```json
    {
      "goal": "Launch a subscription coffee service",
      "duration_days": 14,
      "custom_instructions": "Focus on TikTok, No paid ads"
    }
    ```

## 🧠 Strategic Reasoning Flow

1. **Interpretation**: The agent analyzes the goal to identify target audience, KPIs, and potential challenges.
2. **Decomposition**: The AI breaks down the interpreted goal into 5-10 actionable tasks.
3. **Validation**: Each task is checked against mock marketing tools for feasibility.
4. **Scheduling**: A dependency-aware schedule is generated, identifying milestones and daily activities.

---
Built by [FlixBlackout](https://github.com/FlixBlackout)
