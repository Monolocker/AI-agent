# AI Code Fixer Agent

Based on the concept of agentic workflows, this project was built using Python and Google's Gemini API as part of the [Boot.dev](https://www.boot.dev) curriculum to explore LLM function calling, autonomous problem solving, and enhancing functional programming skills. 

## Features

- **Autonomous Debugging:** The agent analyzes tracebacks and source code to identify errors. 
- **Tool Integration:** Uses Gemini's function calling to interact with the local filesystem and execute Python scripts. 
- **Feedback Loop:** Iteratively runs code and checks output
- **Safety Scoping:** Operations are constrained to a specific directory to ensure only intended files are modified

## Prerequisites 
- Python 3.10+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed
- A Gemini API Key from [Google AI Studio](https://aistudio.google.com/welcome)

## Installation 
```bash 
# Clone the repo 
git clone https://github.com/Monolocker/AI-agent.git

# Navigate to the project folder 
cd ai-agent

# Setup your environment variables 
echo "GEMINI_API_KEY=your_key_here" > .env

# Install dependencies and setup virtual environment 
uv sync
