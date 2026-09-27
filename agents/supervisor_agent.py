class SupervisorAgent:
    """
    Supervisor Agent

    Determines which part of the multi-agent system should handle
    the user's request.

    Routes:
        research -> explanation / information / comparison
        tool     -> calculations / utilities
        direct   -> simple conversational requests
    """

    def __init__(self):
        self.tool_keywords = [
            "calculate",
            "calculator",
            "compute",
            "percentage",
            "percent",
            "sum",
            "multiply",
            "divide",
            "addition",
            "subtraction",
            "subtract",
            "multiply",
            "date",
            "time",
            "current time"
        ]

        self.research_keywords = [
            "research",
            "explain",
            "what is",
            "what are",
            "who is",
            "how does",
            "how do",
            "why",
            "information",
            "compare",
            "comparison",
            "difference",
            "advantages",
            "disadvantages",
            "benefits",
            "limitations",
            "applications",
            "define",
            "meaning",
            "tell me about",
            "describe",
            "machine learning",
            "artificial intelligence",
            "cloud computing",
            "python",
            "sql",
            "databricks",
            "azure data factory",
            "adf"
        ]

    # =========================================================
    # MAIN ROUTING METHOD
    # =========================================================

    def route(self, user_request: str) -> str:
        """
        Decide which agent should handle the request.

        Returns:
            "tool"
            "research"
            "direct"
        """

        request = (user_request or "").strip().lower()

        if not request:
            return "direct"

        # -----------------------------------------------------
        # TOOL ROUTING
        # -----------------------------------------------------

        if self._is_tool_request(request):
            return "tool"

        # -----------------------------------------------------
        # RESEARCH ROUTING
        # -----------------------------------------------------

        if self._is_research_request(request):
            return "research"

        # -----------------------------------------------------
        # DIRECT ROUTING
        # -----------------------------------------------------

        return "direct"

    # =========================================================
    # TOOL DETECTION
    # =========================================================

    def _is_tool_request(self, request: str) -> bool:

        # Explicit calculation words
        for keyword in self.tool_keywords:
            if keyword in request:
                return True

        # Detect simple mathematical expressions
        math_characters = ["+", "-", "*", "/", "%"]

        has_number = any(char.isdigit() for char in request)
        has_math_symbol = any(
            symbol in request
            for symbol in math_characters
        )

        if has_number and has_math_symbol:
            return True

        return False

    # =========================================================
    # RESEARCH DETECTION
    # =========================================================

    def _is_research_request(self, request: str) -> bool:

        for keyword in self.research_keywords:
            if keyword in request:
                return True

        return False

    # =========================================================
    # COMPATIBILITY METHODS
    # =========================================================

    def decide_route(self, user_request: str) -> str:
        """
        Compatibility method for older code.
        """

        return self.route(user_request)

    def get_route(self, user_request: str) -> str:
        """
        Compatibility method for older code.
        """

        return self.route(user_request)

    def classify(self, user_request: str) -> str:
        """
        Compatibility method for older code.
        """

        return self.route(user_request)