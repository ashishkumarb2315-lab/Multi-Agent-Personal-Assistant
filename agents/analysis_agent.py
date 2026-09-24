import re


# ============================================================
# ANALYSIS AGENT
# ============================================================

class AnalysisAgent:
    """
    Analysis Agent

    Development mode:
    Uses local rule-based analysis so the complete
    multi-agent workflow can run without Gemini.
    """

    def __init__(self):

        self.mode = "local"

        print(
            "\nAnalysis Agent Mode: LOCAL"
        )


    # ========================================================
    # ANALYZE
    # ========================================================

    def analyze(self, research_data: str) -> str:

        if not research_data.strip():
            raise ValueError(
                "Research data cannot be empty."
            )

        print(
            "\nAnalysis Agent is processing "
            "the research..."
        )

        benefits = self.extract_section(
            research_data,
            "BENEFITS",
            ["LIMITATIONS", "CHALLENGES"]
        )

        limitations = self.extract_section(
            research_data,
            "LIMITATIONS",
            ["CHALLENGES", "CURRENT TRENDS"]
        )

        challenges = self.extract_section(
            research_data,
            "CHALLENGES",
            ["CURRENT TRENDS", "PRACTICAL EXAMPLES"]
        )

        applications = self.extract_section(
            research_data,
            "APPLICATIONS",
            ["BENEFITS", "LIMITATIONS"]
        )

        trends = self.extract_section(
            research_data,
            "CURRENT TRENDS",
            ["PRACTICAL EXAMPLES", "CONCLUSION"]
        )

        # ----------------------------------------------------
        # Fallback text
        # ----------------------------------------------------

        if not benefits:
            benefits = (
                "Potential benefits include automation, "
                "improved efficiency, data analysis and "
                "decision support."
            )

        if not limitations:
            limitations = (
                "Important limitations include data quality, "
                "incorrect outputs, bias, privacy concerns "
                "and the need for human oversight."
            )

        if not challenges:
            challenges = (
                "Important challenges include data quality, "
                "privacy, security, scalability, cost and "
                "responsible implementation."
            )

        if not applications:
            applications = (
                "The technology can be applied to automation, "
                "analytics, decision support and information "
                "management depending on the domain."
            )

        if not trends:
            trends = (
                "Current development areas include generative "
                "AI, multimodal systems, predictive analytics "
                "and intelligent automation."
            )

        # ----------------------------------------------------
        # Build analysis
        # ----------------------------------------------------

        analysis = f"""
KEY FINDINGS

The research identifies the major concepts,
applications, benefits and limitations associated
with the requested topic.

The information indicates that the technology
can provide useful support when implemented
with appropriate data, validation and human
oversight.


MAJOR BENEFITS

{benefits}


MAJOR RISKS AND LIMITATIONS

{limitations}


TRADE-OFF ANALYSIS

The main trade-off is between the potential
benefits of automation and the need for accuracy,
reliability, privacy and human supervision.

Greater automation may improve efficiency,
but critical applications require appropriate
validation and monitoring.


PRACTICAL IMPLICATIONS

{applications}


CHALLENGES

{challenges}


CURRENT TRENDS

{trends}


POINTS REQUIRING VALIDATION

- Important factual claims should be verified.
- High-impact decisions should not rely solely
  on automated outputs.
- Data quality should be evaluated.
- Model performance should be tested using
  appropriate evaluation metrics.
- Privacy and security requirements should
  be considered.


CONCLUSION

The research suggests that the technology has
meaningful practical applications.

However, successful implementation depends
on appropriate data, validation, monitoring,
security and responsible human oversight.
"""

        print(
            "\nLocal analysis completed."
        )

        return analysis.strip()


    # ========================================================
    # SECTION EXTRACTION
    # ========================================================

    def extract_section(
        self,
        text: str,
        start_heading: str,
        end_headings: list
    ) -> str:

        start_pattern = (
            r"\b"
            + re.escape(start_heading)
            + r"\b"
        )

        match = re.search(
            start_pattern,
            text,
            re.IGNORECASE
        )

        if not match:
            return ""

        start = match.end()

        end = len(text)

        for heading in end_headings:

            heading_match = re.search(
                r"\b"
                + re.escape(heading)
                + r"\b",
                text[start:],
                re.IGNORECASE
            )

            if heading_match:

                candidate_end = (
                    start
                    + heading_match.start()
                )

                if candidate_end < end:
                    end = candidate_end

        return text[start:end].strip()


# ============================================================
# INTERACTIVE TEST
# ============================================================

def main():

    print()
    print("=" * 60)
    print("MULTI-AGENT PERSONAL ASSISTANT")
    print("ANALYSIS AGENT")
    print("=" * 60)

    agent = AnalysisAgent()

    research = input(
        "\nEnter research information:\n> "
    ).strip()

    if not research:

        print(
            "\nERROR: Research data cannot be empty."
        )

        return

    result = agent.analyze(
        research
    )

    print()
    print("=" * 60)
    print("ANALYSIS RESULT")
    print("=" * 60)

    print(result)

    print()
    print("=" * 60)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()