````markdown
# 🤖 Multi-Agent Personal Assistant Swarm

## An Intelligent Collaborative AI System for Autonomous Task Planning, Execution, Validation, and Personalized Assistance

---

## 📌 Project Overview

The **Multi-Agent Personal Assistant Swarm** is a B.Tech final-year project in Artificial Intelligence and Data Science.

The system uses a **multi-agent architecture** to understand user requests, dynamically route tasks to specialized agents, maintain persistent memory, execute tools, validate generated responses, and produce a final response.

Instead of relying on a single agent for every task, the system divides responsibilities among specialized agents coordinated through a **Supervisor Agent** and **LangGraph workflow**.

---

## 🎯 Objectives

The main objectives of the project are:

- Build an intelligent personal assistant using multiple AI agents
- Dynamically route different user requests
- Provide specialized task processing
- Maintain persistent user interaction memory
- Execute tools such as calculations
- Validate generated responses
- Support retry and error-handling mechanisms
- Compare single-agent and multi-agent architectures
- Provide an interactive evaluation dashboard

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │        USER          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  SUPERVISOR AGENT    │
                    │  Dynamic Routing     │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌────────────┐   ┌────────────┐   ┌────────────┐
       │   TOOL     │   │  RESEARCH  │   │   DIRECT   │
       │   AGENT    │   │   AGENT    │   │   ROUTE    │
       └──────┬─────┘   └──────┬─────┘   └────────────┘
              │                │
              │                ▼
              │         ┌────────────┐
              │         │  ANALYSIS  │
              │         │   AGENT    │
              │         └──────┬─────┘
              │                │
              │                ▼
              │         ┌────────────┐
              │         │  WRITING   │
              │         │   AGENT    │
              │         └──────┬─────┘
              │                │
              │                ▼
              │         ┌────────────┐
              │         │ VALIDATOR  │
              │         │   AGENT    │
              │         └──────┬─────┘
              │                │
              └────────────────┘
                       │
                       ▼
              ┌────────────────────┐
              │   SQLITE MEMORY    │
              │ Persistent Memory  │
              └─────────┬──────────┘
                        │
                        ▼
              ┌────────────────────┐
              │   FINAL RESPONSE   │
              └────────────────────┘
````

---

## 🤖 AI Agents

### 1. Supervisor Agent

Responsible for understanding the user request and selecting the appropriate workflow.

### 2. Research Agent

Processes research and information-oriented requests.

### 3. Analysis Agent

Analyzes research information and extracts important points.

### 4. Writing Agent

Converts processed information into a structured final response.

### 5. Tool Agent

Provides controlled tool execution such as arithmetic calculations and date/time operations.

### 6. Validator Agent

Checks generated responses for structure, completeness, and basic quality requirements.

### 7. Memory Agent

Stores and retrieves previous interactions using persistent SQLite storage.

---

## 🔄 Workflow

The system follows a dynamic workflow:

```text
User Request
     ↓
Supervisor
     ↓
Memory Recall
     ↓
Dynamic Routing
     ↓
Specialized Agent
     ↓
Analysis / Writing
     ↓
Validation
     ↓
Retry if Required
     ↓
Memory Save
     ↓
Final Response
```

---

## 🧠 Memory System

The project uses **SQLite** for persistent memory.

Memory capabilities include:

* Saving previous interactions
* Searching previous memories
* Context retrieval
* Duplicate-memory detection
* Persistent storage
* Basic similarity-based retrieval

The database is stored locally in:

```text
memory/memory.db
```

---

## 🛠️ Technology Stack

* Python
* LangGraph
* LangChain
* Gemini API
* Google GenAI SDK
* Streamlit
* SQLite
* Pytest
* Git & GitHub

---

## 📂 Project Structure

