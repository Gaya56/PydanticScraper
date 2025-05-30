# Framework Workflow

## How It Works: Simple Visual Guide

```
┌─────────────────┐
│   User Prompt   │ ──────┐
│ "Find NBA games │       │
│  today"         │       │
└─────────────────┘       │
                          │
                          ▼
┌─────────────────────────────────────────┐
│           Pydantic AI Agent             │
│  • Reads prompt                         │
│  • Decides which tools to use           │
│  • Chains operations automatically      │
└─────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────┐
│           MCP Tool Discovery            │
│  • brave_search.py (Web Search)         │
│  • python_tools.py (Data Processing)    │
│  • Auto-detects available functions     │
└─────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────┐
│         Execute Tool Chain              │
│  1. Search web for "NBA games today"    │
│  2. Parse and filter results            │
│  3. Create data visualization           │
│  4. Format final report                 │
└─────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────┐
│         Formatted Output                │
│  • Game schedules with times            │
│  • Team matchups                        │
│  • TV broadcast info                    │
│  • Optional charts/graphs               │
└─────────────────────────────────────────┘
```

## The Workflow Explained

**Step 1: Prompt Analysis**
When you provide a natural language prompt like "Find NBA games today," the Pydantic AI agent intelligently parses your request and determines what tools and operations are needed to fulfill it.

**Step 2: Tool Discovery**
The Model Context Protocol (MCP) automatically discovers available tools from your MCP servers. Each `.py` file in your project can expose different capabilities - web searching, data processing, visualization, etc.

**Step 3: Intelligent Orchestration** 
The AI agent doesn't just call one tool - it creates a logical sequence. For NBA games, it might: search the web, filter for relevant sports sites, extract game information, and then format the results in a readable way.

**Step 4: Dynamic Execution**
Each tool runs independently but passes data seamlessly to the next. The brave_search.py tool finds raw web data, while python_tools.py can process, analyze, and visualize that data without any manual intervention.

**Step 5: Rich Output**
The final result isn't just text - it's a comprehensive report with properly formatted data, citations, and even charts or graphs when relevant. Everything is generated automatically based on your simple prompt.

**Why This Works**
The magic is in the modular design. Each MCP tool is a specialist that does one thing well. The AI agent acts as the coordinator, deciding how to combine these specialists to solve complex tasks. You get enterprise-level data processing with the simplicity of a single sentence request.

This approach scales beautifully - add more MCP tools and your agent becomes more capable, all without changing your core application logic.
