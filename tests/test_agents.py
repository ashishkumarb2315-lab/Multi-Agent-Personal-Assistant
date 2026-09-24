from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.writing_agent import WritingAgent
from agents.validator_agent import ValidatorAgent
from agents.tool_agent import ToolAgent


def test_research_agent_creation():
    agent = ResearchAgent()

    assert agent is not None


def test_research_agent_fresh():
    agent = ResearchAgent()

    result = agent.research(
        "research artificial intelligence in healthcare"
    )

    assert result is not None
    assert len(result) > 0


def test_research_agent_memory_aware():
    agent = ResearchAgent()

    request = """
    research artificial intelligence in healthcare

    Relevant previous memory:
    Previous research discussed AI applications in healthcare.
    """

    result = agent.research(request)

    assert result is not None
    assert len(result) > 0
    assert "MEMORY-AWARE" in result.upper()


def test_analysis_agent_creation():
    agent = AnalysisAgent()

    assert agent is not None


def test_analysis_agent():
    agent = AnalysisAgent()

    research = """
    Artificial intelligence is used in healthcare.
    AI can support diagnosis and medical analysis.
    """

    result = agent.analyze(research)

    assert result is not None
    assert len(result) > 0


def test_writing_agent_creation():
    agent = WritingAgent()

    assert agent is not None


def test_writing_agent():
    agent = WritingAgent()

    research = """
    OVERVIEW:
    Artificial intelligence is widely used in healthcare.

    MAJOR BENEFITS:
    AI can improve diagnosis and automation.

    MAJOR RISKS AND LIMITATIONS:
    AI may contain errors and requires validation.

    PRACTICAL IMPLICATIONS:
    Healthcare organizations can use AI to support professionals.

    CHALLENGES:
    Data quality and privacy are important challenges.

    CURRENT TRENDS:
    Generative AI and medical AI are growing areas.

    CONCLUSION:
    AI can support healthcare when implemented responsibly.
    """

    analysis = """
    AI provides benefits in healthcare but requires
    validation, security and responsible implementation.
    """

    result = agent.write(
        research,
        analysis
    )

    assert result is not None
    assert len(result) > 0

    output = result.lower()

    assert "introduction" in output
    assert "research summary" in output
    assert "key benefits" in output
    assert "risks and limitations" in output
    assert "practical applications" in output
    assert "challenges" in output
    assert "conclusion" in output


def test_validator_creation():
    agent = ValidatorAgent()

    assert agent is not None


def test_validator_pass():
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

    assert "PASS" in result


def test_validator_fail_empty():
    agent = ValidatorAgent()

    result = agent.validate(
        "test request",
        ""
    )

    assert "FAIL" in result


def test_validator_fail_short():
    agent = ValidatorAgent()

    result = agent.validate(
        "test request",
        "Very short answer."
    )

    assert "FAIL" in result


def test_validator_missing_sections():
    agent = ValidatorAgent()

    result = agent.validate(
        "test request",
        "This is an incomplete answer."
    )

    assert "FAIL" in result
    assert "Missing sections" in result


def test_validator_error_phrase():
    agent = ValidatorAgent()

    result = agent.validate(
        "test request",
        "An error occurred while generating this response."
    )

    assert "FAIL" in result


def test_tool_agent():
    agent = ToolAgent()

    result = agent.calculator(
        "25 * 40 + 100"
    )

    assert result == "1100"


def test_tool_agent_text_analysis():
    agent = ToolAgent()

    result = agent.text_analysis(
        "Hello world. This is testing."
    )

    assert result is not None

    result_text = str(result).lower()

    assert "characters" in result_text
    assert "words" in result_text
    assert "sentences" in result_text