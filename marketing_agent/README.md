# Marketing Planning Assistant Agent

An AI-powered planning assistant that automatically decomposes high-level marketing goals into actionable tasks, validates resources, and generates execution schedules.

## 📋 Project Overview

This project implements an **Agentic AI system** using CrewAI/LangChain that performs multi-step reasoning to create comprehensive marketing execution plans. The agent autonomously:

1. ✅ Interprets marketing objectives
2. ✅ Decomposes goals into actionable tasks
3. ✅ Validates required resources using mock tools
4. ✅ Generates structured execution plans
5. ✅ Creates detailed timelines and schedules

## 🎯 Features

### Core Capabilities

- **Goal Interpretation**: Understands high-level marketing objectives and extracts clear success criteria
- **Task Decomposition**: Automatically breaks down complex goals into 5-7 sequential tasks
- **Resource Validation**: Validates availability of marketing tools and budget allocation
- **Schedule Generation**: Creates day-by-day execution timelines with dependencies
- **Multi-Agent Architecture**: Uses specialized agents for different planning aspects (optional with CrewAI)

### Mock Marketing Tools

The system includes four realistic mock tools:

1. **CompetitorResearchTool**: Identifies competitors and analyzes their strategies
2. **AdDatabaseTool**: Collects and analyzes competitor advertisements
3. **BudgetCheckerTool**: Validates budget allocation and availability
4. **MarketTrendTool**: Identifies industry trends and consumer preferences

## 🏗️ Architecture

```
marketing_agent/
│
├── main.py                 # Entry point and user interface
├── planner_agent.py        # Planner Agent (CrewAI or Simple mode)
├── tools.py               # Mock marketing tools implementation
├── scheduler.py           # Timeline and schedule generation
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

### Component Details

#### `main.py`
- User input handling
- Orchestrates the planning process
- Displays formatted output
- Supports interactive sessions

#### `planner_agent.py`
- **PlannerAgent**: Full CrewAI-based multi-agent system (requires LLM API key)
- **SimplePlanner**: Rule-based planner (works without API key)
- Goal interpretation and task decomposition logic
- Resource validation workflows

#### `tools.py`
- CompetitorResearchTool with mock competitor data
- AdDatabaseTool with sample ad campaigns
- BudgetCheckerTool with allocation recommendations
- MarketTrendTool with industry trend analysis

#### `scheduler.py`
- Dependency-aware task scheduling
- Day-by-day timeline generation
- Critical path identification
- Milestone tracking

## 🚀 Quick Start

### Web Interface (Recommended)
The project now includes a professional React-based web dashboard.

1. **Start the Web Server:**
   ```bash
   python api.py
   ```
2. **Access the Dashboard:**
   Open your browser and navigate to `http://localhost:8000`

### CLI Mode
1. **Navigate to the project directory:**
   ```bash
   cd marketing_agent
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (optional for CrewAI mode):**
   
   Create a `.env` file in the project directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   
   Or set it directly:
   ```bash
   # Windows (PowerShell)
   $env:OPENAI_API_KEY="your-api-key-here"
   
   # macOS/Linux
   export OPENAI_API_KEY="your-api-key-here"
   ```

### Running the Agent

**Basic usage (Simple Planner - no API key required):**

```bash
python main.py
```

**With CrewAI mode (requires API key):**

1. Set your `OPENAI_API_KEY` environment variable
2. Edit `main.py` and change `USE_CREWAI = False` to `USE_CREWAI = True`
3. Run: `python main.py`

## 📝 Example Usage

### Input Example

When prompted, enter a marketing goal:

```
Enter your marketing goal: Analyze competitor ads for a smartphone brand
```

### Output Example

The system will generate:

```
======================================================================
PLAN OUTPUT
======================================================================

GOAL: Analyze competitor ads for a smartphone brand

📋 TASK PLAN:
1. Identify top competitors
   Description: Research and identify key competitors in the market segment
   Required Tools: CompetitorResearchTool
   Estimated Time: 1 day(s)
   Deliverables: Competitor list with market share data

2. Collect competitor advertisements
   Description: Gather and catalog competitor ad campaigns across platforms
   Required Tools: AdDatabaseTool
   Estimated Time: 1 day(s)
   Dependencies: Task numbers [1]
   Deliverables: Ad collection database

3. Analyze ad messaging
   Description: Analyze themes, tone, and messaging strategies in competitor ads
   Required Tools: AdDatabaseTool
   Estimated Time: 1 day(s)
   Dependencies: Task numbers [2]
   Deliverables: Messaging analysis report

4. Identify market trends
   Description: Research current and emerging trends in the industry
   Required Tools: MarketTrendTool
   Estimated Time: 1 day(s)
   Dependencies: Task numbers [1]
   Deliverables: Trend analysis report

5. Generate strategy recommendations
   Description: Synthesize findings into actionable strategy recommendations
   Required Tools: BudgetCheckerTool
   Estimated Time: 1 day(s)
   Dependencies: Task numbers [3, 4]
   Deliverables: Comprehensive strategy document