```text
MULTI-AGENT PERSONAL ASSISTANTS
│
├── agents/
│   ├── research_agent.py
│   ├── planning_agent.py
│   ├── analysis_agent.py
│   ├── writing_agent.py
│   ├── supervisor_agent.py
│   ├── validator_agent.py
│   ├── memory_agent.py
│   └── tool_agent.py
│
├── memory/
│   ├── memory_store.py
│   └── memory.db
│
├── workflows/
│   └── agent_workflow.py
│
├── evaluation/
│   ├── evaluator.py
│   ├── dashboard.py
│   ├── single_agent_baseline.py
│   └── comparison.py
│
├── tests/
│   ├── test_memory.py
│   ├── test_tools.py
│   ├── test_routing.py
│   ├── test_agents.py
│   └── test_workflow.py
│
├── frontend/
│   └── app.py
│
├── documentation/
├── data/
├── models/
├── tools/
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🧪 Testing

The project contains an automated test suite covering:

* Memory functionality
* Tool functionality
* Agent functionality
* Routing
* Workflow execution

Current test result:

```text
51 tests passed
```

---

## 📊 Evaluation Results

The evaluation system was tested using five representative tasks:

1. Hello
2. Calculate 25 × 40
3. Artificial Intelligence explanation
4. Machine Learning explanation
5. Cloud Computing benefits and limitations

### Multi-Agent Evaluation

| Metric                   | Result |
| ------------------------ | -----: |
| Task Completion Rate     |   100% |
| Research Validation Rate |   100% |
| Tool Success Rate        |   100% |
| Memory Save Rate         |   100% |
| Total Tasks              |      5 |
| Completed Tasks          |      5 |
| Total Retries            |      0 |

### Route Distribution

| Route    | Tasks |
| -------- | ----: |
| Direct   |     1 |
| Tool     |     1 |
| Research |     3 |

---

## ⚖️ Single-Agent vs Multi-Agent Experiment

The same five tasks were evaluated using both architectures.

| Metric                  | Single-Agent | Multi-Agent |
| ----------------------- | -----------: | ----------: |
| Task Completion         |         100% |        100% |
| Average Execution Time  |   0.000151 s |  0.032959 s |
| Average Response Length |        272.0 |      1930.8 |
| Memory Save Rate        |           0% |        100% |
| Validation Rate         |          N/A |        100% |
| Tool Success            |          N/A |        100% |
| Total Retries           |            0 |           0 |

The multi-agent workflow introduces additional processing stages including routing, specialized agents, validation, and persistent memory.

Therefore, execution time is interpreted together with the additional capabilities provided by the architecture.

---

## 🖥️ Streamlit Application

The project includes an interactive Streamlit interface.

Run:

```powershell
streamlit run frontend\app.py --server.fileWatcherType none
```

The application provides:

* User request input
* Dynamic route selection
* Agent execution
* Final response
* Memory information
* Validation status
* Execution details

---

## 📊 Evaluation Dashboard

Run:

```powershell
streamlit run evaluation\dashboard.py --server.fileWatcherType none
```

The dashboard provides:

* System performance metrics
* Single-Agent vs Multi-Agent comparison
* Execution time comparison
* Response-length comparison
* Route distribution
* Validation metrics
* Tool success metrics
* Memory metrics
* Individual test-case results
* Architecture capability comparison

---

## ▶️ Running the Project

### 1. Clone the repository

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd "MULTI-AGENT PERSONAL ASSISTANTS"
```

### 2. Create virtual environment

```powershell
python -m venv venv
```

### 3. Activate environment

```powershell
venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Configure Gemini API

Create a `.env` file:

```text
GOOGLE_API_KEY=your_api_key_here
```

Never commit the `.env` file to GitHub.

---

## 🧪 Run Tests

```powershell
pytest -q
```

Expected result:

```text
51 passed
```

---

## 📊 Run Evaluation

```powershell
python evaluation\evaluator.py
```

---

## ⚖️ Run Architecture Comparison

```powershell
python evaluation\comparison.py
```

---

## 🖥️ Run Main Application

```powershell
streamlit run frontend\app.py --server.fileWatcherType none
```

---

## 📈 Run Evaluation Dashboard

```powershell
streamlit run evaluation\dashboard.py --server.fileWatcherType none
```

---

## 🔐 Security

API keys and environment variables are excluded from Git using `.gitignore`.

The project does not store the Gemini API key inside source code.

---

## 🚧 Current Limitations

* Current routing uses rule-based keyword classification in the local workflow.
* Local agent implementations are used when external Gemini services are unavailable.
* The evaluation dataset currently contains five test tasks.
* The current memory retrieval uses lightweight token-based similarity.
* External tool integrations are limited in the current implementation.

---

## 🔮 Future Scope

Future versions can include:

* More specialized AI agents
* Advanced semantic memory
* Vector database integration
* More external tools and APIs
* Web research integration
* Voice assistant capabilities
* Authentication
* Cloud deployment
* Docker deployment
* Azure deployment
* Advanced evaluation datasets
* LLM-based dynamic planning
* Agent-to-agent communication
* Human-in-the-loop approval
* Cost and token monitoring

---

## 🎓 Academic Project

**Project:** Multi-Agent Personal Assistant Swarm

**Degree:** B.Tech – Artificial Intelligence & Data Science

**Project Type:** Final Year Project

---

## 👩‍💻 Author

**Nimisha**

B.Tech – Artificial Intelligence & Data Science

````

### Then save and run these commands

```powershell
git status
````

Then:

```powershell
git add README.md evaluation\dashboard.py evaluation\single_agent_baseline.py evaluation\comparison.py
```

Then:

```powershell
git commit -m "Finalize evaluation dashboard and architecture comparison"
```

Then:

```powershell
git push origin main
```

After that, **Step 14 is complete** and we'll move to **Step 15: create the professional architecture diagram** for your report, PPT, GitHub README, and viva.
