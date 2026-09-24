import sys
import os
from typing import TypedDict

# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# IMPORT AGENTS
# ============================================================

from langgraph.graph import StateGraph, START, END

from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.writing_agent import WritingAgent
from agents.validator_agent import ValidatorAgent
from agents.tool_agent import ToolAgent
from agents.memory_agent import MemoryAgent


# ============================================================
# AGENT INITIALIZATION
# ============================================================

research_agent = ResearchAgent()
analysis_agent = AnalysisAgent()
writing_agent = WritingAgent()
validator_agent = ValidatorAgent()
tool_agent = ToolAgent()
memory_agent = MemoryAgent()


# ============================================================
# CONFIGURATION
# ============================================================

MAX_RETRIES = 2


# ============================================================
# WORKFLOW STATE
# ============================================================

class AgentState(TypedDict):

    user_request: str

    route: str

    memory_context: str

    research: str

    analysis: str

    writing: str

    validation: str

    tool_result: str

    final_response: str

    memory_saved: bool

    retry_count: int


# ============================================================
# SUPERVISOR
# ============================================================

def supervisor_node(state: AgentState):

    user_request = state["user_request"]

    print("\n")
    print("=" * 60)
    print("SUPERVISOR AGENT")
    print("=" * 60)

    print("\nAnalyzing request:")
    print(user_request)

    request_lower = user_request.lower()

    # --------------------------------------------------------
    # TOOL KEYWORDS
    # --------------------------------------------------------

    tool_keywords = [
        "calculate",
        "calculator",
        "compute",
        "percentage",
        "percent",
        "sum",
        "multiply",
        "divide",
        "date",
        "time",
        "current time"
    ]

    # --------------------------------------------------------
    # RESEARCH KEYWORDS
    # --------------------------------------------------------

    research_keywords = [
        "research",
        "explain",
        "latest",
        "information",
        "compare",
        "advantages",
        "disadvantages",
        "benefits",
        "risks",
        "what is"
    ]

    # --------------------------------------------------------
    # ROUTING
    # --------------------------------------------------------

    if any(
        keyword in request_lower
        for keyword in tool_keywords
    ):

        route = "tool"

    elif any(
        keyword in request_lower
        for keyword in research_keywords
    ):

        route = "research"

    else:

        route = "direct"

    print(
        f"\nSupervisor selected route: "
        f"{route.upper()}"
    )

    return {
        "route": route
    }


# ============================================================
# MEMORY RECALL
# ============================================================

def memory_recall_node(state: AgentState):

    user_request = state["user_request"]

    print("\n")
    print("=" * 60)
    print("MEMORY AGENT")
    print("=" * 60)

    print("\nSearching previous memories...")

    results = memory_agent.recall(
        user_request,
        number_of_results=5
    )

    if not results:

        memory_context = (
            "No relevant previous memories were found."
        )

        print("\nNo relevant memories found.")

    else:

        memory_lines = []

        for index, result in enumerate(
            results,
            start=1
        ):

            memory_lines.append(
                f"{index}. {result}"
            )

        memory_context = "\n".join(
            memory_lines
        )

        print("\nRelevant memories:")

        print(memory_context)

    return {
        "memory_context": memory_context
    }


# ============================================================
# TOOL NODE
# ============================================================

def tool_node(state: AgentState):

    user_request = state["user_request"]

    print("\n")
    print("=" * 60)
    print("TOOL AGENT")
    print("=" * 60)

    print(
        "\nExecuting tool for request..."
    )

    result = tool_agent.execute_tool(
        "calculator",
        user_request
    )

    return {
        "tool_result": result
    }


# ============================================================
# TOOL RESULT NODE
# ============================================================

def tool_result_node(state: AgentState):

    print("\n")
    print("=" * 60)
    print("TOOL RESULT")
    print("=" * 60)

    result = state["tool_result"]

    print("\nResult:")
    print(result)

    return {
        "final_response": result
    }


# ============================================================
# RESEARCH NODE
# ============================================================

def research_node(state: AgentState):

    user_request = state["user_request"]
    memory_context = state["memory_context"]

    print("\n")
    print("=" * 60)
    print("RESEARCH AGENT")
    print("=" * 60)

    print(
        "\nSending request to Research Agent..."
    )

    research_request = user_request

    if memory_context:

        research_request += (
            "\n\nRelevant previous memory:\n"
            + memory_context
        )

    research = research_agent.research(
        research_request
    )

    print("\nResearch completed.")

    return {
        "research": research
    }


# ============================================================
# ANALYSIS NODE
# ============================================================

