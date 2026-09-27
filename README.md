# Multi-Agent Personal Assistant Swarm

## An Intelligent Collaborative AI System for Autonomous Task Planning, Execution, Validation, and Personalized Assistance

---

## Live Demo

Streamlit Application:

https://multi-agent-personal-assistant-ha8d49gexropn7sg2olj6m.streamlit.app/

The application provides an interactive interface for submitting user requests and observing the multi-agent workflow.

---

## Project Overview

The Multi-Agent Personal Assistant Swarm is a B.Tech final-year project in Artificial Intelligence and Data Science.

The system uses a multi-agent architecture to understand user requests, route tasks to specialized agents, maintain persistent memory, execute controlled tools, analyze information, validate generated responses, and produce a final response.

Instead of relying on a single component to perform every task, the system separates responsibilities across specialized agents. These agents are coordinated through a Supervisor Agent and a LangGraph-based workflow.

The project demonstrates a modular approach to building an intelligent personal assistant capable of handling different categories of user requests through specialized processing workflows.

---

## Problem Statement

Traditional personal assistant systems may rely on a single processing component to handle multiple types of tasks.

When routing, memory management, information processing, tool execution, response generation, and validation are combined into a single component, the system can become difficult to maintain, test, and extend.

This project addresses this problem by dividing the assistant into specialized agents. Each agent performs a specific responsibility while the overall workflow coordinates their execution.

The architecture is designed to provide modularity, structured processing, persistent memory, controlled tool execution, response validation, retry handling, and measurable system evaluation.

---

## Objectives

The primary objectives of the project are:

- Build an intelligent personal assistant using multiple specialized agents.
- Dynamically route different types of user requests.
- Separate responsibilities across specialized agents.
- Maintain persistent interaction memory.
- Execute controlled tools such as calculations and date/time operations.
- Process and analyze research-oriented requests.
- Generate structured responses.
- Validate generated responses before completion.
- Support retry and error-handling mechanisms.
- Compare single-agent and multi-agent architectures.
- Provide an interactive Streamlit application.
- Provide an evaluation dashboard.
- Measure system performance using automated tests and representative tasks.

---

## Key Features

### Multi-Agent Architecture

The system uses specialized agents for routing, memory, research, analysis, writing, tool execution, and validation.

### Dynamic Request Routing

The Supervisor Agent classifies requests into Direct, Tool, or Research workflows.

### Persistent Memory

SQLite is used to store and retrieve previous interactions.

### Research Processing

Research-oriented requests are processed through a dedicated Research Agent.

### Content Analysis

The Analysis Agent interprets research information and identifies important points, practical implications, and limitations.

### Structured Response Generation

The Writing Agent converts research and analysis into a structured final response.

### Tool Execution

The Tool Agent provides controlled operations including calculator, date/time, and basic text-analysis functionality.

### Response Validation

The Validator Agent checks generated responses for required structure, completeness, and obvious errors.

### Retry Handling

The workflow can retry response generation when validation fails and retry attempts remain.

### Interactive Application

A Streamlit interface provides an accessible way to interact with the system.

### Automated Testing

The project includes automated tests for memory, tools, routing, agents, and workflow execution.

### System Evaluation

The project includes a five-task evaluation and a Single-Agent versus Multi-Agent comparison.

---

## System Architecture

The overall architecture consists of a Supervisor Agent, specialized processing agents, persistent memory, controlled tools, validation, and a final response layer.

                         User Request
                              |
                              v
                     +-------------------+
                     | Supervisor Agent  |
                     | Dynamic Routing   |
                     +---------+---------+
                               |
                 +-------------+-------------+
                 |             |             |
                 v             v             v
          +-----------+  +-----------+  +-----------+
          | Tool      |  | Research  |  | Direct    |
          | Agent     |  | Agent     |  | Route     |
          +-----+-----+  +-----+-----+  +-----+-----+
                |              |               |
                |              v               |
                |       +-------------+        |
                |       | Analysis    |        |
                |       | Agent       |        |
                |       +------+------+        |
                |              |               |
                |              v               |
                |       +-------------+        |
                |       | Writing     |        |
                |       | Agent       |        |
                |       +------+------+        |
                |              |               |
                |              v               |
                |       +-------------+        |
                |       | Validator   |        |
                |       | Agent       |        |
                |       +------+------+        |
                |              |               |
                +--------------+---------------+
                               |
                               v
                      +------------------+
                      | Memory Agent     |
                      | SQLite Storage   |
                      +--------+---------+
                               |
                               v
                      +------------------+
                      | Final Response   |
                      +------------------+

