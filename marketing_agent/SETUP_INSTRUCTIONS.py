"""
Setup Instructions for Marketing Planning Assistant Agent.

This file provides quick setup instructions for different configurations.
"""

# ============================================================================
# SETUP OPTIONS - CHOOSE YOUR PREFERRED MODE
# ============================================================================

"""
OPTION 1: Simple Planner (NO API KEY REQUIRED) ⭐ RECOMMENDED FOR TESTING
---------------------------------------------------------------------------
✅ No API keys needed
✅ Works immediately
✅ Fast execution
✅ Perfect for testing and demos

Steps:
1. Install Python dependencies: pip install -r requirements.txt
2. Run: python main.py
3. That's it!

"""

"""
OPTION 2: CrewAI with OpenAI GPT (Advanced Multi-Agent System)
---------------------------------------------------------------------------
✅ Intelligent goal interpretation
✅ Creative task decomposition
✅ Multi-agent collaboration
❌ Requires OpenAI API key
❌ API costs apply

Steps:
1. Get OpenAI API key from: https://platform.openai.com/api-keys
2. Create .env file in this directory:
   OPENAI_API_KEY=sk-your-key-here
   
3. Edit main.py line ~165: USE_CREWAI = True
4. Install: pip install -r requirements.txt
5. Run: python main.py

"""

"""
OPTION 3: LangChain with Gemini API (Google's AI) 🌟 RECOMMENDED FOR PRODUCTION
---------------------------------------------------------------------------
✅ High-quality responses
✅ Competitive pricing
✅ Google's advanced models
❌ Requires Google account
❌ API key setup needed

Steps:
1. Get Gemini API key from: https://makersuite.google.com/app/apikey
2. Create .env file in this directory:
   GEMINI_API_KEY=your-gemini-key-here
   
3. Edit planner_agent.py to use Gemini (see gemini_planner.py example)
4. Install: pip install -r requirements.txt
5. Run: python main.py

"""

# ============================================================================
# QUICK START COMMANDS
# ============================================================================

"""
Windows PowerShell:
-------------------
# Navigate to project
cd "c:\Planner Agent\marketing_agent"

# Install dependencies
python -m pip install -r requirements.txt

# Run the application
python main.py

# Set environment variable (temporary for session)
$env:OPENAI_API_KEY="your-key-here"
# OR
$env:GEMINI_API_KEY="your-key-here"

"""

"""
macOS/Linux Terminal:
--------------------
# Navigate to project
cd "c:/Planner Agent/marketing_agent"

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py

# Set environment variable
export OPENAI_API_KEY="your-key-here"
# OR
export GEMINI_API_KEY="your-key-here"

"""

# ============================================================================
# ENVIRONMENT VARIABLES REFERENCE
# ============================================================================

"""
Create a .env file in the marketing_agent directory:

# For OpenAI
OPENAI_API_KEY=sk-...

# For Gemini
GEMINI_API_KEY=...

# Optional: Custom configuration
LLM_MODEL=gemini-pro
TEMPERATURE=0.7
MAX_TOKENS=2000

"""

# ============================================================================
# TROUBLESHOOTING
# ============================================================================

"""
Issue: Python not found
Solution: 
- Download from https://www.python.org/downloads/
- Check "Add Python to PATH" during installation

Issue: pip not recognized
Solution:
- Use: python -m pip install ...
- Or add Python Scripts folder to PATH

Issue: ModuleNotFoundError
Solution:
- Ensure you're in the marketing_agent directory
- Run: pip install -r requirements.txt
- Activate virtual environment if using one

Issue: API Key errors
Solution:
- Verify key is correct (no extra spaces)
- Check API key has proper permissions
- Ensure billing is enabled on your account

"""

# ============================================================================
# VERIFICATION TEST
# ============================================================================

"""
Test without API key (Simple mode):
------------------------------------
python -c "from tools import initialize_all_tools; tools = initialize_all_tools(); print('✅ Tools loaded successfully!')"

Test with mock data:
--------------------
python -c "
from tools import CompetitorResearchTool
tool = CompetitorResearchTool()
competitors = tool.identify_competitors('technology', 'smartphone')
print(f'✅ Found {len(competitors)} competitors')
for c in competitors:
    print(f'  - {c[\"name\"]}: {c[\"market_share\"]}')
"

"""
