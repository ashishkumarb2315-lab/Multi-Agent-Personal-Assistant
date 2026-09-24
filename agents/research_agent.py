class ResearchAgent:
    """
    Research Agent

    Development mode:
    Local research processing without requiring Gemini.

    Memory-aware behavior:
    - Performs fresh research when no memory exists.
    - Uses relevant previous memory when available.
    - Identifies the previous response as context rather
      than treating it as new research.
    """

    def __init__(self):

        self.mode = "local"

        print("\nResearch Agent Mode: LOCAL")

    # ========================================================
    # MAIN RESEARCH FUNCTION
    # ========================================================

    def research(
        self,
        user_request: str
    ) -> str:

        if not user_request.strip():
            raise ValueError(
                "Research request cannot be empty."
            )

        print(
            "\nResearch Agent is processing:"
        )

        print(user_request)

        # ----------------------------------------------------
        # Detect memory context
        # ----------------------------------------------------

        memory_marker = (
            "Relevant previous memory:"
        )

        has_memory = (
            memory_marker in user_request
            and
            "No relevant previous memories"
            not in user_request
        )

        # ----------------------------------------------------
        # Extract request
        # ----------------------------------------------------

        research_topic = user_request

        if memory_marker in user_request:

            research_topic = user_request.split(
                memory_marker,
                1
            )[0].strip()

        # ====================================================
        # MEMORY-AWARE RESEARCH
        # ====================================================

        if has_memory:

            print(
                "\nPrevious relevant memory detected."
            )

            print(
                "Research Agent will use previous "
                "work as context."
            )

            overview = (
                "Artificial Intelligence in healthcare "
                "refers to the application of machine "
                "learning, deep learning, natural language "
                "processing, computer vision and related "
                "technologies to healthcare tasks."
            )

            key_concepts = """
- Machine Learning
- Deep Learning
- Natural Language Processing
- Computer Vision
- Predictive Analytics
- Clinical Decision Support
- Medical Data Analysis
"""

            important_facts = """
AI systems can process large amounts of
healthcare data and identify patterns that
may assist healthcare professionals.

Healthcare AI can work with medical images,
electronic health records, laboratory data,
clinical notes and other forms of medical
information.
"""

            applications = """
- Medical image analysis
- Disease risk prediction
- Clinical decision support
- Drug discovery
- Patient monitoring
- Hospital resource management
- Medical documentation
- Personalized treatment support
"""

            benefits = """
- Faster analysis of large datasets
- Support for clinical decision making
- Automation of repetitive tasks
- Improved workflow efficiency
- Assistance with risk identification
- Support for personalized healthcare
"""

            limitations = """
- Data quality affects model performance
- Training data may contain bias
- AI systems can produce incorrect outputs
- Patient privacy must be protected
- Some models are difficult to interpret
- Human oversight remains important
"""

            challenges = """
Healthcare AI requires reliable datasets,
appropriate validation, privacy protection,
security controls, regulatory compliance
and responsible deployment.
"""

            trends = """
Important areas include generative AI,
multimodal AI, medical language models,
AI-assisted medical imaging and clinical
decision-support systems.
"""

            practical_examples = """
AI can assist with medical image analysis,
clinical documentation, patient monitoring,
risk prediction and administrative
healthcare workflows.
"""

            conclusion = """
Artificial Intelligence has significant
potential to support healthcare research,
clinical workflows and medical data analysis.

However, successful implementation requires
validation, privacy protection, security,
human oversight and responsible deployment.
"""

            research = f"""
OVERVIEW

{overview}

KEY CONCEPTS

{key_concepts}

IMPORTANT FACTS

{important_facts}

MAJOR APPLICATIONS

{applications}

BENEFITS

{benefits}

LIMITATIONS

{limitations}

CHALLENGES

{challenges}

CURRENT TRENDS

{trends}

PRACTICAL EXAMPLES

{practical_examples}

MEMORY-AWARE IMPROVEMENT

The previous interaction was identified as
relevant to this request.

The previous response can be used as context
while preparing the current response. The
information should be reviewed and organized
rather than blindly duplicated.

CONCLUSION

{conclusion}
"""

        # ====================================================
        # FRESH RESEARCH
        # ====================================================

        else:

            print(
                "\nNo relevant previous memory detected."
            )

            research = """
OVERVIEW

Artificial Intelligence in healthcare uses
machine learning, deep learning, natural
language processing and computer vision.

KEY CONCEPTS

- Machine Learning
- Deep Learning
- Natural Language Processing
- Computer Vision
- Predictive Analytics
- Clinical Decision Support
- Medical Data Analysis

IMPORTANT FACTS

AI systems can process large amounts of
healthcare data and identify patterns that
may assist healthcare professionals.

Healthcare AI can work with medical images,
electronic health records, laboratory data,
clinical notes and other forms of medical
information.

MAJOR APPLICATIONS

- Medical image analysis
- Disease risk prediction
- Clinical decision support
- Drug discovery
- Patient monitoring
- Hospital resource management
- Medical documentation
- Personalized treatment support

BENEFITS

- Faster analysis of large datasets
- Support for clinical decision making
- Automation of repetitive tasks
- Improved workflow efficiency
- Assistance with risk identification
- Support for personalized healthcare

LIMITATIONS

- Data quality affects model performance
- Training data may contain bias
- AI systems can produce incorrect outputs
- Patient privacy must be protected
- Some models are difficult to interpret
- Human oversight remains important

CHALLENGES

Healthcare AI requires reliable datasets,
appropriate validation, privacy protection,
security controls, regulatory compliance
and responsible deployment.

CURRENT TRENDS

Important areas include generative AI,
multimodal AI, medical language models,
AI-assisted medical imaging and clinical
decision-support systems.

PRACTICAL EXAMPLES

AI can assist with medical image analysis,
clinical documentation, patient monitoring,
risk prediction and administrative
healthcare workflows.

CONCLUSION

Artificial Intelligence has significant
potential to support healthcare research,
clinical workflows and medical data analysis.
However, successful implementation requires
validation, privacy protection, security,
human oversight and responsible deployment.
"""

        print(
            "\nLocal research completed."
        )

        return research.strip()


# ============================================================
# INTERACTIVE TEST
# ============================================================

def main():

    agent = ResearchAgent()

    # --------------------------------------------------------
    # Test 1 — Fresh research
    # --------------------------------------------------------

    print("\n")
    print("=" * 60)
    print("RESEARCH AGENT TEST 1")
    print("=" * 60)

    result_1 = agent.research(
        "research artificial intelligence in healthcare"
    )

    print("\n")
    print(result_1)

    # --------------------------------------------------------
    # Test 2 — Memory-aware research
    # --------------------------------------------------------

    print("\n")
    print("=" * 60)
    print("RESEARCH AGENT TEST 2")
    print("=" * 60)

    result_2 = agent.research(
        """
research artificial intelligence in healthcare

Relevant previous memory:

1. User request: research artificial intelligence
   in healthcare

Assistant response:
Previous research about Artificial Intelligence
in healthcare was completed.
"""
    )

    print("\n")
    print(result_2)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()