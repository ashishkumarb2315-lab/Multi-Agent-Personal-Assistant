import sys
from pathlib import Path

import streamlit as st


# ============================================================
# PROJECT SETUP
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Multi-Agent Personal Assistant Swarm",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        opacity: 0.75;
        margin-bottom: 25px;
    }

    .agent-card {
        padding: 15px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    '🤖 Multi-Agent Personal Assistant Swarm'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'An intelligent collaborative AI system for autonomous task '
    'planning, execution, validation and personalized assistance.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🧠 Agent Architecture")

    agents = [
        ("🧠", "Supervisor Agent"),
        ("💾", "Memory Agent"),
        ("🔎", "Research Agent"),
        ("📊", "Analysis Agent"),
        ("✍️", "Writing Agent"),
        ("🔧", "Tool Agent"),
        ("✅", "Validator Agent"),
    ]

    for icon, name in agents:
        st.write(
            f"{icon} **{name}**"
        )

    st.divider()

    st.header("⚙️ Technology")

    st.write("🐍 Python")
    st.write("🔗 LangGraph")
    st.write("🤖 Gemini")
    st.write("💾 SQLite")
    st.write("🎨 Streamlit")

    st.divider()

    st.header("📌 Project")

    st.write("B.Tech Final Year Project")
    st.write("Artificial Intelligence & Data Science")

    st.divider()

    st.caption(
        "Multi-Agent Personal Assistant Swarm"
    )


# ============================================================
# USER INPUT
# ============================================================

st.subheader(
    "💬 Ask Your Personal Assistant"
)

user_request = st.text_area(
    "Enter your task",
    placeholder=(
        "Examples:\n"
        "• What is Artificial Intelligence?\n"
        "• Calculate 25 * 40\n"
        "• Explain the benefits and risks of AI\n"
        "• Research cloud computing"
    ),
    height=140,
    label_visibility="collapsed"
)


# ============================================================
# EXECUTE TASK
# ============================================================

if st.button(
    "🚀 Execute Task",
    type="primary",
    use_container_width=True
):

    if not user_request.strip():

        st.warning(
            "⚠️ Please enter a task first."
        )

    else:

        from workflows.agent_workflow import build_workflow

        with st.spinner(
            "🤖 Multi-agent system is working..."
        ):

            try:

                workflow = build_workflow()

                initial_state = {
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
                    "retry_count": 0
                }

                result = workflow.invoke(
                    initial_state
                )

                st.session_state["result"] = result

            except Exception as error:

                st.error(
                    f"❌ An error occurred: {error}"
                )


# ============================================================
# DISPLAY RESULTS
# ============================================================

if "result" in st.session_state:

    result = st.session_state["result"]

    route = result.get(
        "route",
        "unknown"
    )

    memory_saved = result.get(
        "memory_saved",
        False
    )

    retry_count = result.get(
        "retry_count",
        0
    )

    validation = result.get(
        "validation",
        ""
    )


    # ========================================================
    # EXECUTION DASHBOARD
    # ========================================================

    st.divider()

    st.header(
        "📊 Execution Dashboard"
    )

    col1, col2, col3, col4 = st.columns(4)


    # --------------------------------------------------------
    # ROUTE
    # --------------------------------------------------------

    with col1:

        st.metric(
            "Selected Route",
            route.upper()
        )


    # --------------------------------------------------------
    # MEMORY
    # --------------------------------------------------------

    with col2:

        st.metric(
            "Memory",
            "SAVED"
            if memory_saved
            else "NOT SAVED"
        )


    # --------------------------------------------------------
    # RETRIES
    # --------------------------------------------------------

    with col3:

        st.metric(
            "Retries",
            retry_count
        )


    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    with col4:

        if validation.startswith("PASS"):

            validation_status = "PASS"

        elif validation:

            validation_status = "CHECK"

        else:

            validation_status = "N/A"

        st.metric(
            "Validation",
            validation_status
        )


    # ========================================================
    # AGENT EXECUTION TIMELINE
    # ========================================================

    st.divider()

    st.header(
        "🔄 Agent Execution Timeline"
    )


    if route == "research":

        timeline = [

            (
                "🧠",
                "Supervisor Agent",
                "Request routing"
            ),

            (
                "💾",
                "Memory Agent",
                "Context retrieval"
            ),

            (
                "🔎",
                "Research Agent",
                "Information research"
            ),

            (
                "📊",
                "Analysis Agent",
                "Research analysis"
            ),

            (
                "✍️",
                "Writing Agent",
                "Response generation"
            ),

            (
                "✅",
                "Validator Agent",
                "Quality validation"
            ),

            (
                "💾",
                "Memory Agent",
                "Interaction storage"
            )
        ]

    elif route == "tool":

        timeline = [

            (
                "🧠",
                "Supervisor Agent",
                "Request routing"
            ),

            (
                "💾",
                "Memory Agent",
                "Context retrieval"
            ),

            (
                "🔧",
                "Tool Agent",
                "Tool execution"
            ),

            (
                "💾",
                "Memory Agent",
                "Interaction storage"
            )
        ]

    else:

        timeline = [

            (
                "🧠",
                "Supervisor Agent",
                "Request routing"
            ),

            (
                "💾",
                "Memory Agent",
                "Context retrieval"
            ),

            (
                "📝",
                "Direct Response",
                "Response generation"
            ),

            (
                "💾",
                "Memory Agent",
                "Interaction storage"
            )
        ]


    for index, (
        icon,
        agent,
        description
    ) in enumerate(
        timeline,
        start=1
    ):

        col1, col2, col3 = st.columns(
            [1, 3, 6]
        )

        with col1:

            st.success(
                f"{index}"
            )

        with col2:

            st.write(
                f"**{icon} {agent}**"
            )

        with col3:

            st.write(
                description
            )


    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    st.divider()

    st.header(
        "🤖 Final Response"
    )

    final_response = result.get(
        "final_response",
        ""
    )


    if final_response:

        # IMPORTANT:
        # Use st.text() instead of st.markdown().
        #
        # st.markdown() interprets # and ## as headings and
        # Streamlit adds heading anchors such as:
        #
        # [svg](http://localhost:8501/...)
        #
        # st.text() displays the generated response exactly
        # as returned by the Writing Agent.

        st.text(
            final_response
        )

    else:

        st.warning(
            "No final response was generated."
        )


    # ========================================================
    # RESEARCH ROUTE DETAILS
    # ========================================================

    if route == "research":

        st.divider()

        st.header(
            "🔬 Agent Outputs"
        )


        # ----------------------------------------------------
        # RESEARCH AGENT
        # ----------------------------------------------------

        with st.expander(
            "🔎 Research Agent Output",
            expanded=False
        ):

            research_output = result.get(
                "research",
                ""
            )

            if research_output:

                st.text(
                    research_output
                )

            else:

                st.info(
                    "No research output."
                )


        # ----------------------------------------------------
        # ANALYSIS AGENT
        # ----------------------------------------------------

        with st.expander(
            "📊 Analysis Agent Output",
            expanded=False
        ):

            analysis_output = result.get(
                "analysis",
                ""
            )

            if analysis_output:

                st.text(
                    analysis_output
                )

            else:

                st.info(
                    "No analysis output."
                )


        # ----------------------------------------------------
        # WRITING AGENT
        # ----------------------------------------------------

        with st.expander(
            "✍️ Writing Agent Output",
            expanded=False
        ):

            writing_output = result.get(
                "writing",
                ""
            )

            if writing_output:

                st.text(
                    writing_output
                )

            else:

                st.info(
                    "No writing output."
                )


        # ----------------------------------------------------
        # VALIDATOR AGENT
        # ----------------------------------------------------

        with st.expander(
            "✅ Validator Agent Result",
            expanded=True
        ):

            if validation.startswith("PASS"):

                st.success(
                    validation
                )

            elif validation:

                st.warning(
                    validation
                )

            else:

                st.info(
                    "No validation result."
                )


    # ========================================================
    # TOOL ROUTE DETAILS
    # ========================================================

    if route == "tool":

        st.divider()

        st.header(
            "🔧 Tool Execution"
        )

        tool_result = result.get(
            "tool_result",
            ""
        )

        if tool_result:

            st.code(
                str(tool_result),
                language="text"
            )

        else:

            st.info(
                "No tool output."
            )


    # ========================================================
    # MEMORY CONTEXT
    # ========================================================

    st.divider()

    st.header(
        "💾 Memory Context"
    )

    memory_context = result.get(
        "memory_context",
        ""
    )

    if memory_context:

        st.text(
            memory_context
        )

    else:

        st.info(
            "No relevant previous memories found."
        )


    # ========================================================
    # REQUEST INFORMATION
    # ========================================================

    st.divider()

    st.header(
        "📋 Request Information"
    )

    st.write(
        f"**Request:** "
        f"{result.get('user_request', '')}"
    )

    st.write(
        f"**Route:** "
        f"{route.upper()}"
    )

    st.write(
        f"**Retry Count:** "
        f"{retry_count}"
    )

    st.write(
        f"**Memory Saved:** "
        f"{'Yes' if memory_saved else 'No'}"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🤖 Multi-Agent Personal Assistant Swarm | "
    "B.Tech AI & Data Science Final Year Project"
)