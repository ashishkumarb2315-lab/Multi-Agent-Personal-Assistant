# ============================================================
# VALIDATOR AGENT
# ============================================================

class ValidatorAgent:
    """
    Validator Agent

    Development mode:
    Performs local quality checks on the final
    written response.
    """

    def __init__(self):

        self.mode = "local"

        print(
            "\nValidator Agent Mode: LOCAL"
        )


    # ========================================================
    # VALIDATE
    # ========================================================

    def validate(
        self,
        user_request: str,
        generated_output: str
    ) -> str:

        if not generated_output.strip():

            return (
                "FAIL\n"
                "Reason: Generated output is empty."
            )

        print(
            "\nValidator Agent is checking "
            "the generated response..."
        )

        issues = []

        output_lower = (
            generated_output.lower()
        )

        # ----------------------------------------------------
        # Check minimum length
        # ----------------------------------------------------

        if len(generated_output.strip()) < 200:

            issues.append(
                "Generated response is too short."
            )

        # ----------------------------------------------------
        # Check important sections
        # ----------------------------------------------------

        expected_sections = [
            "introduction",
            "benefits",
            "risks",
            "limitations",
            "challenges",
            "conclusion"
        ]

        missing_sections = []

        for section in expected_sections:

            if section not in output_lower:

                missing_sections.append(
                    section
                )

        if missing_sections:

            issues.append(
                "Missing sections: "
                + ", ".join(
                    missing_sections
                )
            )

        # ----------------------------------------------------
        # Check obvious error messages
        # ----------------------------------------------------

        error_phrases = [
            "error occurred",
            "unable to generate",
            "generation failed",
            "temporarily unavailable"
        ]

        for phrase in error_phrases:

            if phrase in output_lower:

                issues.append(
                    f"Output contains error "
                    f"message: {phrase}"
                )

        # ====================================================
        # VALIDATION RESULT
        # ====================================================

        if issues:

            result = (
                "FAIL\n\n"
                "VALIDATION ISSUES:\n"
            )

            for issue in issues:

                result += (
                    f"- {issue}\n"
                )

            result += (
                "\nRECOMMENDATION:\n"
                "Regenerate or correct the "
                "generated response."
            )

        else:

            result = (
                "PASS\n\n"
                "Validation checks completed "
                "successfully.\n\n"
                "The generated response contains "
                "the expected structure and "
                "sufficient content."
            )

        print(
            "\nValidation completed."
        )

        return result


# ============================================================
# INTERACTIVE TEST
# ============================================================

def main():

    print()
    print("=" * 60)
    print("MULTI-AGENT PERSONAL ASSISTANT")
    print("VALIDATOR AGENT")
    print("=" * 60)

    agent = ValidatorAgent()

    request = input(
        "\nEnter original request:\n> "
    ).strip()

    output = input(
        "\nEnter generated output:\n> "
    ).strip()

    if not request:

        print(
            "\nERROR: Request cannot be empty."
        )

        return

    if not output:

        print(
            "\nERROR: Output cannot be empty."
        )

        return

    result = agent.validate(
        user_request=request,
        generated_output=output
    )

    print()
    print("=" * 60)
    print("VALIDATION RESULT")
    print("=" * 60)

    print(result)

    print()
    print("=" * 60)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()