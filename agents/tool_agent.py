import ast
import operator
from datetime import datetime


class ToolAgent:
    """
    Tool Agent

    Provides safe local tools for:
    - Calculator
    - Date and time
    - Text analysis
    """

    def __init__(self):

        self.mode = "local"

        print("\nTool Agent Mode: LOCAL")

    # ========================================================
    # CALCULATOR
    # ========================================================

    def calculator(self, expression: str):

        if not expression.strip():

            return "No calculation expression provided."

        try:

            tree = ast.parse(
                expression,
                mode="eval"
            )

            allowed_operators = {

                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.Mod: operator.mod,
                ast.Pow: operator.pow,
                ast.USub: operator.neg,
                ast.UAdd: operator.pos
            }

            def evaluate(node):

                if isinstance(
                    node,
                    ast.Constant
                ):

                    if isinstance(
                        node.value,
                        (int, float)
                    ):

                        return node.value

                    raise ValueError(
                        "Only numbers are allowed."
                    )

                if isinstance(
                    node,
                    ast.BinOp
                ):

                    left = evaluate(
                        node.left
                    )

                    right = evaluate(
                        node.right
                    )

                    operator_type = type(
                        node.op
                    )

                    if operator_type not in allowed_operators:

                        raise ValueError(
                            "Operator not allowed."
                        )

                    return allowed_operators[
                        operator_type
                    ](
                        left,
                        right
                    )

                if isinstance(
                    node,
                    ast.UnaryOp
                ):

                    operand = evaluate(
                        node.operand
                    )

                    operator_type = type(
                        node.op
                    )

                    if operator_type not in allowed_operators:

                        raise ValueError(
                            "Operator not allowed."
                        )

                    return allowed_operators[
                        operator_type
                    ](
                        operand
                    )

                raise ValueError(
                    "Invalid mathematical expression."
                )

            result = evaluate(
                tree.body
            )

            return str(result)

        except ZeroDivisionError:

            return (
                "Calculation error: "
                "division by zero."
            )

        except Exception as error:

            return (
                "Calculation error: "
                + str(error)
            )

    # ========================================================
    # DATE AND TIME
    # ========================================================

    def get_datetime(self):

        current_time = datetime.now()

        return current_time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    # ========================================================
    # TEXT ANALYSIS
    # ========================================================

    def text_analysis(self, text: str):

        if not text.strip():

            return (
                "Characters: 0\n"
                "Words: 0\n"
                "Sentences: 0"
            )

        characters = len(text)

        words = len(
            text.split()
        )

        sentences = 0

        for symbol in [".", "!", "?"]:

            sentences += text.count(
                symbol
            )

        return (
            f"Characters: {characters}\n"
            f"Words: {words}\n"
            f"Sentences: {sentences}"
        )

    # ========================================================
    # CALCULATE FROM NATURAL REQUEST
    # ========================================================

    def extract_expression(
        self,
        request: str
    ):

        request_lower = request.lower()

        prefixes = [
            "calculate",
            "calculator",
            "compute",
            "what is",
            "solve"
        ]

        expression = request.strip()

        for prefix in prefixes:

            if request_lower.startswith(prefix):

                expression = request[
                    len(prefix):
                ].strip()

                break

        return expression

    # ========================================================
    # TOOL EXECUTION
    # ========================================================

    def execute_tool(
        self,
        tool_name: str,
        argument: str = ""
    ):

        tool_name = tool_name.lower().strip()

        if tool_name == "calculator":

            expression = self.extract_expression(
                argument
            )

            return self.calculator(
                expression
            )

        if tool_name in [
            "datetime",
            "date",
            "time"
        ]:

            return self.get_datetime()

        if tool_name in [
            "text",
            "text_analysis"
        ]:

            return self.text_analysis(
                argument
            )

        return (
            f"Unknown tool: {tool_name}"
        )

    # ========================================================
    # AVAILABLE TOOLS
    # ========================================================

    def list_tools(self):

        return [
            "calculator",
            "datetime",
            "text_analysis"
        ]


# ============================================================
# TEST
# ============================================================

def main():

    agent = ToolAgent()

    # --------------------------------------------------------
    # Calculator
    # --------------------------------------------------------

    print("\n")
    print("=" * 60)
    print("CALCULATOR TEST")
    print("=" * 60)

    result = agent.execute_tool(
        "calculator",
        "calculate 25 * 40 + 100"
    )

    print(
        "\nResult:",
        result
    )

    # --------------------------------------------------------
    # Date / Time
    # --------------------------------------------------------

    print("\n")
    print("=" * 60)
    print("DATE/TIME TEST")
    print("=" * 60)

    result = agent.execute_tool(
        "datetime"
    )

    print(
        "\nCurrent date/time:",
        result
    )

    # --------------------------------------------------------
    # Text Analysis
    # --------------------------------------------------------

    print("\n")
    print("=" * 60)
    print("TEXT ANALYSIS TEST")
    print("=" * 60)

    result = agent.execute_tool(
        "text_analysis",
        "Artificial intelligence is useful. "
        "It can automate tasks."
    )

    print("\n" + result)

    # --------------------------------------------------------
    # Available Tools
    # --------------------------------------------------------

    print("\n")
    print("=" * 60)
    print("AVAILABLE TOOLS")
    print("=" * 60)

    for tool in agent.list_tools():

        print(
            f"- {tool}"
        )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()