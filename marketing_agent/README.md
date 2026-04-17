# 🎯 Marketing Planning Assistant

AI-powered marketing planning agent that creates actionable, day-by-day marketing strategies using Google Gemini and multi-agent systems.

## 🚀 Quick Start

### Local Development
```bash
cd marketing_agent
python api.py
```
Access at: http://localhost:8000

### Docker
```bash
docker-compose up
```

### Kubernetes
```bash
cd k8s
.\setup-k8s.bat
```

### AWS (Free Tier)
```bash
cd aws
.\deploy-aws-quick.ps1
```

## 📁 Folder Structure

- `api.py`: FastAPI server that orchestrates the planning process.
- `gemini_planner.py`: Advanced planning logic powered by Google Gemini.
- `planner_agent.py`: Multi-agent system using CrewAI/LangChain and fallback modes.
- `scheduler.py`: A dependency-aware task scheduling engine.
- `tools.py`: Mock marketing tools for resource validation and competitor analysis.
- `static/`: Contains the React-based frontend (`index.html`).
- `k8s/`: Kubernetes deployment manifests
- `aws/`: AWS deployment scripts and templates
- `Dockerfile`: Multi-stage Docker build configuration

## 🌐 Deployment Options

| Platform | Free Tier | Setup Time | Complexity |
|----------|-----------|------------|------------|
| **Local** | ✅ Always | 5 min | Easy |
| **Docker** | ✅ Always | 10 min | Easy |
| **Kubernetes** | ✅ Always | 15 min | Medium |
| **AWS App Runner** | ✅ 100 GB-hrs/mo | 20 min | Easy |
| **Render** | ✅ 750 hrs/mo | 10 min | Easy |

**See deployment guides:**
- [AWS Free Tier Deployment](aws/AWS_DEPLOYMENT.md)
- [AWS Cost Optimization](aws/AWS_FREE_TIER_COST_GUIDE.md)
- [Docker Guide](DOCKER_GUIDE.md)
- [Kubernetes Setup](KUBERNETES_SETUP.md)
- [Kubernetes Quick Ref](k8s/KUBERNETES_QUICK_REF.md)

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
