import pytest
from agents.tool_agent import ToolAgent


@pytest.fixture
def tool_agent():
    return ToolAgent()


def test_tool_agent_creation(tool_agent):
    assert tool_agent is not None


def test_calculator_addition(tool_agent):
    assert tool_agent.calculator("25 + 75") == "100"


def test_calculator_subtraction(tool_agent):
    assert tool_agent.calculator("100 - 25") == "75"


def test_calculator_multiplication(tool_agent):
    assert tool_agent.calculator("10 * 20") == "200"


def test_calculator_division(tool_agent):
    assert tool_agent.calculator("100 / 4") == "25.0"


def test_calculator_power(tool_agent):
    assert tool_agent.calculator("2 ** 5") == "32"


def test_calculator_complex_expression(tool_agent):
    assert tool_agent.calculator("25 * 40 + 100") == "1100"


def test_calculator_division_by_zero(tool_agent):
    result = tool_agent.calculator("10 / 0")

    assert result is not None
    assert "error" in str(result).lower()


def test_calculator_invalid_expression(tool_agent):
    result = tool_agent.calculator("hello + world")

    assert result is not None
    assert "error" in str(result).lower()


def test_datetime(tool_agent):
    result = tool_agent.get_datetime()

    assert result is not None
    assert len(result) > 0


def test_text_analysis(tool_agent):
    result = tool_agent.text_analysis(
        "Hello world. This is a test."
    )

    assert result is not None
    assert len(result) > 0

    result_text = str(result).lower()

    assert "characters" in result_text
    assert "words" in result_text
    assert "sentences" in result_text


def test_empty_text_analysis(tool_agent):
    result = tool_agent.text_analysis("")

    assert result is not None


def test_list_tools(tool_agent):
    tools = tool_agent.list_tools()

    assert "calculator" in tools
    assert "datetime" in tools
    assert "text_analysis" in tools


def test_execute_calculator(tool_agent):
    result = tool_agent.execute_tool(
        "calculator",
        "25 * 40 + 100"
    )

    assert result == "1100"


def test_execute_datetime(tool_agent):
    result = tool_agent.execute_tool("datetime")

    assert result is not None
    assert len(str(result)) > 0


def test_execute_text_analysis(tool_agent):
    result = tool_agent.execute_tool(
        "text_analysis",
        "Hello world."
    )

    assert result is not None


def test_invalid_tool(tool_agent):
    result = tool_agent.execute_tool("invalid_tool")

    assert result is not None
    assert "unknown tool" in str(result).lower()