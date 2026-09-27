
import sys
import time
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from evaluation.single_agent_baseline import SingleAgentBaseline
from workflows.agent_workflow import build_workflow


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
# SINGLE-AGENT EVALUATION
# ============================================================

def evaluate_single_agent():
    print("\n" + "=" * 70)
    print("SINGLE-AGENT EVALUATION")
    print("=" * 70)

    agent = SingleAgentBaseline()

    results = []

    for index, task in enumerate(TEST_TASKS, start=1):

        print(f"\nTest Case {index}")
        print("-" * 70)
        print(f"Task: {task}")

        start_time = time.perf_counter()

        result = agent.process(task)

        execution_time = time.perf_counter() - start_time

        completed = (
            result.get("status") == "completed"
            and bool(result.get("response", "").strip())
        )

        results.append({
            "task": task,
            "completed": completed,
            "execution_time": execution_time,
            "response_length": len(result.get("response", "")),
            "memory_saved": False,
            "validation_passed": None,
            "tool_success": None,
            "retries": 0
        })

        print(f"Completed: {completed}")
        print(f"Execution Time: {execution_time:.6f} seconds")

    return results


# ============================================================
# MULTI-AGENT EVALUATION
# ============================================================

def evaluate_multi_agent():
    print("\n" + "=" * 70)
    print("MULTI-AGENT EVALUATION")
    print("=" * 70)

    workflow = build_workflow()

    results = []

    for index, task in enumerate(TEST_TASKS, start=1):

        print(f"\nTest Case {index}")
        print("-" * 70)
        print(f"Task: {task}")

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

            task_completed = bool(final_response.strip())

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
                "completed": task_completed,
                "execution_time": execution_time,
                "response_length": len(final_response),
                "memory_saved": bool(
                    result.get("memory_saved", False)
                ),
                "validation_passed": validation_passed,
                "tool_success": tool_success,
                "retries": int(
                    result.get("retry_count", 0)
                ),
                "route": route
            })

            print(f"Completed: {task_completed}")
            print(f"Route: {route}")
            print(f"Execution Time: {execution_time:.6f} seconds")
            print(
                f"Memory Saved: "
                f"{result.get('memory_saved', False)}"
            )
            print(
                f"Retries: "
                f"{result.get('retry_count', 0)}"
            )

        except Exception as error:

            execution_time = time.perf_counter() - start_time

            print(f"ERROR: {error}")

            results.append({
                "task": task,
                "completed": False,
                "execution_time": execution_time,
                "response_length": 0,
                "memory_saved": False,
                "validation_passed": None,
                "tool_success": None,
                "retries": 0,
                "route": "error"
            })

    return results


# ============================================================
# METRIC CALCULATIONS
# ============================================================

def calculate_metrics(results, system_name):

    total_tasks = len(results)

    completed_tasks = sum(
        1 for result in results
        if result["completed"]
    )

    completion_rate = (
        completed_tasks / total_tasks * 100
        if total_tasks
        else 0
    )

    average_execution_time = (
        sum(
            result["execution_time"]
            for result in results
        ) / total_tasks
        if total_tasks
        else 0
    )

    average_response_length = (
        sum(
            result["response_length"]
            for result in results
        ) / total_tasks
        if total_tasks
        else 0
    )

    memory_tasks = [
        result for result in results
        if "memory_saved" in result
    ]

    memory_saved = sum(
        1 for result in memory_tasks
        if result["memory_saved"]
    )

    memory_rate = (
        memory_saved / len(memory_tasks) * 100
        if memory_tasks
        else 0
    )

    validation_tasks = [
        result for result in results
        if result["validation_passed"] is not None
    ]

    validation_passed = sum(
        1 for result in validation_tasks
        if result["validation_passed"]
    )

    validation_rate = (
        validation_passed / len(validation_tasks) * 100
        if validation_tasks
        else None
    )

    tool_tasks = [
        result for result in results
        if result["tool_success"] is not None
    ]

    tool_success = sum(
        1 for result in tool_tasks
        if result["tool_success"]
    )

    tool_rate = (
        tool_success / len(tool_tasks) * 100
        if tool_tasks
        else None
    )

    total_retries = sum(
        result["retries"]
        for result in results
    )

    return {
        "system": system_name,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "completion_rate": completion_rate,
        "average_execution_time": average_execution_time,
        "average_response_length": average_response_length,
        "memory_rate": memory_rate,
        "validation_rate": validation_rate,
        "tool_rate": tool_rate,
        "total_retries": total_retries
    }


