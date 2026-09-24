class WritingAgent:
    """
    Writing Agent

    Converts research and analysis into
    a clean, structured final response.

    Development mode:
    Local processing without requiring Gemini.
    """

    def __init__(self):
        self.mode = "local"

        print("\nWriting Agent Mode: LOCAL")

    # ========================================================
    # MAIN WRITING FUNCTION
    # ========================================================

    def write(
        self,
        research_data: str,
        analysis_data: str,
        requested_format: str = "structured response"
    ) -> str:

        if not research_data.strip():
            raise ValueError(
                "Research data cannot be empty."
            )

        if not analysis_data.strip():
            raise ValueError(
                "Analysis data cannot be empty."
            )

        print(
            "\nWriting Agent is preparing "
            "the final response..."
        )

        # ----------------------------------------------------
        # Extract only required sections
        # ----------------------------------------------------

        overview = self.extract_section(
            research_data,
            "OVERVIEW",
            ["KEY CONCEPTS"]
        )

        benefits = self.extract_section(
            analysis_data,
            "MAJOR BENEFITS",
            ["MAJOR RISKS AND LIMITATIONS"]
        )

        risks = self.extract_section(
            analysis_data,
            "MAJOR RISKS AND LIMITATIONS",
            ["TRADE-OFF ANALYSIS"]
        )

        applications = self.extract_section(
            analysis_data,
            "PRACTICAL IMPLICATIONS",
            ["CHALLENGES"]
        )

        challenges = self.extract_section(
            analysis_data,
            "CHALLENGES",
            ["CURRENT TRENDS"]
        )

        trends = self.extract_section(
            analysis_data,
            "CURRENT TRENDS",
            ["POINTS REQUIRING VALIDATION"]
        )

        validation = self.extract_section(
            analysis_data,
            "POINTS REQUIRING VALIDATION",
            ["CONCLUSION"]
        )

        conclusion = self.extract_section(
            analysis_data,
            "CONCLUSION",
            None
        )

        # ----------------------------------------------------
        # Fallback values
        # ----------------------------------------------------

        if not overview:
            overview = (
                "Artificial Intelligence in healthcare "
                "uses technologies such as machine learning, "
                "deep learning, natural language processing "
                "and computer vision to support healthcare "
                "tasks."
            )

        if not benefits:
            benefits = (
                "AI can support faster data analysis, "
                "workflow automation and clinical "
                "decision support."
            )

        if not risks:
            risks = (
                "Important limitations include data quality, "
                "bias, incorrect outputs, privacy concerns "
                "and the need for human oversight."
            )

        if not applications:
            applications = (
                "Applications include medical image analysis, "
                "disease risk prediction, clinical decision "
                "support, drug discovery and patient monitoring."
            )

        if not challenges:
            challenges = (
                "Important challenges include reliable data, "
                "validation, privacy, security, regulatory "
                "compliance and responsible deployment."
            )

        if not trends:
            trends = (
                "Current development areas include generative "
                "AI, multimodal AI, medical language models "
                "and AI-assisted medical imaging."
            )

        if not validation:
            validation = (
                "- Important factual claims should be verified.\n"
                "- Data quality should be evaluated.\n"
                "- Model performance should be tested.\n"
                "- Privacy and security should be considered.\n"
                "- Human oversight should be maintained."
            )

        if not conclusion:
            conclusion = (
                "Successful implementation requires "
                "appropriate data, validation, monitoring, "
                "security and responsible human oversight."
            )

        # ====================================================
        # CLEAN FINAL RESPONSE
        # ====================================================

        final_response = f"""
# Artificial Intelligence in Healthcare

## 1. Introduction

{overview}

## 2. Research Summary

Artificial Intelligence in healthcare combines
multiple AI technologies to process healthcare
information and support healthcare-related tasks.

The system can work with different forms of
healthcare information including medical images,
electronic health records, laboratory data and
clinical notes.

## 3. Key Benefits

{benefits}

## 4. Risks and Limitations

{risks}

## 5. Practical Applications

{applications}

## 6. Challenges

{challenges}

## 7. Current Trends

{trends}

## 8. Validation Considerations

{validation}

## 9. Conclusion

{conclusion}

## 10. Final Perspective

AI can provide useful support for healthcare
research, clinical workflows and medical data
analysis.

However, effective implementation requires
reliable data, appropriate validation, privacy
protection, security controls and human oversight.
"""

        print("\nLocal writing completed.")

        return final_response.strip()

    # ========================================================
    # SECTION EXTRACTION
    # ========================================================

    def extract_section(
        self,
        text,
        start_heading,
        end_headings=None
    ):

        if not text:
            return ""

        text_upper = text.upper()

        start_marker = start_heading.upper()

        start_index = text_upper.find(
            start_marker
        )

        if start_index == -1:
            return ""

        content_start = (
            start_index +
            len(start_marker)
        )

        content_end = len(text)

        if end_headings:

            for heading in end_headings:

                if not heading:
                    continue

                end_index = text_upper.find(
                    heading.upper(),
                    content_start
                )

                if (
                    end_index != -1
                    and end_index < content_end
                ):
                    content_end = end_index

        return text[
            content_start:content_end
        ].strip()


# ============================================================
# INTERACTIVE TEST
# ============================================================

def main():

    agent = WritingAgent()

    research = """
OVERVIEW

Artificial Intelligence in healthcare uses
machine learning, deep learning, natural
language processing and computer vision.

KEY CONCEPTS

Machine Learning
Deep Learning

"""

    analysis = """
MAJOR BENEFITS

- Faster analysis
- Automation
- Decision support

MAJOR RISKS AND LIMITATIONS

- Data quality
- Bias
- Privacy

TRADE-OFF ANALYSIS

Automation requires validation.

PRACTICAL IMPLICATIONS

- Medical image analysis
- Patient monitoring

CHALLENGES

- Data quality
- Security

CURRENT TRENDS

- Generative AI
- Multimodal AI

POINTS REQUIRING VALIDATION

- Verify factual claims
- Evaluate model performance

CONCLUSION

AI can support healthcare when
implemented responsibly.
"""

    result = agent.write(
        research,
        analysis
    )

    print("\n")
    print("=" * 60)
    print("WRITING AGENT TEST RESULT")
    print("=" * 60)

    print(result)


if __name__ == "__main__":
    main()