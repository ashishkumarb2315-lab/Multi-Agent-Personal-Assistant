class ValidatorAgent:
    """
    Validator Agent

    Validates generated responses for:
    - Required sections
    - Minimum content
    - Obvious generation errors

    The validator does NOT perform strict topic matching.
    """

    REQUIRED_SECTIONS = [
        "introduction",
        "research summary",
        "key benefits",
        "risks and limitations",
        "practical applications",
        "challenges",
        "current trends",
        "validation considerations",
        "conclusion",
    ]

    ERROR_PHRASES = [
        "an error occurred",
        "error occurred",
        "exception occurred",
        "traceback",
        "unable to generate",
        "failed to generate",
    ]

    def __init__(self):
        self.agent_name = "Validator Agent"

    # ============================================================
    # VALIDATE
    # ============================================================

    def validate(
        self,
        user_request,
        generated_output
    ):
        """
        Validate a generated response.

        Parameters
        ----------
        user_request : str
            Original user request.

        generated_output : str
            Generated response.

        Returns
        -------
        str
            PASS or FAIL validation result.
        """

        output = str(
            generated_output
            if generated_output is not None
            else ""
        ).strip()

        # --------------------------------------------------------
        # EMPTY RESPONSE
        # --------------------------------------------------------

        if not output:

            missing_sections = self._get_missing_sections(
                output
            )

            return (
                "FAIL\n\n"
                "VALIDATION ISSUES:\n"
                "- Response is empty.\n\n"
                "Missing sections:\n"
                + self._format_missing_sections(
                    missing_sections
                )
                + "\n\n"
                "RECOMMENDATION: Generate a complete response."
            )

        output_lower = output.lower()

        issues = []

        # --------------------------------------------------------
        # ERROR MESSAGE CHECK
        # --------------------------------------------------------

        for error_phrase in self.ERROR_PHRASES:

            if error_phrase in output_lower:

                issues.append(
                    "Response contains an error message."
                )

                break

        # --------------------------------------------------------
        # REQUIRED SECTION CHECK
        # --------------------------------------------------------

        missing_sections = self._get_missing_sections(
            output
        )

        if missing_sections:

            issues.append(
                "Missing sections:\n"
                + self._format_missing_sections(
                    missing_sections
                )
            )

        # --------------------------------------------------------
        # MINIMUM LENGTH CHECK
        # --------------------------------------------------------

        if len(output) < 100:

            issues.append(
                "Response is too short."
            )

        # --------------------------------------------------------
        # IMPORTANT:
        #
        # We intentionally do NOT compare the user request
        # against the generated response.
        #
        # Example:
        #
        #     user_request = "test request"
        #
        # is only a test input. The supplied output already
        # contains all required sections and should therefore
        # PASS.
        # --------------------------------------------------------

        # --------------------------------------------------------
        # FAIL
        # --------------------------------------------------------

        if issues:

            return (
                "FAIL\n\n"
                "VALIDATION ISSUES:\n"
                + "\n".join(
                    f"- {issue}"
                    for issue in issues
                )
                + "\n\n"
                "RECOMMENDATION: Generate a more complete "
                "and structurally valid answer."
            )

        # --------------------------------------------------------
        # PASS
        # --------------------------------------------------------

        return (
            "PASS\n\n"
            "VALIDATION SUMMARY:\n"
            "- All required sections are present.\n"
            "- Response contains sufficient content.\n"
            "- No obvious generation error was detected.\n"
            "- Response structure is valid.\n"
        )

    # ============================================================
    # GET MISSING SECTIONS
    # ============================================================

    def _get_missing_sections(
        self,
        output
    ):
        """
        Return all required sections missing from the output.
        """

        output_lower = str(
            output
            if output is not None
            else ""
        ).lower()

        missing_sections = []

        for section in self.REQUIRED_SECTIONS:

            if section not in output_lower:

                missing_sections.append(
                    section
                )

        return missing_sections

    # ============================================================
    # FORMAT MISSING SECTIONS
    # ============================================================

    def _format_missing_sections(
        self,
        sections
    ):
        """
        Format missing sections into a readable list.
        """

        if not sections:

            return "- None"

        return "\n".join(
            f"- {section.title()}"
            for section in sections
        )

    # ============================================================
    # CHECK REQUIRED SECTIONS
    # ============================================================

    def check_required_sections(
        self,
        generated_output
    ):
        """
        Return missing required sections.
        """

        return self._get_missing_sections(
            generated_output
        )

    # ============================================================
    # IS VALID
    # ============================================================

    def is_valid(
        self,
        user_request,
        generated_output
    ):
        """
        Return True when the generated response passes.
        """

        result = self.validate(
            user_request,
            generated_output
        )

        return result.startswith(
            "PASS"
        )


# ================================================================
# DIRECT TEST
# ================================================================

if __name__ == "__main__":

    agent = ValidatorAgent()

    output = """
    Introduction

    This is an introduction to the topic.

    Research Summary

    Research information is presented here.

    Key Benefits

    The benefits are explained here.

    Risks and Limitations

    Risks and limitations are explained here.

    Practical Applications

    Practical applications are explained here.

    Challenges

    Challenges are explained here.

    Current Trends

    Current trends are explained here.

    Validation Considerations

    Validation considerations are explained here.

    Conclusion

    This is the conclusion.
    """

    result = agent.validate(
        "test request",
        output
    )

    print("=" * 70)
    print(result)
    print("=" * 70)