from workflows.agent_workflow import supervisor_node


def create_state(user_request):
    return {
        "user_request": user_request,
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


def test_research_route():
    state = create_state(
        "research artificial intelligence in healthcare"
    )

    result = supervisor_node(state)

    assert result["route"] == "research"


def test_tool_route():
    state = create_state(
        "calculate 25 * 40 + 100"
    )

    result = supervisor_node(state)

    assert result["route"] == "tool"


def test_datetime_route():
    state = create_state(
        "what is the current time"
    )

    result = supervisor_node(state)

    assert result["route"] == "tool"


def test_direct_route():
    state = create_state(
        "hello, how are you?"
    )

    result = supervisor_node(state)

    assert result["route"] == "direct"


def test_valid_route():
    requests = [
        "research artificial intelligence",
        "calculate 10 + 20",
        "hello there",
    ]

    valid_routes = {
        "research",
        "tool",
        "direct",
    }

    for request in requests:
        state = create_state(request)
        result = supervisor_node(state)

        assert result["route"] in valid_routes
        