
import sys
import time
from pathlib import Path

import streamlit as st


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from workflows.agent_workflow import build_workflow
from evaluation.single_agent_baseline import SingleAgentBaseline


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Multi-Agent Personal Assistant Swarm",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# TEST TASKS
# ============================================================

TEST_TASKS = [
    "Hello",
    "Calculate 25 * 40",
    "What is Artificial Intelligence? Explain its benefits, risks, and practical applications.",
    "Explain machine learning and its major applications.",
    "What are the benefits and limitations of cloud computing?"
]


# ============================================================
# SESSION STATE
# ============================================================

if "evaluation_results" not in st.session_state:
    st.session_state.evaluation_results = None

if "comparison_results" not in st.session_state:
    st.session_state.comparison_results = None


# ============================================================
# MULTI-AGENT EVALUATION
# ============================================================

def run_multi_agent_evaluation():

    workflow = build_workflow()

    results = []

    for task in TEST_TASKS:

        start_time = time.perf_counter()

        initial_state = {
            "user_request": task,
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

            result = workflow.invoke(initial_state)

            execution_time = time.perf_counter() - start_time

            final_response = str(
                result.get("final_response", "")
            )

            route = str(
                result.get("route", "")
            )

            validation = str(
                result.get("validation", "")
            )

            completed = bool(
                final_response.strip()
            )

            validation_applicable = route == "research"

            validation_passed = None

            if validation_applicable:
                validation_passed = (
                    "PASS" in validation.upper()
                )

            tool_success = None

            if route == "tool":

                tool_result = str(
                    result.get("tool_result", "")
                )

                tool_success = (
                    bool(tool_result.strip())
                    and "unknown tool" not in tool_result.lower()
                    and "error" not in tool_result.lower()
                )

            results.append({
                "task": task,
                "completed": completed,
                "execution_time": execution_time,
                "response_length": len(final_response),
                "route": route,
                "memory_saved": bool(
                    result.get("memory_saved", False)
                ),
                "validation_passed": validation_passed,
                "tool_success": tool_success,
                "retries": int(
                    result.get("retry_count", 0)
                )
            })

        except Exception as error:

            execution_time = time.perf_counter() - start_time

            results.append({
                "task": task,
                "completed": False,
                "execution_time": execution_time,
                "response_length": 0,
                "route": "error",
                "memory_saved": False,
                "validation_passed": None,
                "tool_success": None,
                "retries": 0,
                "error": str(error)
            })

    return results


# ============================================================
# SINGLE-AGENT EVALUATION
# ============================================================

def run_single_agent_evaluation():

    agent = SingleAgentBaseline()

    results = []

    for task in TEST_TASKS:

        start_time = time.perf_counter()

        try:

            result = agent.process(task)

            execution_time = time.perf_counter() - start_time

            response = str(
                result.get("response", "")
            )

            completed = (
                result.get("status") == "completed"
                and bool(response.strip())
            )

            results.append({
                "task": task,
                "completed": completed,
                "execution_time": execution_time,
                "response_length": len(response),
                "memory_saved": False,
                "validation_passed": None,
                "tool_success": None,
                "retries": 0
            })

        except Exception as error:

            execution_time = time.perf_counter() - start_time

            results.append({
                "task": task,
                "completed": False,
                "execution_time": execution_time,
                "response_length": 0,
                "memory_saved": False,
                "validation_passed": None,
                "tool_success": None,
                "retries": 0,
                "error": str(error)
            })

    return results


# ============================================================
# METRIC CALCULATOR
# ============================================================

def calculate_metrics(results):

    total = len(results)

    completed = sum(
        1 for item in results
        if item["completed"]
    )

    completion_rate = (
        completed / total * 100
        if total
        else 0
    )

    average_time = (
        sum(
            item["execution_time"]
            for item in results
        ) / total
        if total
        else 0
    )

    average_response_length = (
        sum(
            item["response_length"]
            for item in results
        ) / total
        if total
        else 0
    )

    memory_tasks = [
        item for item in results
        if "memory_saved" in item
    ]

    memory_saved = sum(
        1 for item in memory_tasks
        if item["memory_saved"]
    )

    memory_rate = (
        memory_saved / len(memory_tasks) * 100
        if memory_tasks
        else 0
    )

    validation_tasks = [
        item for item in results
        if item["validation_passed"] is not None
    ]

    validation_passed = sum(
        1 for item in validation_tasks
        if item["validation_passed"]
    )

    validation_rate = (
        validation_passed / len(validation_tasks) * 100
        if validation_tasks
        else None
    )

    tool_tasks = [
        item for item in results
        if item["tool_success"] is not None
    ]

    tool_success = sum(
        1 for item in tool_tasks
        if item["tool_success"]
    )

    tool_rate = (
        tool_success / len(tool_tasks) * 100
        if tool_tasks
        else None
    )

    total_retries = sum(
        item["retries"]
        for item in results
    )

    return {
        "total": total,
        "completed": completed,
        "completion_rate": completion_rate,
        "average_time": average_time,
        "average_response_length": average_response_length,
        "memory_rate": memory_rate,
        "validation_rate": validation_rate,
        "tool_rate": tool_rate,
        "retries": total_retries
    }


# ============================================================
# HEADER
# ============================================================

st.title("🤖 Multi-Agent Personal Assistant Swarm")

st.subheader("📊 Evaluation & Architecture Comparison Dashboard")

st.write(
    "This dashboard evaluates the Multi-Agent Personal Assistant "
    "Swarm and compares it with a Single-Agent baseline using "
    "the same five test tasks."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Evaluation Controls")

st.sidebar.write("Test Tasks: 5")
st.sidebar.write("Architecture: Multi-Agent + Single-Agent")

run_button = st.sidebar.button(
    "🚀 Run Complete Evaluation",
    use_container_width=True
)


# ============================================================
# RUN EVALUATION
# ============================================================

if run_button:

    with st.spinner(
        "Running Single-Agent and Multi-Agent evaluations..."
    ):

        single_results = run_single_agent_evaluation()

        multi_results = run_multi_agent_evaluation()

        single_metrics = calculate_metrics(
            single_results
        )

        multi_metrics = calculate_metrics(
            multi_results
        )

        st.session_state.evaluation_results = {
            "single": single_results,
            "multi": multi_results,
            "single_metrics": single_metrics,
            "multi_metrics": multi_metrics
        }


# ============================================================
# RESULTS
# ============================================================

if st.session_state.evaluation_results is not None:

    data = st.session_state.evaluation_results

    single = data["single_metrics"]
    multi = data["multi_metrics"]

    # --------------------------------------------------------
    # SYSTEM PERFORMANCE
    # --------------------------------------------------------

    st.header("📊 System Performance")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Task Completion",
            f"{multi['completion_rate']:.1f}%"
        )

    with col2:
        validation_value = (
            "N/A"
            if multi["validation_rate"] is None
            else f"{multi['validation_rate']:.1f}%"
        )

        st.metric(
            "Research Validation",
            validation_value
        )

    with col3:
        tool_value = (
            "N/A"
            if multi["tool_rate"] is None
            else f"{multi['tool_rate']:.1f}%"
        )

        st.metric(
            "Tool Success",
            tool_value
        )

    with col4:
        st.metric(
            "Memory Save",
            f"{multi['memory_rate']:.1f}%"
        )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Tasks",
            multi["total"]
        )

    with col2:
        st.metric(
            "Completed Tasks",
            multi["completed"]
        )

    with col3:
        st.metric(
            "Total Retries",
            multi["retries"]
        )

    with col4:
        research_count = sum(
            1 for item in data["multi"]
            if item["route"] == "research"
        )

        st.metric(
            "Research Tasks",
            research_count
        )

    # --------------------------------------------------------
    # ARCHITECTURE COMPARISON
    # --------------------------------------------------------

    st.header("⚖️ Single-Agent vs Multi-Agent")

    st.write(
        "Both architectures were evaluated using the same five "
        "test tasks."
    )

    st.markdown("### 📋 Performance Comparison")

    comparison_table = {
        "Metric": [
            "Task Completion",
            "Average Execution Time",
            "Average Response Length",
            "Memory Save",
            "Validation",
            "Tool Success",
            "Total Retries"
        ],
        "Single-Agent": [
            f"{single['completion_rate']:.1f}%",
            f"{single['average_time']:.6f} s",
            f"{single['average_response_length']:.1f}",
            f"{single['memory_rate']:.1f}%",
            "N/A",
            "N/A",
            str(single["retries"])
        ],
        "Multi-Agent": [
            f"{multi['completion_rate']:.1f}%",
            f"{multi['average_time']:.6f} s",
            f"{multi['average_response_length']:.1f}",
            f"{multi['memory_rate']:.1f}%",
            (
                "N/A"
                if multi["validation_rate"] is None
                else f"{multi['validation_rate']:.1f}%"
            ),
            (
                "N/A"
                if multi["tool_rate"] is None
                else f"{multi['tool_rate']:.1f}%"
            ),
            str(multi["retries"])
        ]
    }

    st.table(comparison_table)

    # --------------------------------------------------------
    # EXECUTION TIME
    # --------------------------------------------------------

    st.subheader("⏱️ Average Execution Time")

    time_col1, time_col2 = st.columns(2)

    with time_col1:
        st.metric(
            "Single-Agent",
            f"{single['average_time']:.6f} s"
        )

    with time_col2:
        st.metric(
            "Multi-Agent",
            f"{multi['average_time']:.6f} s"
        )

    st.info(
        "The Multi-Agent workflow performs additional routing, "
        "specialized processing, validation and memory operations. "
        "Therefore execution time should be interpreted together "
        "with the additional capabilities provided by the architecture."
    )

    # --------------------------------------------------------
    # RESPONSE LENGTH
    # --------------------------------------------------------

    st.subheader("📝 Average Response Length")

    response_col1, response_col2 = st.columns(2)

    with response_col1:
        st.metric(
            "Single-Agent",
            f"{single['average_response_length']:.1f} characters"
        )

    with response_col2:
        st.metric(
            "Multi-Agent",
            f"{multi['average_response_length']:.1f} characters"
        )

    # --------------------------------------------------------
    # MULTI-AGENT ROUTES
    # --------------------------------------------------------

    st.header("🧭 Multi-Agent Route Distribution")

    route_counts = {}

    for item in data["multi"]:

        route = item["route"].upper()

        route_counts[route] = (
            route_counts.get(route, 0) + 1
        )

    for route, count in route_counts.items():

        percentage = (
            count / len(data["multi"]) * 100
            if data["multi"]
            else 0
        )

        st.write(
            f"**{route}** — {count} task(s) — "
            f"{percentage:.1f}%"
        )

        st.progress(
            percentage / 100
        )

    # --------------------------------------------------------
    # SUCCESS METRICS
    # --------------------------------------------------------

    st.header("📈 Multi-Agent Success Metrics")

    metrics = [
        (
            "Task Completion",
            multi["completion_rate"]
        ),
        (
            "Memory Save",
            multi["memory_rate"]
        )
    ]

    if multi["validation_rate"] is not None:
        metrics.append(
            (
                "Research Validation",
                multi["validation_rate"]
            )
        )

    if multi["tool_rate"] is not None:
        metrics.append(
            (
                "Tool Success",
                multi["tool_rate"]
            )
        )

    for name, value in metrics:

        st.write(
            f"**{name}: {value:.1f}%**"
        )

        st.progress(
            value / 100
        )

    # --------------------------------------------------------
    # TEST CASE RESULTS
    # --------------------------------------------------------

    st.header("🧪 Test Case Results")

    for index, (single_result, multi_result) in enumerate(
        zip(
            data["single"],
            data["multi"]
        ),
        start=1
    ):

        with st.expander(
            f"Test Case {index}: {single_result['task']}"
        ):

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("### Single-Agent")

                st.write(
                    f"Completed: "
                    f"{'✅' if single_result['completed'] else '❌'}"
                )

                st.write(
                    f"Execution Time: "
                    f"{single_result['execution_time']:.6f} s"
                )

                st.write(
                    f"Response Length: "
                    f"{single_result['response_length']} characters"
                )

            with col2:

                st.markdown("### Multi-Agent")

                st.write(
                    f"Completed: "
                    f"{'✅' if multi_result['completed'] else '❌'}"
                )

                st.write(
                    f"Route: "
                    f"{multi_result['route'].upper()}"
                )

                st.write(
                    f"Execution Time: "
                    f"{multi_result['execution_time']:.6f} s"
                )

                st.write(
                    f"Response Length: "
                    f"{multi_result['response_length']} characters"
                )

                st.write(
                    f"Memory Saved: "
                    f"{'✅' if multi_result['memory_saved'] else '❌'}"
                )

                if multi_result["validation_passed"] is not None:

                    st.write(
                        f"Validation: "
                        f"{'✅ PASS' if multi_result['validation_passed'] else '❌ FAIL'}"
                    )

                if multi_result["tool_success"] is not None:

                    st.write(
                        f"Tool Success: "
                        f"{'✅' if multi_result['tool_success'] else '❌'}"
                    )

                st.write(
                    f"Retries: "
                    f"{multi_result['retries']}"
                )

    # --------------------------------------------------------
    # ARCHITECTURE CAPABILITIES
    # --------------------------------------------------------

    st.header("🏗️ Architecture Capabilities")

    capability_table = {
        "Capability": [
            "Direct Task Handling",
            "Dynamic Routing",
            "Specialized Agents",
            "Persistent Memory",
            "Tool Execution",
            "Response Validation",
            "Retry Mechanism"
        ],
        "Single-Agent": [
            "✅",
            "❌",
            "❌",
            "❌",
            "Basic",
            "❌",
            "❌"
        ],
        "Multi-Agent": [
            "✅",
            "✅",
            "✅",
            "✅",
            "✅",
            "✅",
            "✅"
        ]
    }

    st.table(capability_table)

    # --------------------------------------------------------
    # EXPERIMENTAL INTERPRETATION
    # --------------------------------------------------------

    st.header("📋 Experimental Interpretation")

    st.write(
        "Both architectures achieved "
        f"{multi['completion_rate']:.1f}% task completion "
        "on the selected five-task test set."
    )

    st.write(
        "The Multi-Agent architecture introduces additional "
        "specialization, dynamic routing, persistent memory, "
        "validation and tool-handling capabilities."
    )

    st.write(
        "The additional workflow stages increase execution "
        "overhead in the current local environment. Therefore, "
        "execution time should not be interpreted independently "
        "from the capabilities performed by each architecture."
    )

    # --------------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------------

    st.header("📌 Evaluation Summary")

    st.markdown(
        f"""
**Total Tasks:** {multi['total']}

**Completed Tasks:** {multi['completed']}

**Task Completion Rate:** {multi['completion_rate']:.1f}%

**Average Multi-Agent Execution Time:** {multi['average_time']:.6f} seconds

**Average Multi-Agent Response Length:** {multi['average_response_length']:.1f} characters

**Memory Save Rate:** {multi['memory_rate']:.1f}%

**Total Retries:** {multi['retries']}
"""
    )

    st.success(
        "Evaluation completed successfully."
    )

else:

    st.info(
        "Click **🚀 Run Complete Evaluation** in the sidebar "
        "to run the five-task Single-Agent vs Multi-Agent experiment."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Multi-Agent Personal Assistant Swarm | "
    "B.Tech AI & Data Science Final Year Project"
)

