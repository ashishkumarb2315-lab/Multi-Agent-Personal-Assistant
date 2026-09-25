import sys
from pathlib import Path

import streamlit as st


# =========================================================
# PROJECT ROOT
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Multi-Agent Personal Assistant Swarm",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# HEADER
# =========================================================

st.title("🤖 Multi-Agent Personal Assistant Swarm")

st.markdown(
    """
### Intelligent Collaborative AI System

A multi-agent AI system that understands a user request,
routes it to specialized agents, uses memory and tools,
validates the result, and generates a unified response.
"""
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("🧠 AI Agents")

    st.markdown(
        """
        **🧠 Supervisor Agent**  
        Routes the user's request.

        **💾 Memory Agent**  
        Recalls and stores previous interactions.

        **🔎 Research Agent**  
        Performs structured research.

        **📊 Analysis Agent**  
        Analyzes research findings.

        **✍️ Writing Agent**  
        Generates the final response.

        **🔧 Tool Agent**  
        Performs calculations and tools.

        **✅ Validator Agent**  
        Checks response quality.
        """
    )

    st.divider()

    st.subheader("⚙️ Technology Stack")

    st.write("🐍 Python")
    st.write("🔗 LangGraph")
    st.write("🤖 Gemini")
    st.write("💾 SQLite")
    st.write("🎨 Streamlit")

    st.divider()

    st.subheader("📌 Project")

    st.write("B.Tech Final Year Project")
    st.write("Artificial Intelligence & Data Science")

    st.divider()

    st.caption(
        "Multi-Agent Personal Assistant Swarm"
    )


# =========================================================
# USER INPUT
# =========================================================

st.subheader("💬 Ask Your Personal Assistant")

user_request = st.text_area(
    "Enter your task",
    placeholder=(
        "Example:\n"
        "What is Artificial Intelligence? "
        "Explain its benefits, risks and applications."
    ),
    height=140
)


# =========================================================
# EXECUTE TASK
# =========================================================

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

        # -------------------------------------------------
        # IMPORTANT:
        # Import workflow only after the user clicks
        # Execute Task. This keeps Streamlit startup fast.
        # -------------------------------------------------

        from workflows.agent_workflow import build_workflow

        with st.spinner(
            "🤖 Multi-agent system is processing your request..."
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

                # Store result so it remains visible
                # during Streamlit reruns.

                st.session_state["result"] = result

            except Exception as error:

                st.error(
                    f"❌ An error occurred: {error}"
                )


# =========================================================
# RESULTS
# =========================================================

if "result" in st.session_state:

    result = st.session_state["result"]

    st.divider()

    st.header("📊 Execution Results")


    # =====================================================
    # METRICS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)


    # -----------------------------------------------------
    # ROUTE
    # -----------------------------------------------------

    with col1:

        route = result.get(
            "route",
            "unknown"
        )

        st.metric(
            "Selected Route",
            route.upper()
        )


    # -----------------------------------------------------
    # MEMORY
    # -----------------------------------------------------

    with col2:

        memory_saved = result.get(
            "memory_saved",
            False
        )

        st.metric(
            "Memory Saved",
            "YES" if memory_saved else "NO"
        )


    # -----------------------------------------------------
    # RETRIES
    # -----------------------------------------------------

    with col3:

        retry_count = result.get(
            "retry_count",
            0
        )

        st.metric(
            "Retry Count",
            retry_count
        )


    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    with col4:

        validation = result.get(
            "validation",
            ""
        )

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


    # =====================================================
    # FINAL RESPONSE
    # =====================================================

    st.divider()

    st.header("🤖 Final Response")

    final_response = result.get(
        "final_response",
        ""
    )

    if final_response:

        st.markdown(
            final_response
        )

    else:

        st.warning(
            "No final response was generated."
        )


    # =====================================================
    # AGENT EXECUTION DETAILS
    # =====================================================

    st.divider()

    st.header(
        "🔄 Agent Execution Details"
    )


    route = result.get(
        "route",
        ""
    )


    # =====================================================
    # DIRECT ROUTE
    # =====================================================

    if route == "direct":

        st.success(
            "🧠 Supervisor → "
            "💾 Memory → "
            "📝 Direct → "
            "💾 Memory"
        )


    # =====================================================
    # TOOL ROUTE
    # =====================================================

    elif route == "tool":

        st.success(
            "🧠 Supervisor → "
            "💾 Memory → "
            "🔧 Tool → "
            "💾 Memory"
        )

        st.subheader(
            "🔧 Tool Agent Output"
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
                "No tool output available."
            )


    # =====================================================
    # RESEARCH ROUTE
    # =====================================================

    elif route == "research":

        st.success(
            "🧠 Supervisor → "
            "💾 Memory → "
            "🔎 Research → "
            "📊 Analysis → "
            "✍️ Writing → "
            "✅ Validator → "
            "💾 Memory"
        )


        # -------------------------------------------------
        # RESEARCH AGENT
        # -------------------------------------------------

        with st.expander(
            "🔎 Research Agent Output",
            expanded=True
        ):

            research_output = result.get(
                "research",
                ""
            )

            if research_output:

                # Use st.text instead of st.markdown.
                # This preserves the agent's raw output
                # and prevents Markdown from displaying
                # strange "- * -" formatting.

                st.text(
                    research_output
                )

            else:

                st.info(
                    "No research output available."
                )


        # -------------------------------------------------
        # ANALYSIS AGENT
        # -------------------------------------------------

        with st.expander(
            "📊 Analysis Agent Output",
            expanded=True
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
                    "No analysis output available."
                )


        # -------------------------------------------------
        # WRITING AGENT
        # -------------------------------------------------

        with st.expander(
            "✍️ Writing Agent Output",
            expanded=True
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
                    "No writing output available."
                )


        # -------------------------------------------------
        # VALIDATOR AGENT
        # -------------------------------------------------

        with st.expander(
            "✅ Validator Agent Result",
            expanded=True
        ):

            validation_output = result.get(
                "validation",
                ""
            )

            if validation_output:

                if validation_output.startswith(
                    "PASS"
                ):

                    st.success(
                        validation_output
                    )

                else:

                    st.warning(
                        validation_output
                    )

            else:

                st.info(
                    "No validation result available."
                )


    # =====================================================
    # MEMORY
    # =====================================================

    st.divider()

    st.header("💾 Memory")


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
            "No relevant previous memories were found."
        )


    # =====================================================
    # REQUEST INFORMATION
    # =====================================================

    st.divider()

    st.subheader(
        "📋 Request Information"
    )

    st.write(
        f"**User Request:** {result.get('user_request', '')}"
    )

    st.write(
        f"**Route:** {result.get('route', '').upper()}"
    )

    st.write(
        f"**Retries:** {result.get('retry_count', 0)}"
    )

    st.write(
        f"**Memory Saved:** "
        f"{'Yes' if result.get('memory_saved') else 'No'}"
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🤖 Multi-Agent Personal Assistant Swarm | "
    "B.Tech AI & Data Science Final Year Project"
)