# ============================================================
# COMPARISON REPORT
# ============================================================

def print_comparison(single_metrics, multi_metrics):

    print("\n\n" + "=" * 80)
    print("SINGLE-AGENT vs MULTI-AGENT COMPARISON")
    print("=" * 80)

    print("\nMetric Comparison")
    print("-" * 80)

    print(
        f"{'Metric':<30}"
        f"{'Single-Agent':>20}"
        f"{'Multi-Agent':>20}"
    )

    print("-" * 80)

    print(
        f"{'Task Completion Rate':<30}"
        f"{single_metrics['completion_rate']:>19.1f}%"
        f"{multi_metrics['completion_rate']:>19.1f}%"
    )

    print(
        f"{'Average Execution Time':<30}"
        f"{single_metrics['average_execution_time']:>19.6f}s"
        f"{multi_metrics['average_execution_time']:>19.6f}s"
    )

    print(
        f"{'Average Response Length':<30}"
        f"{single_metrics['average_response_length']:>20.1f}"
        f"{multi_metrics['average_response_length']:>20.1f}"
    )

    print(
        f"{'Memory Save Rate':<30}"
        f"{single_metrics['memory_rate']:>19.1f}%"
        f"{multi_metrics['memory_rate']:>19.1f}%"
    )

    single_validation = (
        "N/A"
        if single_metrics["validation_rate"] is None
        else f"{single_metrics['validation_rate']:.1f}%"
    )

    multi_validation = (
        "N/A"
        if multi_metrics["validation_rate"] is None
        else f"{multi_metrics['validation_rate']:.1f}%"
    )

    print(
        f"{'Validation Rate':<30}"
        f"{single_validation:>20}"
        f"{multi_validation:>20}"
    )

    single_tool = (
        "N/A"
        if single_metrics["tool_rate"] is None
        else f"{single_metrics['tool_rate']:.1f}%"
    )

    multi_tool = (
        "N/A"
        if multi_metrics["tool_rate"] is None
        else f"{multi_metrics['tool_rate']:.1f}%"
    )

    print(
        f"{'Tool Success Rate':<30}"
        f"{single_tool:>20}"
        f"{multi_tool:>20}"
    )

    print(
        f"{'Total Retries':<30}"
        f"{single_metrics['total_retries']:>20}"
        f"{multi_metrics['total_retries']:>20}"
    )

    print("-" * 80)

    print("\nArchitecture Comparison")
    print("-" * 80)

    print(
        "Single-Agent:\n"
        "One agent directly handles the complete request."
    )

    print(
        "\nMulti-Agent:\n"
        "Supervisor dynamically routes the request to "
        "specialized agents such as Tool, Research, "
        "Analysis, Writing and Validator agents."
    )

    print("\nExperimental Interpretation")
    print("-" * 80)

    print(
        "The comparison measures the same five tasks using "
        "both architectures under the current local execution "
        "environment."
    )

    print(
        "\nThe multi-agent architecture provides additional "
        "specialization, routing, validation and persistent "
        "memory capabilities."
    )

    print(
        "\nExecution time should be interpreted together with "
        "the additional capabilities performed by the multi-agent "
        "workflow rather than as a standalone quality measure."
    )

    print("\n" + "=" * 80)
    print("COMPARISON COMPLETED")
    print("=" * 80)


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n" + "#" * 80)
    print("# MULTI-AGENT PERSONAL ASSISTANT SWARM")
    print("# ARCHITECTURE COMPARISON EXPERIMENT")
    print("#" + " " * 79 + "#")
    print("#" * 80)

    single_results = evaluate_single_agent()

    multi_results = evaluate_multi_agent()

    single_metrics = calculate_metrics(
        single_results,
        "Single-Agent"
    )

    multi_metrics = calculate_metrics(
        multi_results,
        "Multi-Agent"
    )

    print_comparison(
        single_metrics,
        multi_metrics
    )


if __name__ == "__main__":
    main()