---

## Agents and Responsibilities

| Agent | Responsibility |
|---|---|
| Supervisor Agent | Classifies requests and selects the appropriate workflow |
| Memory Agent | Stores and retrieves previous interactions |
| Research Agent | Processes research-oriented requests |
| Analysis Agent | Analyzes research information and identifies important insights |
| Writing Agent | Generates structured final responses |
| Tool Agent | Executes controlled tools such as calculations and date/time |
| Validator Agent | Validates generated responses and supports retry handling |

---

## Supervisor Agent

The Supervisor Agent acts as the routing component of the system.

Its primary responsibility is to analyze the incoming user request and determine which workflow should be executed.

The system currently supports three main routes:

User Request
     |
     v
Supervisor Agent
     |
     +----> Research
     |
     +----> Tool
     |
     +----> Direct

### Research Route

Research-related requests are routed to the Research Agent.

Examples:

- Explain artificial intelligence in healthcare.
- Research machine learning.
- Compare cloud computing concepts.

### Tool Route

Requests requiring controlled computation or utility operations are routed to the Tool Agent.

Examples:

- Calculate 25 * 40 + 100.
- What is the current time?
- Perform a text analysis.

### Direct Route

Simple conversational requests can be processed through the direct workflow.

Example:

- Hello, how are you?

---

## Memory Agent

The Memory Agent provides persistent storage and retrieval for previous interactions.

The project uses SQLite as the persistent memory backend.

The memory system stores information using:

- Content
- Category
- Creation timestamp

The Memory Agent provides operations for:

- Saving memories
- Recalling relevant memories
- Counting stored memories
- Closing the memory connection

The system uses token-based similarity matching to identify relevant previous information.

Memory is integrated into the workflow so that previous interactions can provide supporting context for new requests.

---

## Research Agent

The Research Agent processes research-oriented requests.

Its responsibility is to create structured research information based on the current user request.

The agent identifies the topic from the current request and organizes the information into sections such as:

- Introduction
- Research Summary
- Key Benefits
- Risks and Limitations
- Practical Applications
- Challenges
- Current Trends
- Validation Considerations
- Conclusion

The Research Agent is designed so that previous memory provides supporting context without overriding the topic of the current request.

For example, a request such as:

Research artificial intelligence in healthcare

produces healthcare-specific research rather than incorrectly reusing unrelated previous memories.

---

## Analysis Agent

The Analysis Agent processes the research output and extracts meaningful insights.

The analysis includes:

- Topic relevance
- Main concepts
- Important points
- Practical interpretation
- Limitations
- Final assessment

For healthcare-related research, the analysis can consider areas such as:

- Medical imaging
- Electronic health records
- Disease and health-risk prediction
- Clinical decision support
- Patient monitoring
- Drug discovery
- Clinical documentation
- Personalized healthcare

The Analysis Agent helps transform raw research information into a structured interpretation.

---

## Writing Agent

The Writing Agent converts research and analysis information into a structured final response.

The generated response contains sections such as:

1. Introduction
2. Research Summary
3. Key Benefits
4. Risks and Limitations
5. Practical Applications
6. Analysis
7. Challenges
8. Current Trends
9. Validation Considerations
10. Conclusion

The Writing Agent also receives the current user request so that the generated response remains aligned with the requested topic.

---

## Tool Agent

The Tool Agent is responsible for executing controlled utility operations.

Currently supported tools include:

