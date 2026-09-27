from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from agents.supervisor_agent import SupervisorAgent
from agents.memory_agent import MemoryAgent
from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.writing_agent import WritingAgent
from agents.validator_agent import ValidatorAgent
from agents.tool_agent import ToolAgent


# ================================================================
# STATE
# ================================================================

class AgentState(TypedDict):
    """
    Shared state passed between all agents.
    """

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


# ================================================================
# CONSTANTS
# ================================================================

MAX_RETRIES = 2


# ================================================================
# AGENTS
# ================================================================

supervisor_agent = SupervisorAgent()

memory_agent = MemoryAgent()

research_agent = ResearchAgent()

analysis_agent = AnalysisAgent()

writing_agent = WritingAgent()

validator_agent = ValidatorAgent()

tool_agent = ToolAgent()


# ================================================================
# INITIAL STATE
# ================================================================

def create_initial_state(
    user_request: str
) -> AgentState:
    """
    Create the initial workflow state.
    """

    return {
        "user_request": str(
            user_request
        ),

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
    }


# ================================================================
# SUPERVISOR NODE
# ================================================================

def supervisor_node(
    state: AgentState
):
    """
    Decide which route should handle the request.
    """

    user_request = state[
        "user_request"
    ]

    route = supervisor_agent.route(
        user_request
    )

    return {
        "route": route
    }


# ================================================================
# ROUTER
# ================================================================

def route_after_supervisor(
    state: AgentState
):
    """
    Select the next workflow path.
    """

    route = state.get(
        "route",
        "direct"
    )

    if route == "research":
        return "memory"

    if route == "tool":
        return "tool"

    return "direct"


# ================================================================
# MEMORY NODE
# ================================================================

def memory_node(
    state: AgentState
):
    """
    Recall relevant previous memories.

    Memory is supplied to research only when it is relevant.
    """

    user_request = state[
        "user_request"
    ]

    try:

        print(
            "\nSearching memory..."
        )

        memories = memory_agent.recall_memory(
            user_request,
            5
        )

    except Exception:

        memories = []

    if memories:

        memory_context = (
            "\n\n".join(
                str(memory)
                for memory in memories
            )
        )

    else:

        memory_context = ""

    return {
        "memory_context": memory_context
    }


# ================================================================
# RESEARCH NODE
# ================================================================

def research_node(
    state: AgentState
):
    """
    Execute the Research Agent.
    """

    user_request = state[
        "user_request"
    ]

    memory_context = state.get(
        "memory_context",
        ""
    )

    research = research_agent.research(
        user_request,
        memory_context
    )

    return {
        "research": research
    }


# ================================================================
# ANALYSIS NODE
# ================================================================

def analysis_node(
    state: AgentState
):
    """
    Execute the Analysis Agent.
    """

    research = state.get(
        "research",
        ""
    )

    user_request = state[
        "user_request"
    ]

    analysis = analysis_agent.analyze(
        research,
        user_request
    )

    return {
        "analysis": analysis
    }


# ================================================================
# WRITING NODE
# ================================================================

def writing_node(
    state: AgentState
):
    """
    Execute the Writing Agent.
    """

    research = state.get(
        "research",
        ""
    )

    analysis = state.get(
        "analysis",
        ""
    )

    user_request = state[
        "user_request"
    ]

    writing = writing_agent.write(
        research,
        analysis,
        "structured response",
        user_request
    )

    return {
        "writing": writing
    }


# ================================================================
# VALIDATION NODE
# ================================================================

def validation_node(
    state: AgentState
):
    """
    Validate the generated response.
    """

    user_request = state[
        "user_request"
    ]

    writing = state.get(
        "writing",
        ""
    )

    validation = validator_agent.validate(
        user_request,
        writing
    )

    return {
        "validation": validation
    }


# ================================================================
# VALIDATION ROUTER
# ================================================================

def route_after_validation(
    state: AgentState
):
    """
    Decide whether to retry writing or finish.
    """

    validation = state.get(
        "validation",
        ""
    ).upper()

    retry_count = state.get(
        "retry_count",
        0
    )

    if "PASS" in validation:

        return "final"

    if retry_count < MAX_RETRIES:

        return "retry"

    return "validation_failure"


# ================================================================
# RETRY NODE
# ================================================================

def retry_node(
    state: AgentState
):
    """
    Increment the retry counter before regenerating
    the written response.
    """

    retry_count = state.get(
        "retry_count",
        0
    )

    return {
        "retry_count": retry_count + 1
    }


# ================================================================
# VALIDATION FAILURE NODE
# ================================================================