✅ RESOURCE VALIDATION:
Competitor Research Tool → Available
Ad Database Tool → Available
Budget Checker Tool → Available
Market Trend Tool → Available

📅 EXECUTION SCHEDULE:
Day 1: Identify top competitors
Day 2: Collect competitor ads
Day 3: Analyze ad messaging
Day 4: Identify market trends
Day 5: Generate strategy recommendations

======================================================================
```

## 🔧 How It Works

### Step 1: Goal Interpretation

The agent analyzes the marketing goal to identify:
- Primary objective
- Focus areas (competitive analysis, advertising, trends, etc.)
- Complexity level
- Success metrics

### Step 2: Task Decomposition

Using either:
- **CrewAI Mode**: LLM-powered task decomposition via specialized agents
- **Simple Mode**: Rule-based decomposition using predefined templates

Generates 5-7 sequential tasks with:
- Clear descriptions
- Required tools
- Duration estimates
- Dependencies
- Deliverables

### Step 3: Resource Validation

The system validates:
- Tool availability for each task
- Budget allocation appropriateness
- Resource conflicts or constraints

### Step 4: Schedule Generation

Creates a timeline with:
- Day-by-day task assignments
- Dependency-aware ordering
- Critical path identification
- Milestone markers

## 🧪 Testing the Tools

You can test individual components:

```python
from tools import initialize_all_tools

# Initialize all tools
tools = initialize_all_tools()

# Test CompetitorResearchTool
competitor_tool = tools['competitor_research']
competitors = competitor_tool.identify_competitors('technology', 'smartphone')
print(f"Found {len(competitors)} competitors")

# Test AdDatabaseTool
ad_tool = tools['ad_database']
ads = ad_tool.collect_ads('TechCorp')
print(f"Collected {len(ads)} ads")

# Test MarketTrendTool
trend_tool = tools['market_trend']
trends = trend_tool.identify_trends('technology')
print(f"Trending topics: {trends['trending_topics']}")
```

## ⚙️ Configuration Options

### Using CrewAI vs Simple Planner

**Simple Planner (Default)**
- ✅ No API key required
- ✅ Fast execution
- ✅ Deterministic outputs
- ❌ Less flexible interpretation

**CrewAI Planner**
- ✅ Intelligent goal interpretation
- ✅ More creative task decomposition
- ✅ Better handling of complex goals
- ❌ Requires OpenAI API key
- ❌ Slower execution
- ❌ API costs

### Switching LLM Models

If using CrewAI, you can change the model in `planner_agent.py`:

```python
def __init__(self, llm_model: str = "gpt-4"):
    # Change to:
    # llm_model = "gpt-3.5-turbo"  # Faster, cheaper
    # llm_model = "gpt-4-turbo"    # Latest GPT-4
```

## 📊 Sample Marketing Goals

Try these example goals:

1. *"Analyze competitor ads for a smartphone brand"*
2. *"Launch a new product in the fashion industry"*
3. *"Increase social media engagement by 50%"*
4. *"Identify emerging market trends in tech"*
5. *"Develop a content marketing strategy"*
6. *"Plan an influencer marketing campaign"*
7. *"Research customer segmentation opportunities"*

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'crewai'`
- **Solution**: Install dependencies: `pip install -r requirements.txt`

**Issue**: `OPENAI_API_KEY not found`
- **Solution**: Either set the API key or use Simple Planner mode (default)

**Issue**: Tasks not displaying correctly
- **Solution**: Ensure terminal width is at least 70 characters

**Issue**: Import errors in planner_agent.py
- **Solution**: Make sure you're running from the `marketing_agent` directory

## 📈 Extending the System

### Adding New Tools

1. Create a new tool class in `tools.py`:

```python
class SocialMediaTool:
    def __init__(self):
        self.name = "SocialMediaTool"
        self.description = "Analyzes social media metrics"
    
    def analyze_engagement(self, platform: str) -> dict:
        # Implementation
        pass
```

2. Add to the tool registry:

```python
MARKETING_TOOLS["SocialMediaTool"] = SocialMediaTool
```

### Customizing Task Templates

Modify the `decompose_tasks()` method in `planner_agent.py` to add industry-specific task templates.

### Integrating Real APIs

Replace mock tools with real API integrations:

```python
class RealCompetitorTool(CompetitorResearchTool):
    def identify_competitors(self, industry: str, product_type: str):
        # Call actual API instead of returning mock data
        response = api_client.get_competitors(industry, product_type)
        return response.data
```

## 🎓 Learning Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [Agentic AI Patterns](https://github.com/joaomdmoura/crewai)

## 📄 License

This project is provided as-is for educational and demonstration purposes.

## 👨‍💻 Author

Generated by an expert Python AI engineer specializing in Agentic AI systems.

## 🤝 Contributing

Feel free to extend this project with:
- Additional marketing tools
- Real API integrations
- Enhanced scheduling algorithms
- Custom output formats
- Industry-specific templates

---

**Happy Marketing Planning! 🚀**