### Calculator

Performs arithmetic expressions safely.

Example:

25 * 40 + 100

Result:

1100

### Date and Time

Provides date and time information.

### Text Analysis

Provides basic text statistics including:

- Characters
- Words
- Sentences

The Tool Agent uses controlled execution instead of directly evaluating arbitrary Python code.

---

## Validator Agent

The Validator Agent checks the generated response before it is returned to the user.

Validation includes checks for:

- Required sections
- Response completeness
- Empty responses
- Obvious error messages
- Minimum response quality

For research responses, the validator checks that the expected structured sections are present.

If validation fails and retry attempts remain, the workflow can return to response generation.

Writing Agent
      |
      v
Validator Agent
      |
      +---- PASS ----> Final Response
      |
      +---- FAIL ----> Retry

The current implementation uses a maximum retry limit of two attempts.

---

## Workflow

The project uses LangGraph to coordinate the multi-agent workflow.

### Research Workflow

START
  |
  v
Supervisor
  |
  v
Memory Recall
  |
  v
Research Agent
  |
  v
Analysis Agent
  |
  v
Writing Agent
  |
  v
Validator Agent
  |
  +---- PASS ----> Memory Save ----> END
  |
  +---- FAIL ----> Retry

### Tool Workflow

START
  |
  v
Supervisor
  |
  v
Memory Recall
  |
  v
Tool Agent
  |
  v
Memory Save
  |
  v
END

### Direct Workflow

START
  |
  v
Supervisor
  |
  v
Memory Recall
  |
  v
Direct Response
  |
  v
Memory Save
  |
  v
END

### Validation and Retry Workflow

Writing Agent
     |
     v
Validator Agent
     |
     +---- PASS
     |       |
     |       v
     |    Final Response
     |
     +---- FAIL
             |
             v
          Retry Count
             |
       +-----+-----+
       |           |
     Retry       Limit
       |           |
       v           v
 Writing Agent   Validation
                Failure

---

## Memory System

The persistent memory system is implemented using SQLite.

The database is stored in:

memory/memory.db

The memory table stores:

id
content
category
created_at

The memory system supports similarity-based retrieval using tokenization and cosine similarity.

The memory workflow is:

User Request
     |
     v
Memory Search
     |
     v
Relevant Previous Context
     |
     v
Specialized Agent
     |
     v
Final Response
     |
     v
Save New Memory

The memory system allows the assistant to preserve useful context across interactions.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| LangGraph | Agent workflow orchestration |
| LangChain | AI application framework |
| Google Gemini | Generative AI integration |
| Streamlit | Interactive web interface |
| SQLite | Persistent memory storage |
| ChromaDB | Earlier memory experimentation |
| Pydantic | Data validation and structured data |
| Pandas | Data processing and evaluation |
| NumPy | Numerical processing |
| Pytest | Automated testing |
| Git | Version control |
| GitHub | Source-code hosting |

---

## Project Structure

MULTI-AGENT PERSONAL ASSISTANTS
|
+-- agents/
|   +-- __init__.py
|   +-- test_gemini.py
|   +-- research_agent.py
|   +-- planning_agent.py
|   +-- analysis_agent.py
|   +-- writing_agent.py
|   +-- supervisor_agent.py
|   +-- validator_agent.py
|   +-- memory_agent.py
|   +-- tool_agent.py
|
+-- data/
|
+-- documentation/
|
+-- evaluation/
|   +-- __init__.py
|   +-- evaluator.py
|   +-- dashboard.py
|   +-- single_agent_baseline.py
|   +-- comparison.py
|
+-- frontend/
|   +-- app.py
|
+-- memory/
|   +-- __init__.py
|   +-- memory_store.py
|
+-- models/
|
+-- tests/
|   +-- __init__.py
|   +-- test_memory.py
|   +-- test_tools.py
|   +-- test_routing.py
|   +-- test_agents.py
|   +-- test_workflow.py
|
+-- venv/
|
+-- .gitignore
+-- README.md
+-- requirements.txt