def validation_failure_node(
    state: AgentState
):
    """
    Create a safe final response when validation
    fails after the maximum retry count.
    """

    writing = state.get(
        "writing",
        ""
    )

    validation = state.get(
        "validation",
        ""
    )

    if writing:

        final_response = writing

    else:

        final_response = (
            "The system could not generate a validated "
            "response for the requested task.\n\n"
            f"Validation result:\n{validation}"
        )

    return {
        "final_response": final_response
    }


# ================================================================
# FINAL RESPONSE NODE
# ================================================================

def final_response_node(
    state: AgentState
):
    """
    Move the validated writing into final_response.
    """

    writing = state.get(
        "writing",
        ""
    )

    return {
        "final_response": writing
    }


# ================================================================
# TOOL ARGUMENT EXTRACTION
# ================================================================

def extract_calculator_expression(
    user_request: str
):
    """
    Extract a mathematical expression from a calculator request.

    Example:

        calculate 25 * 40 + 100

    becomes:

        25 * 40 + 100
    """

    request = str(
        user_request
    ).strip()

    lower_request = request.lower()

    prefixes = [
        "calculate",
        "calculator",
        "compute",
        "what is",
        "solve",
    ]

    expression = request

    for prefix in prefixes:

        if lower_request.startswith(
            prefix
        ):

            expression = request[
                len(prefix):
            ].strip()

            break

    # Remove common punctuation.
    expression = expression.strip(
        " :?="
    )

    return expression


# ================================================================
# TOOL NODE
# ================================================================

def tool_node(
    state: AgentState
):
    """
    Execute the appropriate tool.
    """

    user_request = state[
        "user_request"
    ]

    route = state.get(
        "route",
        ""
    )

    request_lower = user_request.lower()

    # ------------------------------------------------------------
    # Calculator
    # ------------------------------------------------------------

    calculator_keywords = [
        "calculate",
        "calculator",
        "compute",
        "percentage",
        "percent",
        "sum",
        "multiply",
        "divide",
        "solve",
    ]

    is_calculation = (
        route == "tool"
        and any(
            keyword in request_lower
            for keyword in calculator_keywords
        )
    )

    if is_calculation:

        expression = extract_calculator_expression(
            user_request
        )

        result = tool_agent.execute_tool(
            "calculator",
            expression
        )

    # ------------------------------------------------------------
    # Date / Time
    # ------------------------------------------------------------

    elif (
        "time" in request_lower
        or "date" in request_lower
    ):

        result = tool_agent.execute_tool(
            "datetime",
            user_request
        )

    # ------------------------------------------------------------
    # Fallback
    # ------------------------------------------------------------

    else:

        result = tool_agent.execute_tool(
            "text_analysis",
            user_request
        )

    return {
        "tool_result": str(
            result
        ),

        "final_response": str(
            result
        ),
    }


# ================================================================
# DIRECT NODE
# ================================================================

def direct_node(
    state: AgentState
):
    """
    Handle simple requests directly.
    """

    user_request = state[
        "user_request"
    ].strip()

    request_lower = user_request.lower()

    # ------------------------------------------------------------
    # Greetings
    # ------------------------------------------------------------

    if request_lower in {
        "hello",
        "hi",
        "hey",
        "hello!",
        "hi!",
        "hey!",
        "hello, how are you?",
    }:

        response = (
            "Hello! I'm your Multi-Agent Personal Assistant. "
            "How can I help you today?"
        )

    # ------------------------------------------------------------
    # Generic response
    # ------------------------------------------------------------

    else:

        response = (
            "I understand your request:\n\n"
            f"{user_request}\n\n"
            "This request does not require the research or "
            "tool workflow, so it was handled directly."
        )

    return {
        "final_response": response
    }


# ================================================================
# MEMORY SAVE NODE
# ================================================================

def memory_save_node(
    state: AgentState
):
    """
    Save the completed interaction into memory.
    """

    user_request = state[
        "user_request"
    ]

    final_response = state.get(
        "final_response",
        ""
    )

    if not final_response:

        final_response = state.get(
            "writing",
            ""
        )

    try:

        print(
            "\nSaving memory..."
        )

        memory_content = (
            f"User request: {user_request}\n"
            f"Assistant response: {final_response}"
        )

        result = memory_agent.save_memory(
            memory_content,
            "conversation"
        )

        print(
            "Memory saved successfully."
        )

        return {
            "memory_saved": bool(
                result
                if result is not None
                else True
            )
        }

    except Exception:

        return {
            "memory_saved": False
        }


# ================================================================
# BUILD WORKFLOW
# ================================================================

