from workflows.agent_workflow import build_workflow


def create_initial_state(request):
    return {
        "user_request": request,
        "route": "",
        "memory_context": "",
        "research": "",
        "analysis": "",
        "writing": "",
        "validation": "",
        "tool_result": "",
        "final_response": "",
        "memory_saved": False,
        "retry_count": 0,
    }


def test_research_workflow():
    workflow = build_workflow()

    state = create_initial_state(
        "research artificial intelligence in healthcare"
    )

    result = workflow.invoke(state)

    assert result is not None
    assert result["route"] == "research"

    assert result["final_response"] is not None
    assert len(result["final_response"]) > 0

    assert result["validation"] is not None
    assert len(result["validation"]) > 0

    assert result["memory_saved"] is True


def test_tool_workflow():
    workflow = build_workflow()

    state = create_initial_state(
        "calculate 25 * 40 + 100"
    )

    result = workflow.invoke(state)

    assert result is not None
    assert result["route"] == "tool"

    assert "1100" in str(result["tool_result"])

    assert "1100" in str(
        result["final_response"]
    )

    assert result["memory_saved"] is True


def test_direct_workflow():
    workflow = build_workflow()

    state = create_initial_state(
        "hello, how are you?"
    )

    result = workflow.invoke(state)

    assert result is not None
    assert result["route"] == "direct"

    assert result["final_response"] is not None
    assert len(result["final_response"]) > 0

    assert result["memory_saved"] is True