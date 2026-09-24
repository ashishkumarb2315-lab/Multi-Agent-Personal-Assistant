import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()


class PlanningAgent:
    """
    Planning Agent

    Converts a complex user request into smaller executable tasks.
    """

    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY is not set in the .env file."
            )

        self.client = genai.Client(api_key=api_key)

        # Primary model
        self.primary_model = "gemini-3.6-flash"

        # Fallback model
        self.fallback_model = "gemini-3.6-pro"

    def create_plan(self, request: str) -> str:

        prompt = f"""
You are a Planning Agent in a Multi-Agent Personal Assistant Swarm.

Break the following user request into 4 to 6 executable tasks.

Available agents:
- Research Agent
- Analysis Agent
- Writing Agent
- Validator Agent
- Tool Agent
- Memory Agent

For every task provide:

TASK:
DESCRIPTION:
ASSIGNED AGENT:
DEPENDENCY:

User request:
{request}

Return only the execution plan.
"""

        models = [
            self.primary_model,
            self.fallback_model
        ]

        last_error = None

        for model in models:

            for attempt in range(3):

                try:
                    print(
                        f"Using {model} "
                        f"(attempt {attempt + 1}/3)..."
                    )

                    response = self.client.interactions.create(
                        model=model,
                        input=prompt
                    )

                    return response.output_text

                except Exception as error:

                    last_error = error

                    print(
                        f"Model temporarily unavailable. "
                        f"Retrying in {2 ** attempt} seconds..."
                    )

                    time.sleep(2 ** attempt)

        raise RuntimeError(
            f"All Gemini models failed. Last error: {last_error}"
        )


def main():

    print("=" * 60)
    print("MULTI-AGENT PERSONAL ASSISTANT SWARM")
    print("PLANNING AGENT")
    print("=" * 60)

    request = input(
        "\nEnter your complex task:\n> "
    ).strip()

    if not request:
        print("\nPlease enter a task.")
        return

    print("\nCreating execution plan...\n")

    try:

        agent = PlanningAgent()

        plan = agent.create_plan(request)

        print("\n" + "=" * 60)
        print("PLANNING AGENT RESULT")
        print("=" * 60)

        print(plan)

        print("\n" + "=" * 60)
        print("Planning completed successfully.")
        print("=" * 60)

    except Exception as error:

        print("\nERROR:")
        print(error)


if __name__ == "__main__":
    main()