def build_workflow():
    """
    Build and compile the LangGraph workflow.
    """

    graph = StateGraph(
        AgentState
    )

    # ------------------------------------------------------------
    # Nodes
    # ------------------------------------------------------------

    graph.add_node(
        "supervisor",
        supervisor_node
    )

    graph.add_node(
        "memory",
        memory_node
    )

    graph.add_node(
        "research",
        research_node
    )

    graph.add_node(
        "analysis",
        analysis_node
    )

    graph.add_node(
        "writing",
        writing_node
    )

    graph.add_node(
        "validator",
        validation_node
    )

    graph.add_node(
        "retry",
        retry_node
    )

    graph.add_node(
        "validation_failure",
        validation_failure_node
    )

    graph.add_node(
        "final",
        final_response_node
    )

    graph.add_node(
        "tool",
        tool_node
    )

    graph.add_node(
        "direct",
        direct_node
    )

    graph.add_node(
        "memory_save",
        memory_save_node
    )

    # ------------------------------------------------------------
    # START
    # ------------------------------------------------------------

    graph.add_edge(
        START,
        "supervisor"
    )

    # ------------------------------------------------------------
    # Supervisor routing
    # ------------------------------------------------------------

    graph.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {
            "memory": "memory",
            "tool": "tool",
            "direct": "direct",
        }
    )

    # ------------------------------------------------------------
    # Research workflow
    # ------------------------------------------------------------

    graph.add_edge(
        "memory",
        "research"
    )

    graph.add_edge(
        "research",
        "analysis"
    )

    graph.add_edge(
        "analysis",
        "writing"
    )

    graph.add_edge(
        "writing",
        "validator"
    )

    # ------------------------------------------------------------
    # Validation routing
    # ------------------------------------------------------------

    graph.add_conditional_edges(
        "validator",
        route_after_validation,
        {
            "final": "final",
            "retry": "retry",
            "validation_failure": "validation_failure",
        }
    )

    # ------------------------------------------------------------
    # Retry
    # ------------------------------------------------------------

    graph.add_edge(
        "retry",
        "writing"
    )

    # ------------------------------------------------------------
    # Valid final response
    # ------------------------------------------------------------

    graph.add_edge(
        "final",
        "memory_save"
    )

    # ------------------------------------------------------------
    # Validation failure
    # ------------------------------------------------------------

    graph.add_edge(
        "validation_failure",
        "memory_save"
    )

    # ------------------------------------------------------------
    # Tool workflow
    # ------------------------------------------------------------

    graph.add_edge(
        "tool",
        "memory_save"
    )

    # ------------------------------------------------------------
    # Direct workflow
    # ------------------------------------------------------------

    graph.add_edge(
        "direct",
        "memory_save"
    )

    # ------------------------------------------------------------
    # End
    # ------------------------------------------------------------

    graph.add_edge(
        "memory_save",
        END
    )

    return graph.compile()


# ================================================================
# CREATE DEFAULT WORKFLOW
# ================================================================

workflow = build_workflow()


# ================================================================
# DIRECT TEST
# ================================================================

if __name__ == "__main__":

    print("=" * 70)
    print("MULTI-AGENT PERSONAL ASSISTANT WORKFLOW TEST")
    print("=" * 70)

    # ------------------------------------------------------------
    # Research test
    # ------------------------------------------------------------

    print("\n1. RESEARCH REQUEST")

    research_state = create_initial_state(
        "research artificial intelligence in healthcare"
    )

    research_result = workflow.invoke(
        research_state
    )

    print(
        "\nRoute:",
        research_result["route"]
    )

    print(
        "\nValidation:",
        research_result["validation"]
    )

    print(
        "\nFinal Response:\n",
        research_result["final_response"]
    )

    # ------------------------------------------------------------
    # Tool test
    # ------------------------------------------------------------

    print("\n2. TOOL REQUEST")

    tool_state = create_initial_state(
        "calculate 25 * 40 + 100"
    )

    tool_result = workflow.invoke(
        tool_state
    )

    print(
        "\nRoute:",
        tool_result["route"]
    )

    print(
        "\nTool Result:",
        tool_result["tool_result"]
    )

    print(
        "\nFinal Response:",
        tool_result["final_response"]
    )

    # ------------------------------------------------------------
    # Direct test
    # ------------------------------------------------------------

    print("\n3. DIRECT REQUEST")

    direct_state = create_initial_state(
        "hello, how are you?"
    )

    direct_result = workflow.invoke(
        direct_state
    )

    print(
        "\nRoute:",
        direct_result["route"]
    )

    print(
        "\nFinal Response:",
        direct_result["final_response"]
    )

    print("\n" + "=" * 70)
    print("WORKFLOW TEST COMPLETED")
    print("=" * 70)