---

## Streamlit Application

The project provides an interactive Streamlit interface.

The application allows users to:

- Enter a request.
- Submit the request to the multi-agent workflow.
- Observe the selected route.
- View the generated response.
- Review workflow-related information.

The application can be started using:

streamlit run frontend\app.py --server.fileWatcherType none

The public deployment is available at:

https://multi-agent-personal-assistant-ha8d49gexropn7sg2olj6m.streamlit.app/

---

## Evaluation Dashboard

The project contains an evaluation dashboard for reviewing system performance.

The dashboard is implemented in:

evaluation/dashboard.py

It can be used to display evaluation results and compare different system configurations.

---

## Testing

The project includes automated tests covering the major components.

Test categories include:

- Memory tests
- Tool tests
- Routing tests
- Agent tests
- Workflow tests

The complete test suite currently contains:

51 passed

The latest complete test execution completed successfully.

---

## Evaluation Methodology

The system was evaluated using representative user requests covering:

- Research
- Tool execution
- Direct conversation
- Memory handling
- Response validation
- Workflow execution

The evaluation measures:

- Task completion
- Research validation
- Tool success
- Memory saving
- Retry behavior
- Route distribution
- Execution time
- Response length

---

## Multi-Agent Evaluation Results

The latest five-task evaluation produced the following results:

| Metric | Result |
|---|---:|
| Total Tasks | 5 |
| Completed Tasks | 5 |
| Completion Rate | 100% |
| Research Validation | 100% |
| Tool Success | 100% |
| Memory Save | 100% |
| Retries | 0 |
| Average Execution Time | 0.021298 seconds |
| Average Response Length | 1933.6 characters |

---

## Route Distribution

The five-task evaluation produced the following route distribution:

| Route | Number of Tasks |
|---|---:|
| Direct | 1 |
| Tool | 1 |
| Research | 3 |
| Total | 5 |

---

## Single-Agent versus Multi-Agent Comparison

The project includes a comparison between a baseline Single-Agent approach and the Multi-Agent architecture.

| Metric | Single-Agent | Multi-Agent |
|---|---:|---:|
| Completion Rate | 100% | 100% |
| Average Execution Time | 0.000135 seconds | 0.021298 seconds |
| Average Response Length | 272.0 characters | 1933.6 characters |
| Memory Save | 0% | 100% |
| Validation | Not applied in the same workflow | 100% |
| Tool Success | Not measured in the same workflow | 100% |
| Retries | Not used in the same workflow | 0 |

The comparison demonstrates that the Multi-Agent architecture introduces additional workflow processing while providing explicit specialization, memory handling, validation, and tool integration.

The Single-Agent and Multi-Agent measurements were produced using the project's evaluation scripts and are intended as project-level experimental results rather than universal performance benchmarks.

---

## Installation and Setup

### 1. Clone the Repository

git clone <YOUR-GITHUB-REPOSITORY-URL>
cd MULTI-AGENT-PERSONAL-ASSISTANTS

### 2. Create a Virtual Environment

python -m venv venv

### 3. Activate the Virtual Environment

venv\Scripts\activate

### 4. Install Dependencies

pip install -r requirements.txt

### 5. Configure the API Key

Create a .env file in the project root.

GOOGLE_API_KEY=your_api_key_here

Do not commit the .env file to GitHub.

The project .gitignore should exclude:

.env
venv/
__pycache__/
*.pyc

---

## Running the Project

### Run the Streamlit Application

streamlit run frontend\app.py --server.fileWatcherType none

### Run the Evaluation Dashboard

streamlit run evaluation\dashboard.py

### Run All Tests

pytest -q

### Run Evaluation

python evaluation\evaluator.py

### Run Single-Agent versus Multi-Agent Comparison

python evaluation\comparison.py

---

## Example Requests

### Research Request

Research artificial intelligence in healthcare

Expected route:

Research

Expected processing:

Supervisor
    |
    v
Memory
    |
    v
Research
    |
    v
