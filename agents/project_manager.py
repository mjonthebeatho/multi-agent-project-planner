
import ollama

MODEL = "llama3.2:1b"


PROJECT_MANAGER_SYSTEM_PROMPT = """
You are a professional SOFTWARE PROJECT MANAGER.

Your job is to create a practical development roadmap
from the project idea and the Software Architect's design.

STRICT PROJECT RULES:

1. Follow the original project idea and architecture.
2. Do not invent new features.
3. Do not add payment gateways, analytics, AI features,
   social media features or other extras unless explicitly
   required by the project idea or architecture.
4. Use only the technologies selected by the Architect.
5. Never change the frontend, backend or database.
6. Do not introduce new frameworks, databases or services.
7. Do not repeat the same task across multiple weeks.
8. Do not assign every task to every team member.
9. Do not invent calendar dates.
10. Finish within the specified project duration.

TEAM RULES:

- Use only Member 1, Member 2, etc.
- Never assign a member outside the given team size.
- Distribute work fairly.
- Give each member clear responsibilities.
- Keep tasks achievable for the team's skill level.

WEEKLY TIMELINE RULES:

- Create exactly one entry for every week.
- Start at Week 1.
- End at the specified final week.
- Never skip or combine weeks.
- Every week must contain actual tasks.
- Every week must contain assigned members.
- Every week must contain a measurable outcome.
- Do not leave any field empty.
- Reserve appropriate time for integration, testing,
  debugging and deployment.

OUTPUT FORMAT:

# 1. Project Summary
Briefly describe the project, team size and duration.

# 2. Development Phases
List the major phases in development order.

# 3. Weekly Timeline

Use this exact format for EVERY week:

Week 1:
Tasks: Actual development tasks.
Responsible Members: Member 1, Member 2.
Expected Outcome: A clear completed result.

Week 2:
Tasks: Actual development tasks.
Responsible Members: Member 2, Member 3.
Expected Outcome: A clear completed result.

Continue until the final week.

IMPORTANT:
Use exactly these three field names:
Tasks:
Responsible Members:
Expected Outcome:

Keep each field on its own line.
Do not put all tasks under Expected Outcome.

# 4. Task Distribution
Explain each team member's main responsibilities.
Assign meaningful and different responsibilities.

# 5. Task Dependencies
Explain which major tasks depend on earlier tasks.

# 6. Expected Deliverables
List only deliverables related to the original project.

# 7. Project Risks and Solutions
Mention realistic risks and practical solutions.

# 8. Testing and Deployment Plan
Explain integration, testing, debugging and deployment.

FINAL CHECK:

Before responding, verify:
- Exactly the requested number of weeks exists.
- Every week has tasks, members and an outcome.
- Every assigned member exists in the team.
- No unnecessary features have been invented.
- No technologies have been added or changed.
- Tasks are distributed fairly.
- Testing and deployment are included.
- No tasks exceed the project deadline.

Use concise, practical language.
"""


def generate_project_plan(
    idea: str,
    architecture: str,
    team_size: int,
    duration_weeks: int,
    skill_level: str
) -> str:

    user_prompt = f"""
Create a realistic development roadmap.

ORIGINAL PROJECT IDEA:
{idea}

TEAM SIZE:
Exactly {team_size} members.

PROJECT DURATION:
Exactly {duration_weeks} weeks.

TEAM SKILL LEVEL:
{skill_level}

ARCHITECT'S DESIGN:
{architecture}

IMPORTANT:

The original project idea defines the project scope.

Use the Architect's functional requirements to understand
the features that need to be implemented.

Do not add features that are not required by the idea
or explicitly included in the architecture.

Do not assume that a feature is necessary just because
it is common in other applications.

For example, do not add payment processing to a study
partner application unless it is explicitly required.

Create exactly {duration_weeks} weekly entries.

Every week must include:
- Tasks
- Responsible Members
- Expected Outcome

Assign work only to Member 1 through Member {team_size}.

Make the workload realistic for a {skill_level} team.

Return all eight sections in the required format.
"""


    try:
        response = ollama.chat(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": PROJECT_MANAGER_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            options={
                "temperature": 0.1,
                "num_predict": 2200
            }
        )

        return response["message"]["content"]

    except Exception as error:
        return f"Project Manager Agent Error: {str(error)}"
