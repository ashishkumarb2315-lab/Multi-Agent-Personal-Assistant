import sys
import time
from pathlib import Path
from typing import Dict, List

# ---------------------------------------------------------
# PROJECT ROOT
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from workflows.agent_workflow import build_workflow


class WorkflowEvaluator:
    """
    Evaluation framework for the Multi-Agent Personal Assistant Swarm.

    Measures:
    - Route selection
    - Task completion
    - Research validation
    - Tool success
    - Memory saving
    - Retry count
    - Execution time
    """

    def __init__(self):
        self.workflow = build_workflow()

    # -----------------------------------------------------
    # RUN SINGLE TEST
    # -----------------------------------------------------

    def evaluate_task(self, user_request: str) -> Dict:

        print("\n" + "=" * 70)
        print("EVALUATING TASK")
        print("=" * 70)

        print(f"\nRequest: {user_request}")

        start_time = time.perf_counter()

        try:

            initial_state = {
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

            result = self.workflow.invoke(initial_state)

            end_time = time.perf_counter()

            execution_time = end_time - start_time

            route = result.get(
                "route",
                "unknown"
            )

            final_response = result.get(
                "final_response",
                ""
            )

            validation = result.get(
                "validation",
                ""
            )

            tool_result = result.get(
                "tool_result",
                ""
            )

            memory_saved = result.get(
                "memory_saved",
                False
            )

            retry_count = result.get(
                "retry_count",
                0
            )

            # ---------------------------------------------
            # TASK COMPLETION
            # ---------------------------------------------

            task_completed = bool(
                final_response
                and final_response.strip()
            )

            # ---------------------------------------------
            # RESEARCH VALIDATION
            # ---------------------------------------------

            # Validator is applicable only to research
            # workflows.

            if route == "research":

                validation_applicable = True

                validation_passed = validation.startswith(
                    "PASS"
                )

            else:

                validation_applicable = False

                validation_passed = None

            # ---------------------------------------------
            # TOOL SUCCESS
            # ---------------------------------------------

            if route == "tool":

                tool_success = bool(
                    tool_result
                    and tool_result.strip()
                )

            else:

                tool_success = None

            # ---------------------------------------------
            # RESULT
            # ---------------------------------------------

            evaluation = {

                "request": user_request,

                "route": route,

                "task_completed": task_completed,

                "validation_applicable": validation_applicable,

                "validation_passed": validation_passed,

                "tool_success": tool_success,

                "memory_saved": bool(
                    memory_saved
                ),

                "retry_count": retry_count,

                "execution_time_seconds": round(
                    execution_time,
                    4
                ),

                "final_response_length": len(
                    final_response
                ),

                "status": "SUCCESS"

            }

            # ---------------------------------------------
            # DISPLAY RESULT
            # ---------------------------------------------

            print("\nEvaluation completed.")

            print(
                f"Route: {route}"
            )

            print(
                f"Task completed: "
                f"{task_completed}"
            )

            if validation_applicable:

                print(
                    f"Validation passed: "
                    f"{validation_passed}"
                )

            else:

                print(
                    "Validation passed: N/A "
                    "(not a research task)"
                )

            print(
                f"Memory saved: "
                f"{memory_saved}"
            )

            print(
                f"Retry count: "
                f"{retry_count}"
            )

            print(
                f"Execution time: "
                f"{execution_time:.4f} seconds"
            )

            return evaluation

        except Exception as error:

            end_time = time.perf_counter()

            execution_time = end_time - start_time

            print(
                f"\nEvaluation failed: {error}"
            )

            return {

                "request": user_request,

                "route": "error",

                "task_completed": False,

                "validation_applicable": False,

                "validation_passed": None,

                "tool_success": False,

                "memory_saved": False,

                "retry_count": 0,

                "execution_time_seconds": round(
                    execution_time,
                    4
                ),

                "final_response_length": 0,

                "status": "FAILED",

                "error": str(error)

            }

    # -----------------------------------------------------
    # RUN TEST SUITE
    # -----------------------------------------------------

    def run_evaluation_suite(
        self,
        tasks: List[str]
    ) -> List[Dict]:

        print("\n" + "=" * 70)
        print("MULTI-AGENT SYSTEM EVALUATION")
        print("=" * 70)

        results = []

        for index, task in enumerate(
            tasks,
            start=1
        ):

            print(
                f"\n\nTEST CASE {index}/{len(tasks)}"
            )

            result = self.evaluate_task(
                task
            )

            results.append(
                result
            )

        return results

    # -----------------------------------------------------
    # GENERATE SUMMARY
    # -----------------------------------------------------

    def generate_summary(
        self,
        results: List[Dict]
    ) -> Dict:

        if not results:
            return {}

        total_tasks = len(results)

        # ---------------------------------------------
        # TASK COMPLETION
        # ---------------------------------------------

        completed_tasks = sum(
            1
            for result in results
            if result["task_completed"]
        )

        task_completion_rate = (
            completed_tasks
            / total_tasks
            * 100
        )

        # ---------------------------------------------
        # RESEARCH VALIDATION
        # ---------------------------------------------

        research_results = [
            result
            for result in results
            if result["validation_applicable"]
        ]

        if research_results:

            validated_tasks = sum(
                1
                for result in research_results
                if result["validation_passed"]
            )

            research_validation_rate = (
                validated_tasks
                / len(research_results)
                * 100
            )

        else:

            validated_tasks = 0

            research_validation_rate = 0.0

        # ---------------------------------------------
        # MEMORY
        # ---------------------------------------------

        memory_tasks = sum(
            1
            for result in results
            if result["memory_saved"]
        )

        memory_save_rate = (
            memory_tasks
            / total_tasks
            * 100
        )

        # ---------------------------------------------
        # SYSTEM SUCCESS
        # ---------------------------------------------

        successful_tasks = sum(
            1
            for result in results
            if result["status"] == "SUCCESS"
        )

        system_success_rate = (
            successful_tasks
            / total_tasks
            * 100
        )

        # ---------------------------------------------
        # RETRIES
        # ---------------------------------------------

        total_retries = sum(
            result["retry_count"]
            for result in results
        )

        # ---------------------------------------------
        # EXECUTION TIME
        # ---------------------------------------------

        total_execution_time = sum(
            result["execution_time_seconds"]
            for result in results
        )

        average_execution_time = (
            total_execution_time
            / total_tasks
        )

        # ---------------------------------------------
        # TOOL SUCCESS
        # ---------------------------------------------

        tool_results = [
            result
            for result in results
            if result["tool_success"] is not None
        ]

        if tool_results:

            successful_tools = sum(
                1
                for result in tool_results
                if result["tool_success"]
            )

            tool_success_rate = (
                successful_tools
                / len(tool_results)
                * 100
            )

        else:

            tool_success_rate = 0.0

        # ---------------------------------------------
        # ROUTE DISTRIBUTION
        # ---------------------------------------------

        route_distribution = {}

        for result in results:

            route = result["route"]

            route_distribution[route] = (
                route_distribution.get(
                    route,
                    0
                ) + 1
            )

        # ---------------------------------------------
        # FINAL SUMMARY
        # ---------------------------------------------

        summary = {

            "total_tasks": total_tasks,

            "completed_tasks": completed_tasks,

            "task_completion_rate": round(
                task_completion_rate,
                2
            ),

            "research_validation_tasks": len(
                research_results
            ),

            "validated_research_tasks": validated_tasks,

            "research_validation_rate": round(
                research_validation_rate,
                2
            ),

            "tool_success_rate": round(
                tool_success_rate,
                2
            ),

            "memory_save_rate": round(
                memory_save_rate,
                2
            ),

            "system_success_rate": round(
                system_success_rate,
                2
            ),

            "average_execution_time_seconds": round(
                average_execution_time,
                4
            ),

            "total_retries": total_retries,

            "route_distribution": route_distribution

        }

        return summary

    # -----------------------------------------------------
    # PRINT REPORT
    # -----------------------------------------------------

    def print_report(
        self,
        results: List[Dict],
        summary: Dict
    ):

        print("\n" + "=" * 70)
        print("EVALUATION REPORT")
        print("=" * 70)

        print(
            f"\nTotal Tasks: "
            f"{summary['total_tasks']}"
        )

        print(
            f"Completed Tasks: "
            f"{summary['completed_tasks']}"
        )

        print(
            f"Task Completion Rate: "
            f"{summary['task_completion_rate']}%"
        )

        print(
            f"Research Validation Tasks: "
            f"{summary['research_validation_tasks']}"
        )

        print(
            f"Validated Research Tasks: "
            f"{summary['validated_research_tasks']}"
        )

        print(
            f"Research Validation Rate: "
            f"{summary['research_validation_rate']}%"
        )

        print(
            f"Tool Success Rate: "
            f"{summary['tool_success_rate']}%"
        )

        print(
            f"Memory Save Rate: "
            f"{summary['memory_save_rate']}%"
        )

        print(
            f"System Success Rate: "
            f"{summary['system_success_rate']}%"
        )

        print(
            f"Average Execution Time: "
            f"{summary['average_execution_time_seconds']} "
            f"seconds"
        )

        print(
            f"Total Retries: "
            f"{summary['total_retries']}"
        )

        print("\nRoute Distribution:")

        for route, count in summary[
            "route_distribution"
        ].items():

            print(
                f"  {route}: {count}"
            )

        print("\n" + "=" * 70)


# ---------------------------------------------------------
# MAIN EVALUATION
# ---------------------------------------------------------

if __name__ == "__main__":

    evaluator = WorkflowEvaluator()

    test_tasks = [

        "Hello",

        "Calculate 25 * 40",

        (
            "What is Artificial Intelligence? "
            "Explain its benefits, risks, "
            "and practical applications."
        ),

        (
            "Explain machine learning "
            "and its major applications."
        ),

        (
            "What are the benefits and "
            "limitations of cloud computing?"
        )

    ]

    results = evaluator.run_evaluation_suite(
        test_tasks
    )

    summary = evaluator.generate_summary(
        results
    )

    evaluator.print_report(
        results,
        summary
    )

