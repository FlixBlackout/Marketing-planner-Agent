# 🤖 Marketing Planner Agent

An advanced, agentic AI system designed to automate the process of creating comprehensive marketing execution plans. Powered by Gemini Flash 2.0 and React, this tool decomposes high-level goals into actionable tasks, validates resources, and generates a realistic day-by-day execution schedule.

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/FlixBlackout/Marketing-planner-Agent)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0+-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://reactjs.org/)

## ✨ Key Features

- **🎯 Agentic Goal Decomposition**: Automatically breaks down complex marketing objectives into 5-10 actionable tasks.
- **📅 Dynamic Scheduling**: Generates a dependency-aware, day-by-day execution timeline based on your target duration.
- **⚙️ Strategic Customization**: Adjust plan duration (3-60 days) and provide custom constraints (e.g., "TikTok focus," "No paid ads").
- **🧠 Multi-Agent Intelligence**: Analyzes target audience, success metrics (KPIs), and potential challenges.
- **💻 Professional Web UI**: Modern, responsive React dashboard with real-time planning feedback and strategic insights.
- **🛠️ Integrated Mock Tools**: Simulates resource validation using competitor research, ad databases, and budget checkers.

## 🏗️ Project Architecture

The system is built on a modern, decoupled architecture:

- **Frontend**: A high-performance React SPA served via FastAPI, using Tailwind CSS for professional styling.
- **Backend API**: A FastAPI REST server that orchestrates the planning logic and handles multi-agent communication.
- **Planning Engines**: 
  - **OpenRouter Planner (Primary)**: Uses OpenRouter (OpenAI-compatible) to access a wide range of models (Gemini, GPT-4, Claude).
  - **Gemini Planner (Secondary)**: Direct integration with Google's Gemini Flash 2.0.
  - **Simple Planner**: A robust rule-based fallback system.
- **Scheduling Engine**: A custom dependency-aware scheduler that calculates critical paths and milestones.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8 or higher.
- A Google Gemini API Key (Optional, but recommended for full AI features).

### 2. Setup
Clone the repository and run the automated setup:
```powershell
git clone https://github.com/FlixBlackout/Marketing-planner-Agent.git
cd Marketing-planner-Agent/marketing_agent
./setup.bat
```

### 3. Run the Dashboard
Launch the professional web interface:
```powershell
cd ..
./web_run.bat
```
Visit **[http://localhost:8001](http://localhost:8001)** in your browser to start planning.

## 🌐 Deployment (Render / Heroku)

This project is configured for easy deployment on platforms like Render or Heroku.

### Steps to Deploy on Render:
1. **Connect GitHub**: Fork this repository and connect it to a new "Web Service" on Render.
2. **Build Settings**:
   - **Environment**: `Python`
   - **Build Command**: `pip install -r marketing_agent/requirements.txt`
   - **Start Command**: `uvicorn marketing_agent.api:app --host 0.0.0.0 --port $PORT`
3. **Environment Variables**:
   - Add `OPENROUTER_API_KEY` (or `GEMINI_API_KEY`) to the environment variables section in the Render dashboard.
   - Set `MAX_TOKENS=2500` and `TEMPERATURE=0.7` as needed.

## 🛠️ Technology Stack

- **Core**: Python 3.10+
- **AI/LLM**: Google Gemini Flash 2.0, CrewAI, LangChain
- **Backend**: FastAPI, Uvicorn, Pydantic
- **Frontend**: React 18, Tailwind CSS, Lucide Icons, Framer Motion
- **DevOps**: Git, GitHub Actions

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---
Built with ❤️ by [FlixBlackout](https://github.com/FlixBlackout)
