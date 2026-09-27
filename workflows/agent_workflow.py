import sys
import os
from datetime import datetime
from typing import TypedDict, List, Dict, Any

from langgraph.graph import StateGraph, START, END


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

    # New field:
    # Stores the complete agent execution history.
    activity_log: List[Dict[str, Any]]


# ============================================================
# ACTIVITY LOG HELPER
# ============================================================

def add_activity(
    state: AgentState,
    agent: str,
    status: str,
    action: str
):
    """
    Add an event to the agent activity log.

    Example:

    {
        "agent": "Research Agent",
        "status": "COMPLETED",
        "action": "Research completed",
        "timestamp": "2026-09-25 21:30:00"
    }
    """

    current_log = list(
        state.get(
            "activity_log",
            []
        )
    )

    current_log.append(
        {
            "agent": agent,
            "status": status,
            "action": action,
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }
    )

    return current_log


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

    activity_log = add_activity(
        state,
        "Supervisor Agent",
        "RUNNING",
        "Analyzing user request and selecting route"
    )

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


    activity_log = add_activity(
        {
            **state,
            "activity_log": activity_log
        },
        "Supervisor Agent",
        "COMPLETED",
        f"Selected {route.upper()} route"
    )


    return {
        "route": route,
        "activity_log": activity_log
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


    activity_log = add_activity(
        state,
        "Memory Agent",
        "RUNNING",
        "Searching previous interactions"
    )


    results = memory_agent.recall(
        user_request,
        number_of_results=5
    )


    if not results:

        memory_context = (
            "No relevant previous memories were found."
        )

        print(
            "\nNo relevant memories found."
        )

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


    activity_log = add_activity(
        {
            **state,
            "activity_log": activity_log
        },
        "Memory Agent",
        "COMPLETED",
        "Memory search completed"
    )


    return {
        "memory_context": memory_context,
        "activity_log": activity_log
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


    activity_log = add_activity(
        state,
        "Tool Agent",
        "RUNNING",
        "Executing requested tool"
    )


    result = tool_agent.execute_tool(
        "calculator",
        user_request
    )


    activity_log = add_activity(
        {
            **state,
            "activity_log": activity_log
        },
        "Tool Agent",
        "COMPLETED",
        "Tool execution completed"
    )


    return {
        "tool_result": result,
        "activity_log": activity_log
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


    activity_log = add_activity(
        state,
        "Tool Result",
        "COMPLETED",
        "Tool result prepared for final response"
    )


    return {
        "final_response": result,
        "activity_log": activity_log
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


    activity_log = add_activity(
        state,
        "Research Agent",
        "RUNNING",
        "Researching requested topic"
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


    activity_log = add_activity(
        {
            **state,
            "activity_log": activity_log
        },
        "Research Agent",
        "COMPLETED",
        "Research completed successfully"
    )


    return {
        "research": str(research),
        "activity_log": activity_log
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


    activity_log = add_activity(
        state,
        "Analysis Agent",
        "RUNNING",
        "Analyzing research findings"
    )


    analysis = analysis_agent.analyze(
        research
    )


    print("\nAnalysis completed.")


    activity_log = add_activity(
        {
            **state,
            "activity_log": activity_log
        },
        "Analysis Agent",
        "COMPLETED",
        "Research analysis completed"
    )


    return {
        "analysis": str(analysis),
        "activity_log": activity_log
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


    activity_log = add_activity(
        state,
        "Writing Agent",
        "RUNNING",
        "Generating final response"
    )


    writing = writing_agent.write(
        research,
        analysis
    )


    print("\nWriting completed.")


    activity_log = add_activity(
        {
            **state,
            "activity_log": activity_log
        },
        "Writing Agent",
        "COMPLETED",
        "Final response generated"
    )


    return {
        "writing": str(writing),
        "final_response": str(writing),
        "activity_log": activity_log
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


    activity_log = add_activity(
        state,
        "Validator Agent",
        "RUNNING",
        "Validating generated response"
    )


    validation = validator_agent.validate(
        user_request,
        writing
    )


    activity_log = add_activity(
        {
            **state,
            "activity_log": activity_log
        },
        "Validator Agent",
        "COMPLETED",
        (
            "Validation passed"
            if validation.startswith("PASS")
            else "Validation requires review"
        )
    )


    return {
        "validation": validation,
        "activity_log": activity_log
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


    activity_log = add_activity(
        state,
        "Workflow Controller",
        "RETRY",
        f"Retrying response generation - attempt {retry_count}"
    )


    return {
        "retry_count": retry_count,
        "activity_log": activity_log
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


    activity_log = add_activity(
        state,
        "Workflow Controller",
        "COMPLETED",
        "Final response approved after validation"
    )


    return {
        "final_response": writing,
        "activity_log": activity_log
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


    activity_log = add_activity(
        state,
        "Memory Agent",
        "RUNNING",
        "Saving completed interaction"
    )


    # --------------------------------------------------------
    # Store compact interaction summary.
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

    else:

        print(
            "\nInteraction processed by SQLite memory."
        )


    activity_log = add_activity(
        {
            **state,
            "activity_log": activity_log
        },
        "Memory Agent",
        "COMPLETED",
        "Interaction saved to SQLite memory"
    )


    return {
        "memory_saved": saved,
        "activity_log": activity_log
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


    activity_log = add_activity(
        state,
        "Validator Agent",
        "FAILED",
        "Maximum validation retries reached"
    )


    return {
        "final_response": final_response,
        "activity_log": activity_log
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


    activity_log = add_activity(
        state,
        "Direct Response",
        "RUNNING",
        "Preparing direct response"
    )


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


    activity_log = add_activity(
        {
            **state,
            "activity_log": activity_log
        },
        "Direct Response",
        "COMPLETED",
        "Direct response prepared"
    )


    return {
        "final_response": response,
        "activity_log": activity_log
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

        "retry_count": 0,

        "activity_log": []
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
        print("AGENT ACTIVITY LOG")
        print("=" * 60)


        for index, event in enumerate(
            result.get(
                "activity_log",
                []
            ),
            start=1
        ):

            print(
                f"\n{index}. "
                f"{event['agent']} "
                f"| {event['status']}"
            )

            print(
                f"   Action: "
                f"{event['action']}"
            )

            print(
                f"   Time: "
                f"{event['timestamp']}"
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