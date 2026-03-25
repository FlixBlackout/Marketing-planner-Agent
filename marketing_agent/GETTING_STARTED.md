# 🚀 Getting Started with Marketing Planning Assistant

## Quick Start Guide

Welcome to the **Marketing Planning Assistant**! This guide will help you get up and running in minutes.

---

## 📋 Table of Contents

1. [Installation Options](#installation-options)
2. [Setup Instructions](#setup-instructions)
3. [Running the Application](#running-the-application)
4. [API Key Setup](#api-key-setup)
5. [First Run Example](#first-run-example)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 Installation Options

### Option A: Automated Setup (Windows - EASIEST) ⭐

**Perfect for beginners!**

1. Navigate to the `marketing_agent` folder
2. **Double-click** `setup.bat`
3. Wait for installation to complete
4. **Double-click** `web_run.bat` (to start the Web Dashboard) or `run.bat` (for CLI)

That's it! ✨

### Option B: Manual Setup (All Platforms)

**For advanced users or macOS/Linux:**

```bash
# 1. Navigate to project directory
cd marketing_agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Web Dashboard
python api.py

# 4. Open in browser
http://localhost:8000
```

---

## 🔧 Setup Instructions

### Step 1: Check Python Installation

Open terminal/command prompt and run:

```bash
python --version
```

**Expected output**: `Python 3.8.x` or higher

**If Python is not found:**
- Download from: https://www.python.org/downloads/
- ✅ **Important**: Check "Add Python to PATH" during installation

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- CrewAI (for multi-agent AI)
- LangChain (AI framework)
- Google Generative AI (Gemini support)
- Rich (beautiful terminal output)
- Other utilities

### Step 3: Choose Your Mode

The application works in **THREE modes**:

| Mode | API Key Required | Speed | Best For |
|------|-----------------|-------|----------|
| **Simple Planner** | ❌ No | ⚡⚡⚡ Fast | Testing, demos, quick tasks |
| **Gemini AI** | ✅ Yes (FREE) | ⚡⚡ Medium | Production, intelligent planning |
| **CrewAI/OpenAI** | ✅ Yes (Paid) | ⚡ Slower | Advanced multi-agent systems |

---

## 🎮 Running the Application

### Method 1: Simple Planner (NO API KEY)

```bash
python main.py
```

**Features:**
- ✅ Works immediately
- ✅ No setup required
- ✅ Fast execution
- ✅ Deterministic results

### Method 2: Gemini-Powered AI (RECOMMENDED) 🌟

```bash
python gemini_planner.py
```

**Features:**
- ✅ Intelligent goal interpretation
- ✅ Creative task breakdown
- ✅ Strategic recommendations
- ✅ FREE API with generous limits

**Setup Required:**
1. Get FREE API key: https://makersuite.google.com/app/apikey
2. Set environment variable (see [API Key Setup](#api-key-setup))

### Method 3: CrewAI with OpenAI

Edit `main.py` line ~165:
```python
USE_CREWAI = True
```

Then run:
```bash
export OPENAI_API_KEY="your-key-here"  # macOS/Linux
# OR
$env:OPENAI_API_KEY="your-key-here"    # Windows PowerShell

python main.py
```

---

## 🔑 API Key Setup

### Getting a Gemini API Key (FREE) ⭐ RECOMMENDED

1. **Visit**: https://makersuite.google.com/app/apikey
2. **Sign in** with your Google account
3. **Click** "Create API Key"
4. **Copy** the generated key

**Set the API Key:**

#### Windows (PowerShell):
```powershell
$env:GEMINI_API_KEY="paste-your-key-here"
python gemini_planner.py
```

#### Windows (Command Prompt):
```cmd
set GEMINI_API_KEY=paste-your-key-here
python gemini_planner.py
```

#### macOS/Linux:
```bash
export GEMINI_API_KEY="paste-your-key-here"
python gemini_planner.py
```

#### Permanent Setup (.env file):

Create a file named `.env` in the `marketing_agent` folder:

```
GEMINI_API_KEY=your-gemini-api-key-here
```

Then install python-dotenv:
```bash
pip install python-dotenv
```

---

## 📝 First Run Example

### Example 1: Simple Planner

```
Enter your marketing goal: Analyze competitor ads for a smartphone brand

======================================================================
MARKETING PLANNING ASSISTANT
======================================================================

[Step 1] Understanding marketing goal...
[Step 2] Breaking down into actionable tasks...
[Step 3] Checking resource availability...

GOAL: Analyze competitor ads for a smartphone brand

📋 TASK PLAN:
1. Identify top competitors
   - Research and identify key competitors
   - Tools: CompetitorResearchTool
   - Duration: 1 day

2. Collect competitor advertisements
   - Gather competitor ad campaigns
   - Tools: AdDatabaseTool
   - Duration: 1 day

3. Analyze ad messaging
   - Analyze themes and messaging
   - Tools: AdDatabaseTool
   - Duration: 1 day

4. Identify market trends
   - Research industry trends
   - Tools: MarketTrendTool
   - Duration: 1 day

5. Generate strategy recommendations
   - Create actionable strategy
   - Tools: BudgetCheckerTool
   - Duration: 1 day

✅ RESOURCE VALIDATION:
Competitor Research Tool → Available
Ad Database Tool → Available
Budget Checker Tool → Available
Market Trend Tool → Available

📅 EXECUTION SCHEDULE:
Day 1 → Identify top competitors
Day 2 → Collect competitor advertisements
Day 3 → Analyze ad messaging
Day 4 → Identify market trends
Day 5 → Generate strategy recommendations
```

### Example 2: Gemini-Powered Planner

```
Enter your marketing goal: Launch new eco-friendly product line

🌟 GEMINI-POWERED MARKETING PLANNING ASSISTANT

[Step 1/4] 🤖 AI analyzing your marketing goal...

   📍 Primary Objective: Successfully introduce sustainable product line to market
   🎯 Focus Areas: Product Launch, Sustainability, Market Penetration
   ⏱️ Timeline: 7-10 days

[Step 2/4] 📋 Breaking down into actionable tasks...

   ✅ Generated 6 tasks:
      • Market research and segmentation (2 days)
      • Competitor sustainability analysis (1 day)
      • Eco-friendly positioning strategy (1 day)
      • Green marketing campaign development (2 days)
      • Influencer partnership outreach (1 day)
      • Launch event planning (2 days)

💡 AI RECOMMENDATIONS:
   • Emphasize authentic sustainability claims
   • Target environmentally-conscious demographics
   • Leverage social proof through eco-influencers
   • Consider carbon-neutral shipping options
```

---

## 🐛 Troubleshooting

### Issue: Python not found

**Solution:**
```bash
# Check if Python is installed
python --version

# If not found, download from:
https://www.python.org/downloads/

# During installation, CHECK "Add Python to PATH"
```

### Issue: pip not recognized

**Solution:**
```bash
# Use this instead:
python -m pip install -r requirements.txt

# Or add Python Scripts to PATH:
# C:\Users\YourName\AppData\Local\Programs\Python\Python3x\Scripts
```

### Issue: ModuleNotFoundError

**Solution:**
```bash
# Ensure you're in the correct directory
cd marketing_agent

# Reinstall dependencies
pip install -r requirements.txt

# Activate virtual environment if using one
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### Issue: API Key errors

**Solution:**
```bash
# Verify key is set correctly
echo $GEMINI_API_KEY  # macOS/Linux
echo $env:GEMINI_API_KEY  # Windows PowerShell

# Should show your key without errors
# If blank, set it again
```

### Issue: Installation takes too long

**Solution:**
```bash
# Install only essential packages
pip install google-generativeai rich python-dotenv

# Skip optional packages like CrewAI if not needed
```

---

## 💡 Tips & Best Practices

### 1. Start with Simple Planner
- Test the system without API keys
- Understand the workflow
- Fast iteration

### 2. Upgrade to Gemini for Production
- FREE API with generous limits
- Better quality outputs
- More creative strategies

### 3. Use Virtual Environments
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 4. Save Your Plans
- Copy terminal output to text files
- Take screenshots of schedules
- Export to project management tools

### 5. Experiment with Goals
Try different marketing objectives:
- "Analyze competitor pricing strategy"
- "Launch social media campaign"
- "Identify new market segments"
- "Develop content marketing plan"

---

## 📚 Next Steps

Once you're comfortable with the basics:

1. **Explore the code structure**
   - Read `tools.py` to understand mock tools
   - Review `planner_agent.py` for agent logic
   - Check `scheduler.py` for timeline generation

2. **Customize for your needs**
   - Add industry-specific task templates
   - Modify tool implementations
   - Integrate real APIs

3. **Share feedback**
   - What features would help you?
   - What industries could benefit?
   - What integrations are needed?

---

## 🆘 Need Help?

### Resources:
- **README.md**: Full documentation
- **SETUP_INSTRUCTIONS.py**: Detailed setup guide
- **gemini_planner.py**: AI-powered version with comments

### Common Questions:

**Q: Do I need an API key?**  
A: No! The Simple Planner works without any API keys.

**Q: Which API is best?**  
A: Gemini is recommended (FREE, high quality). OpenAI is an alternative.

**Q: Can I use this commercially?**  
A: Yes! The mock tools work fine for prototyping. Replace with real APIs for production.

**Q: How do I customize tasks?**  
A: Edit the `decompose_tasks()` method in `planner_agent.py` or `gemini_planner.py`.

---

## 🎉 You're Ready!

Choose your mode and start planning:

```bash
# Simple mode (no API key)
python main.py

# AI-powered mode (recommended)
python gemini_planner.py
```

Happy marketing planning! 🚀✨
