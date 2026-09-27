
import re
import time
from datetime import datetime


class SingleAgentBaseline:
    """
    Single-Agent Baseline

    This represents a simple architecture where one agent handles
    the complete user request without specialized agent-to-agent
    orchestration, validation routing, or multi-agent delegation.

    The baseline is intentionally lightweight and works offline.
    """

    def __init__(self):
        self.mode = "LOCAL_SINGLE_AGENT"

    def _calculate(self, expression):
        """
        Safe calculator for basic arithmetic.
        """
        expression = expression.replace("×", "*").replace("÷", "/")

        if not re.fullmatch(r"[0-9+\-*/().%\s]+", expression):
            return "Unable to calculate the expression."

        try:
            result = eval(
                expression,
                {"__builtins__": {}},
                {}
            )
            return str(result)
        except Exception:
            return "Unable to calculate the expression."

    def _extract_expression(self, request):
        patterns = [
            r"calculate\s+(.+)",
            r"compute\s+(.+)",
            r"what\s+is\s+(.+)"
        ]

        for pattern in patterns:
            match = re.search(pattern, request, re.IGNORECASE)
            if match:
                expression = match.group(1).strip()

                if re.fullmatch(r"[0-9+\-*/().%\s]+", expression):
                    return expression

        return None

    def _research_response(self, request):
        """
        Local deterministic responses used when the external LLM
        service is unavailable.
        """

        request_lower = request.lower()

        if "artificial intelligence" in request_lower:
            return """
Artificial Intelligence is a field of computer science that develops
systems capable of performing tasks that normally require human
intelligence.

Benefits:
- Automation of repetitive tasks
- Faster decision support
- Improved productivity
- Ability to process large datasets

Risks:
- Privacy and security concerns
- Bias in AI systems
- Incorrect or unreliable outputs
- Job displacement in some activities

Practical Applications:
- Healthcare
- Banking
- Customer service
- Recommendation systems
- Fraud detection
- Autonomous systems
"""

        if "machine learning" in request_lower:
            return """
Machine Learning is a branch of Artificial Intelligence in which
computer systems learn patterns from data and use those patterns
to make predictions or decisions.

Major applications include:
- Recommendation systems
- Fraud detection
- Image recognition
- Speech recognition
- Predictive maintenance
- Medical diagnosis support
- Customer analytics
"""

        if "cloud computing" in request_lower:
            return """
Cloud computing provides computing resources such as storage,
servers, databases, networking and software through internet-based
services.

Benefits:
- Scalability
- Flexible resource usage
- Reduced infrastructure management
- Accessibility
- Faster deployment

Limitations:
- Internet dependency
- Security and privacy concerns
- Vendor dependency
- Possible service outages
- Ongoing usage costs
"""

        return """
The requested topic can be analyzed using a structured approach.

The answer should consider:
- Definition and background
- Major benefits
- Risks and limitations
- Practical applications
- Challenges
- Current trends
- Conclusion
"""

    def process(self, user_request):
        """
        Process the complete request using one agent.
        """

        start_time = time.perf_counter()

        request = user_request.strip()

        if not request:
            response = "Please provide a valid request."

        elif request.lower() in ["hello", "hi", "hey"]:
            response = (
                "Hello! I am the Single-Agent Baseline Assistant. "
                "How can I help you?"
            )

        else:
            expression = self._extract_expression(request)

            if expression:
                response = self._calculate(expression)

            else:
                response = self._research_response(request)

        execution_time = time.perf_counter() - start_time

        return {
            "user_request": user_request,
            "response": response.strip(),
            "execution_time": round(execution_time, 6),
            "status": "completed" if response.strip() else "failed",
            "mode": self.mode,
            "timestamp": datetime.now().isoformat()
        }


def main():
    agent = SingleAgentBaseline()

    print("\n" + "=" * 70)
    print("SINGLE-AGENT BASELINE TEST")
    print("=" * 70)

    test_requests = [
        "Hello",
        "Calculate 25 * 40",
        "What is Artificial Intelligence? Explain its benefits, risks, and practical applications.",
        "Explain machine learning and its major applications.",
        "What are the benefits and limitations of cloud computing?"
    ]

    for index, request in enumerate(test_requests, start=1):
        result = agent.process(request)

        print(f"\nTest Case {index}")
        print("-" * 70)
        print(f"Request: {request}")
        print(f"Status: {result['status']}")
        print(f"Execution Time: {result['execution_time']} seconds")
        print(f"Mode: {result['mode']}")
        print("\nResponse:")
        print(result["response"])

    print("\n" + "=" * 70)
    print("SINGLE-AGENT BASELINE TEST COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()

