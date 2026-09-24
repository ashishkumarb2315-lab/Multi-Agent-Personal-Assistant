import os

from dotenv import load_dotenv
from google import genai


# ========================================================
# LOAD ENVIRONMENT
# ========================================================

load_dotenv()


class SupervisorAgent:
    """
    Supervisor / Orchestrator Agent.

    Responsibilities:
    - Understand the user's request
    - Identify required agents
    - Determine execution order
    - Decide whether tools are required
    - Produce a workflow decision
    """

    def __init__(self):

        api_key = os.getenv(
            "GOOGLE_API_KEY"
        )

        if not api_key:

            raise ValueError(
                "GOOGLE_API_KEY is not set "
                "in the .env file."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.primary_model = (
            "gemini-3.8-flash"
        )

        self.fallback_model = (
            "gemini-3.7-flash"
        )

    # ====================================================
    # SUPERVISOR DECISION
    # ====================================================

    def decide_workflow(
        self,
        user_request: str
    ) -> str:

        if not user_request.strip():

            raise ValueError(
                "User request cannot be empty."
            )

        prompt = f"""
You are the Supervisor Agent of a
Multi-Agent Personal Assistant Swarm.

Your job is to analyze the user's request
and decide which specialized agents are
required.

AVAILABLE AGENTS:

1. Planning Agent
   - Breaks complex tasks into steps.

2. Research Agent
   - Performs information research.

3. Analysis Agent
   - Analyzes information and identifies insights.

4. Writing Agent
   - Produces structured written output.

5. Tool Agent
   - Performs calculations, date/time operations,
     text analysis and other utilities.

6. Memory Agent
   - Stores and retrieves useful long-term context.

7. Validator Agent
   - Checks the quality and completeness
     of generated results.

Return your decision in exactly this structure:

REQUEST TYPE:
<type>

REQUIRED AGENTS:
<comma-separated list>

EXECUTION ORDER:
<ordered list>

TOOL REQUIRED:
<YES or NO>

MEMORY REQUIRED:
<YES or NO>

REASONING:
<short explanation>

FINAL OBJECTIVE:
<what the system should ultimately produce>

USER REQUEST:
{user_request}
"""

        models = [
            self.primary_model,
            self.fallback_model
        ]

        last_error = None

        for model in models:

            try:

                response = (
                    self.client.interactions.create(
                        model=model,
                        input=prompt
                    )
                )

                return response.output_text

            except Exception as error:

                last_error = error

        raise RuntimeError(
            f"Supervisor Agent failed. "
            f"Last error: {last_error}"
        )


# ========================================================
# TEST PROGRAM
# ========================================================

def main():

    print()

    print("=" * 60)
    print("MULTI-AGENT PERSONAL ASSISTANT")
    print("SUPERVISOR AGENT")
    print("=" * 60)

    try:

        agent = SupervisorAgent()

        request = input(
            "\nEnter a user request:\n> "
        ).strip()

        if not request:

            print(
                "\nERROR: Request cannot be empty."
            )

            return

        print(
            "\nSupervisor analyzing request..."
        )

        decision = agent.decide_workflow(
            request
        )

        print()

        print("=" * 60)
        print("SUPERVISOR DECISION")
        print("=" * 60)

        print(decision)

    except Exception as error:

        print()

        print("=" * 60)
        print("SUPERVISOR ERROR")
        print("=" * 60)

        print(
            f"Error Type: "
            f"{type(error).__name__}"
        )

        print(
            f"Error Message: "
            f"{error}"
        )


# ========================================================
# RUN
# ========================================================

if __name__ == "__main__":

    main()