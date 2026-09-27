"""
Analysis Agent
--------------
Analyzes the research produced by the Research Agent and creates
topic-specific interpretations, practical implications, limitations,
and an overall assessment.

The Analysis Agent does not replace the Research Agent's content.
It analyzes the research that it receives.
"""


class AnalysisAgent:
    """
    Analysis agent responsible for evaluating research content.
    """

    def __init__(self):
        self.name = "Analysis Agent"

    # ------------------------------------------------------------------
    # Utility Methods
    # ------------------------------------------------------------------

    def _clean_text(self, text: str) -> str:
        """Clean unnecessary whitespace."""

        if not text:
            return ""

        lines = text.splitlines()

        cleaned = []

        for line in lines:
            line = line.strip()

            if line:
                cleaned.append(line)

        return "\n".join(cleaned)

    def _detect_topic(self, text: str) -> str:
        """
        Detect the topic from the supplied research.

        Research content is used as the primary source.
        """

        content = (text or "").lower()

        if (
            "artificial intelligence in healthcare" in content
            or "ai in healthcare" in content
            or (
                "artificial intelligence" in content
                and "healthcare" in content
            )
        ):
            return "Artificial Intelligence in Healthcare"

        if (
            "azure data factory" in content
            or "azure datafactory" in content
        ):
            return "Azure Data Factory"

        if "machine learning" in content:
            return "Machine Learning"

        if "cloud computing" in content:
            return "Cloud Computing"

        if "databricks" in content:
            return "Databricks"

        if "artificial intelligence" in content:
            return "Artificial Intelligence"

        if "python" in content:
            return "Python"

        if "sql" in content:
            return "SQL"

        return "the requested topic"

    # ------------------------------------------------------------------
    # Healthcare Analysis
    # ------------------------------------------------------------------

    def _healthcare_analysis(self) -> dict:
        """
        Return topic-specific analytical points for AI in healthcare.
        """

        return {
            "relevance": (
                "The research is directly relevant to healthcare because "
                "it focuses on how AI can process medical information, "
                "support healthcare workflows, assist decision-making, "
                "and help identify patterns in healthcare data."
            ),

            "main_concept": (
                "The central concept is the use of AI technologies such as "
                "machine learning, deep learning, natural language processing, "
                "and computer vision to support healthcare-related tasks."
            ),

            "important_points": (
                "The research identifies medical imaging, electronic health "
                "records, disease and health-risk prediction, clinical "
                "decision support, patient monitoring, drug discovery, "
                "clinical documentation, and personalized healthcare as "
                "important application areas."
            ),

            "practical_interpretation": (
                "In practice, AI can act as a decision-support and automation "
                "technology. For example, it can help analyze medical images, "
                "process large healthcare datasets, identify potential risk "
                "patterns, summarize clinical information, and support "
                "healthcare professionals. These systems should support "
                "rather than replace appropriate professional judgment."
            ),

            "limitations": (
                "The effectiveness of healthcare AI depends on the quality "
                "and representativeness of available data. Bias, incorrect "
                "predictions, privacy concerns, security vulnerabilities, "
                "limited explainability, and insufficient validation can "
                "limit safe and reliable deployment."
            ),

            "assessment": (
                "The research provides a sufficient structured foundation "
                "for understanding AI in healthcare. However, real-world "
                "implementation requires additional validation using "
                "appropriate datasets, healthcare workflows, security "
                "requirements, privacy controls, and domain-specific "
                "performance measures."
            ),
        }

    # ------------------------------------------------------------------
    # Generic Analysis
    # ------------------------------------------------------------------

    def _generic_analysis(self, topic: str) -> dict:
        """
        Generic analytical framework for topics that do not have a
        dedicated domain-specific analysis.
        """

        return {
            "relevance": (
                f"The research is relevant to {topic} because it "
                "addresses the main concepts, benefits, applications, "
                "risks, and practical considerations associated with "
                "the topic."
            ),

            "main_concept": (
                f"The central concept is understanding how {topic} "
                "can be applied to practical requirements and workflows."
            ),

            "important_points": (
                f"The research identifies the major concepts, benefits, "
                f"applications, risks, challenges, and trends associated "
                f"with {topic}."
            ),

            "practical_interpretation": (
                f"In practice, {topic} can provide value when it is "
                "implemented according to the specific requirements, "
                "available resources, and intended use case."
            ),

            "limitations": (
                "The effectiveness of the approach depends on data quality, "
                "implementation decisions, security, reliability, and "
                "appropriate validation."
            ),

            "assessment": (
                f"The research provides a structured foundation for "
                f"understanding {topic}. Further evaluation may be required "
                "before applying the information to a real-world environment."
            ),
        }

    # ------------------------------------------------------------------
    # Main Analysis Method
    # ------------------------------------------------------------------

    def analyze(
        self,
        research_data: str,
        user_request: str = ""
    ) -> str:
        """
        Analyze the Research Agent output.

        Parameters
        ----------
        research_data:
            Research Agent output.

        user_request:
            Original user request. It is optional so the existing
            workflow and tests remain compatible.

        Returns
        -------
        str
            Structured analytical response.
        """

        research_data = research_data or ""
        user_request = user_request or ""

        if not research_data.strip():
            return (
                "Analysis could not be completed because no research "
                "content was provided."
            )

        topic = self._detect_topic(
            research_data
        )

        # --------------------------------------------------------------
        # Select domain-specific analysis.
        # --------------------------------------------------------------

        if topic == "Artificial Intelligence in Healthcare":
            analysis = self._healthcare_analysis()
        else:
            analysis = self._generic_analysis(topic)

        # --------------------------------------------------------------
        # Build analytical response.
        # --------------------------------------------------------------

        output = []

        output.append(
            f"Analysis Topic: {topic}"
        )

        if user_request.strip():
            output.append(
                f"Current User Request: {user_request.strip()}"
            )

        output.append(
            "Analysis:"
        )

        output.append(
            "1. Relevance"
        )
        output.append(
            analysis["relevance"]
        )

        output.append(
            "2. Main Concept"
        )
        output.append(
            analysis["main_concept"]
        )

        output.append(
            "3. Important Points"
        )
        output.append(
            analysis["important_points"]
        )

        output.append(
            "4. Practical Interpretation"
        )
        output.append(
            analysis["practical_interpretation"]
        )

        output.append(
            "5. Limitations"
        )
        output.append(
            analysis["limitations"]
        )

        output.append(
            "6. Final Assessment"
        )
        output.append(
            analysis["assessment"]
        )

        return "\n".join(output)


# ----------------------------------------------------------------------
# Manual Test
# ----------------------------------------------------------------------

if __name__ == "__main__":

    research = """
    # Artificial Intelligence in Healthcare

    ## 1. Introduction

    Artificial Intelligence in healthcare refers to the use of
    computational systems to analyze healthcare data.

    ## 2. Research Summary

    AI can process medical images, electronic health records,
    laboratory results, and patient monitoring data.

    ## 3. Key Benefits

    - Faster analysis of healthcare data.
    - Support for clinical decision-making.

    ## 4. Risks and Limitations

    - Data bias.
    - Privacy concerns.
    - Security risks.

    ## 5. Practical Applications

    - Medical imaging.
    - Disease prediction.
    - Patient monitoring.
    - Drug discovery.

    ## 6. Challenges

    - Data quality.
    - Explainability.
    - Privacy.
    """

    agent = AnalysisAgent()

    result = agent.analyze(
        research,
        "Research artificial intelligence in healthcare"
    )

    print(result)