Analysis
    |
    v
Writing
    |
    v
Validation
    |
    v
Final Response

### Tool Request

Calculate 25 * 40 + 100

Expected route:

Tool

Expected result:

1100

### Direct Request

Hello, how are you?

Expected route:

Direct

---

## Security

The project uses environment variables for API credentials.

API keys should never be hard-coded into source files or committed to GitHub.

The .env file should remain local and should be included in .gitignore.

If an API key has accidentally been exposed publicly, it should be revoked and regenerated through the relevant provider.

---

## Current Limitations

The current implementation has several limitations.

### Rule-Based Routing

The Supervisor Agent currently uses rule-based keyword routing rather than a fully autonomous language-model-based routing strategy.

### Local Research Knowledge

The current Research Agent uses structured topic knowledge and does not provide unrestricted live web research.

### Memory Retrieval

Memory retrieval currently uses lightweight token-based similarity rather than a full production vector database architecture.

### External Tools

The current Tool Agent supports a controlled set of utility operations.

### Validation

The Validator Agent performs structural and error-oriented validation. It is not a substitute for comprehensive factual verification.

### Production Deployment

The current project is designed primarily as an academic prototype and demonstration system rather than a production healthcare or enterprise assistant.

---

## Future Scope

Possible future improvements include:

- LLM-based autonomous planning.
- More advanced dynamic agent selection.
- Real-time web research.
- Additional external API integrations.
- Advanced vector database memory.
- Semantic embeddings for memory retrieval.
- Long-term user preference modeling.
- More sophisticated response validation.
- Automatic fact verification.
- More advanced tool orchestration.
- Human-in-the-loop approval workflows.
- Improved security controls.
- Production-grade observability.
- Distributed agent execution.
- Advanced evaluation datasets.
- Multi-user support.
- Voice-based interaction.
- Additional enterprise integrations.

---

## Project Demonstration

The project can be demonstrated using three primary scenarios.

### Scenario 1: Research

Input:

Research artificial intelligence in healthcare

Demonstrates:

- Supervisor routing
- Memory retrieval
- Research Agent
- Analysis Agent
- Writing Agent
- Validator Agent
- Memory saving

### Scenario 2: Tool Execution

Input:

Calculate 25 * 40 + 100

Demonstrates:

- Supervisor routing
- Tool Agent
- Controlled calculation
- Memory saving

### Scenario 3: Direct Conversation

Input:

Hello, how are you?

Demonstrates:

- Supervisor routing
- Direct response
- Memory saving

---

## Documentation

The project documentation package contains:

- Final Project Report
- Architecture and Agent Explanation
- Five-Minute Demo Script
- Viva Questions and Answers
- Testing and Evaluation Report
- GitHub and README Submission Guide
- Screenshot and Evidence Checklist
- Final Presentation Slide Guide
- Final Submission Checklist
- Installation and Run Guide

These documents provide supporting material for project demonstration, academic evaluation, viva preparation, and final submission.

---

## Academic Information

### Project Type

B.Tech Final Year Project

### Domain

Artificial Intelligence and Data Science

### Project Category

Multi-Agent Artificial Intelligence System

### Primary Technologies

Python, LangGraph, LangChain, Google Gemini, Streamlit, SQLite, Pytest

### Project Title

Multi-Agent Personal Assistant Swarm: An Intelligent Collaborative AI System for Autonomous Task Planning, Execution, Validation, and Personalized Assistance

---

## Author

Developed as a B.Tech Artificial Intelligence and Data Science final-year project.

---

## Conclusion

The Multi-Agent Personal Assistant Swarm demonstrates how specialized AI agents can collaborate through a structured workflow to process different categories of user requests.

The system separates routing, memory, research, analysis, writing, tool execution, and validation into dedicated components.

The project currently achieves successful execution across the implemented test suite and representative evaluation tasks while providing a modular foundation for future improvements.

The architecture can be extended with more advanced planning, real-time research, semantic memory, additional tools, stronger validation, and production-oriented deployment capabilities.