def analysis_node(state: AgentState):

    research = state["research"]

    print("\n")
    print("=" * 60)
    print("ANALYSIS AGENT")
    print("=" * 60)

    print(
        "\nSending research to Analysis Agent..."
    )

    analysis = analysis_agent.analyze(
        research
    )

    print("\nAnalysis completed.")

    return {
        "analysis": analysis
    }


# ============================================================
# WRITING NODE
# ============================================================

def writing_node(state: AgentState):

    research = state["research"]
    analysis = state["analysis"]

    print("\n")
    print("=" * 60)
    print("WRITING AGENT")
    print("=" * 60)

    print(
        "\nGenerating response..."
    )

    writing = writing_agent.write(
        research,
        analysis
    )

    print("\nWriting completed.")

    return {
        "writing": writing
    }


# ============================================================
# VALIDATOR NODE
# ============================================================

def validator_node(state: AgentState):

    user_request = state["user_request"]
    writing = state["writing"]

    print("\n")
    print("=" * 60)
    print("VALIDATOR AGENT")
    print("=" * 60)

    validation = validator_agent.validate(
        user_request,
        writing
    )

    return {
        "validation": validation
    }


# ============================================================
# VALIDATION ROUTER
# ============================================================

def route_after_validation(state: AgentState):

    validation = state["validation"]
    retry_count = state["retry_count"]

    print("\n")
    print("=" * 60)
    print("VALIDATION ROUTING")
    print("=" * 60)

    if validation.startswith("PASS"):

        print(
            "\nValidation status: PASS"
        )

        return "final"

    if retry_count < MAX_RETRIES:

        print(
            "\nValidation status: FAIL"
        )

        print(
            f"Retrying... "
            f"Attempt {retry_count + 1}"
        )

        return "retry"

    print(
        "\nMaximum retry limit reached."
    )

    return "failure"


# ============================================================
# RETRY NODE
# ============================================================

def retry_node(state: AgentState):

    retry_count = state["retry_count"]

    retry_count += 1

    print("\n")
    print("=" * 60)
    print("RETRY NODE")
    print("=" * 60)

    print(
        f"\nRetry attempt: "
        f"{retry_count}"
    )

    return {
        "retry_count": retry_count
    }


# ============================================================
# FINAL RESPONSE NODE
# ============================================================

def final_response_node(state: AgentState):

    writing = state["writing"]

    print("\n")
    print("=" * 60)
    print("FINAL RESPONSE")
    print("=" * 60)

    return {
        "final_response": writing
    }


# ============================================================
# SAVE MEMORY NODE
# ============================================================

def save_memory_node(state: AgentState):

    user_request = state["user_request"]
    final_response = state["final_response"]

    print("\n")
    print("=" * 60)
    print("MEMORY SAVE")
    print("=" * 60)

    # --------------------------------------------------------
    # Store a compact interaction summary.
    # --------------------------------------------------------

    memory_text = (
        f"User request: {user_request}\n"
        f"Assistant response: {final_response[:1000]}"
    )

    saved = memory_agent.remember(
        memory_text,
        category="interaction"
    )

    if saved:

        print(
            "\nInteraction saved to SQLite memory."
        )

    return {
        "memory_saved": saved
    }


# ============================================================
# VALIDATION FAILURE NODE
# ============================================================

def validation_failure_node(state: AgentState):

    validation = state["validation"]

    final_response = (
        "The generated response could not pass "
        "validation after the maximum number "
        "of retry attempts.\n\n"
        "Validation details:\n"
        + validation
    )

    return {
        "final_response": final_response
    }


# ============================================================
# DIRECT NODE
# ============================================================

def direct_node(state: AgentState):

    user_request = state["user_request"]
    memory_context = state["memory_context"]

    print("\n")
    print("=" * 60)
    print("DIRECT RESPONSE")
    print("=" * 60)

    if memory_context and (
        "No relevant previous memories"
        not in memory_context
    ):

        response = (
            f"Request:\n{user_request}\n\n"
            f"Relevant previous memory:\n"
            f"{memory_context}"
        )

    else:

        response = (
            "Request received:\n"
            + user_request
        )

    return {
        "final_response": response
    }


# ============================================================
# ROUTER AFTER SUPERVISOR
# ============================================================

def route_after_supervisor(state: AgentState):

    route = state["route"]

    if route == "tool":

        return "tool"

    if route == "research":

        return "research"

    return "direct"


# ============================================================
# BUILD WORKFLOW
# ============================================================

