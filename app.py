
import streamlit as st
import ollama
from pydantic import BaseModel, Field

MODEL = "llama3.2:1b"


class ProjectInput(BaseModel):
    idea: str = Field(min_length=10, max_length=2000)
    team_size: int = Field(ge=1, le=20)
    duration_weeks: int = Field(ge=1, le=52)
    skill_level: str


def ask_agent(role: str, instructions: str, context: str) -> str:
    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": f"You are the {role}. Follow these instructions: "
                f"{instructions}. Be practical, specific, and concise."
            },
            {
                "role": "user",
                "content": context
            },
        ],
    )
    return response.message.content


st.set_page_config(
    page_title="Project Planner",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 Multi-Agent Project Planner")
st.caption("Two AI agents. One coordinated project roadmap.")

with st.form("project_form"):
    idea = st.text_area(
        "What do you want to build?",
        placeholder="Example: An e-commerce website for a clothing business...",
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        team_size = st.number_input(
            "Team size", min_value=1, max_value=20, value=3
        )

    with col2:
        duration = st.number_input(
            "Duration (weeks)", min_value=1, max_value=52, value=8
        )

    with col3:
        skill = st.selectbox(
            "Team experience",
            ["Beginner", "Intermediate", "Advanced"],
        )

    submitted = st.form_submit_button(
        "Generate project roadmap",
        type="primary",
    )

if submitted:
    try:
        project = ProjectInput(
            idea=idea.strip(),
            team_size=int(team_size),
            duration_weeks=int(duration),
            skill_level=skill,
        )

        context = (
            f"Project idea: {project.idea}\n"
            f"Team size: {project.team_size}\n"
            f"Timeline: {project.duration_weeks} weeks\n"
            f"Experience: {project.skill_level}"
        )

        with st.spinner("Agent 1: Designing the architecture..."):
            architecture = ask_agent(
                "Software Architect",
                (
                    "Design a feasible software architecture. "
                    "Recommend a tech stack, main components, "
                    "database schema where relevant, and technical risks. "
                    "Respect the team's experience and timeline."
                ),
                context,
            )

        with st.spinner("Agent 2: Planning the project..."):
            schedule = ask_agent(
                "Project Manager",
                (
                    "Create a week-by-week project plan with tasks, "
                    "deliverables, dependencies, and risks. "
                    "Use the architect's proposal. Fit the specified "
                    "team size and deadline. Do not invent completed work."
                ),
                f"{context}\n\nArchitect's proposal:\n{architecture}",
            )

        st.success("Both agents completed their plans.")

        tab1, tab2 = st.tabs(
            ["🏗️ Software Architecture", "📅 Project Timeline"]
        )

        with tab1:
            st.markdown(architecture)

        with tab2:
            st.markdown(schedule)

        st.download_button(
            "Download project plan",
            data=(
                f"# Project Plan\n\n## Project\n{project.idea}\n\n"
                f"## Software Architecture\n{architecture}\n\n"
                f"## Project Timeline\n{schedule}\n"
            ),
            file_name="project_plan.md",
            mime="text/markdown",
        )

    except Exception as exc:
        st.error(
            "Something went wrong. Check that Ollama is running, "
            "the model is installed, and your project details are valid."
        )
        st.caption(f"Technical details: {exc}")