def build_workflow():

    workflow = StateGraph(
        AgentState
    )

    # --------------------------------------------------------
    # ADD NODES
    # --------------------------------------------------------

    workflow.add_node(
        "supervisor",
        supervisor_node
    )

    workflow.add_node(
        "memory_recall",
        memory_recall_node
    )

    workflow.add_node(
        "tool",
        tool_node
    )

    workflow.add_node(
        "tool_result",
        tool_result_node
    )

    workflow.add_node(
        "research",
        research_node
    )

    workflow.add_node(
        "analysis",
        analysis_node
    )

    workflow.add_node(
        "writing",
        writing_node
    )

    workflow.add_node(
        "validator",
        validator_node
    )

    workflow.add_node(
        "retry",
        retry_node
    )

    workflow.add_node(
        "final",
        final_response_node
    )

    workflow.add_node(
        "save_memory",
        save_memory_node
    )

    workflow.add_node(
        "validation_failure",
        validation_failure_node
    )

    workflow.add_node(
        "direct",
        direct_node
    )

    # --------------------------------------------------------
    # START
    # --------------------------------------------------------

    workflow.add_edge(
        START,
        "supervisor"
    )

    # --------------------------------------------------------
    # SUPERVISOR → MEMORY
    # --------------------------------------------------------

    workflow.add_edge(
        "supervisor",
        "memory_recall"
    )

    # --------------------------------------------------------
    # MEMORY → ROUTE
    # --------------------------------------------------------

    workflow.add_conditional_edges(
        "memory_recall",
        route_after_supervisor,
        {
            "tool": "tool",
            "research": "research",
            "direct": "direct"
        }
    )

    # --------------------------------------------------------
    # TOOL
    # --------------------------------------------------------

    workflow.add_edge(
        "tool",
        "tool_result"
    )

    workflow.add_edge(
        "tool_result",
        "save_memory"
    )

    # --------------------------------------------------------
    # RESEARCH PIPELINE
    # --------------------------------------------------------

    workflow.add_edge(
        "research",
        "analysis"
    )

    workflow.add_edge(
        "analysis",
        "writing"
    )

    workflow.add_edge(
        "writing",
        "validator"
    )

    # --------------------------------------------------------
    # VALIDATOR ROUTING
    # --------------------------------------------------------

    workflow.add_conditional_edges(
        "validator",
        route_after_validation,
        {
            "final": "final",
            "retry": "retry",
            "failure": "validation_failure"
        }
    )

    # --------------------------------------------------------
    # RETRY
    # --------------------------------------------------------

    workflow.add_edge(
        "retry",
        "writing"
    )

    # --------------------------------------------------------
    # FINAL
    # --------------------------------------------------------

    workflow.add_edge(
        "final",
        "save_memory"
    )

    # --------------------------------------------------------
    # VALIDATION FAILURE
    # --------------------------------------------------------

    workflow.add_edge(
        "validation_failure",
        "save_memory"
    )

    # --------------------------------------------------------
    # DIRECT
    # --------------------------------------------------------

    workflow.add_edge(
        "direct",
        "save_memory"
    )

    # --------------------------------------------------------
    # SAVE MEMORY → END
    # --------------------------------------------------------

    workflow.add_edge(
        "save_memory",
        END
    )

    return workflow.compile()


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n")
    print("=" * 60)
    print("MULTI-AGENT PERSONAL ASSISTANT SWARM")
    print("DYNAMIC MULTI-AGENT WORKFLOW")
    print("=" * 60)

    user_request = input(
        "\nEnter your request:\n> "
    ).strip()

    if not user_request:

        print(
            "\nPlease enter a valid request."
        )

        return

    workflow = build_workflow()

    initial_state: AgentState = {

        "user_request": user_request,

        "route": "",

        "memory_context": "",

        "research": "",

        "analysis": "",

        "writing": "",

        "validation": "",

        "tool_result": "",

        "final_response": "",

        "memory_saved": False,

        "retry_count": 0
    }

    try:

        result = workflow.invoke(
            initial_state
        )

        print("\n")
        print("=" * 60)
        print("FINAL RESULT")
        print("=" * 60)

        print(
            "\n"
            + result["final_response"]
        )

        print("\n")
        print("=" * 60)
        print("MEMORY STATUS")
        print("=" * 60)

        print(
            "\nMemory saved:",
            result.get(
                "memory_saved",
                False
            )
        )

        print(
            "Total memories:",
            memory_agent.memory_count()
        )

        print("\n")
        print("=" * 60)
        print("MULTI-AGENT WORKFLOW COMPLETED")
        print("=" * 60)

    finally:

        memory_agent.close()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()