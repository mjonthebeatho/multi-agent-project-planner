
import re

from agents.architect import generate_architecture
from agents.project_manager import generate_project_plan


# Recognised technologies and their name variations.
TECHNOLOGY_ALIASES = {
    "Python": [r"\bPython\b"],
    "Flask": [r"\bFlask\b"],
    "Django": [r"\bDjango\b"],
    "FastAPI": [r"\bFastAPI\b"],
    "Node.js": [r"\bNode\.?js\b", r"\bNodeJS\b"],
    "Express.js": [r"\bExpress(?:\.js)?\b"],
    "React": [r"\bReact\b"],
    "Angular": [r"\bAngular\b"],
    "Vue": [r"\bVue(?:\.js)?\b"],
    "MongoDB": [r"\bMongoDB\b"],
    "PostgreSQL": [r"\bPostgreSQL\b"],
    "MySQL": [r"\bMySQL\b"],
    "SQLite": [r"\bSQLite\b"],
    "Firebase": [r"\bFirebase\b"],
    "Supabase": [r"\bSupabase\b"],
    "SQLAlchemy": [r"\bSQLAlchemy\b"],
    "Passport.js": [r"\bPassport\.js\b"],
    "JWT": [r"\bJWT\b", r"\bJSON Web Token\b"],
    "Socket.IO": [r"\bSocket\.IO\b"],
    "Redis": [r"\bRedis\b"],
    "RabbitMQ": [r"\bRabbitMQ\b"],
    "Kafka": [r"\bKafka\b"],
}


def find_technologies(text: str) -> set:
    """Find recognised technologies in text."""

    found = set()

    for technology, patterns in TECHNOLOGY_ALIASES.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                found.add(technology)
                break

    return found


def validate_blueprint(
    architecture: str,
    project_plan: str,
    team_size: int,
    duration_weeks: int
) -> list:
    """Validate the generated architecture and project roadmap."""

    warnings = []

    # 1. Check agent failures.
    if not architecture or architecture.startswith(
        "Architect Agent Error:"
    ):
        return ["Architect failed to generate an architecture."]

    if not project_plan or project_plan.startswith(
        "Project Manager Agent Error:"
    ):
        return ["Project Manager failed to generate a project plan."]

    architecture_lower = architecture.lower()
    plan_lower = project_plan.lower()

    # 2. Check architecture sections.
    architecture_sections = [
        "project overview",
        "functional requirements",
        "non-functional requirements",
        "recommended technology stack",
        "system architecture",
        "database design",
        "api design",
        "security design"
    ]

    for section in architecture_sections:
        if section not in architecture_lower:
            warnings.append(
                f"Architect output is missing: {section.title()}."
            )

    # 3. Check project plan sections.
    planning_sections = [
        "project summary",
        "development phases",
        "weekly timeline",
        "task distribution",
        "task dependencies",
        "expected deliverables",
        "project risks",
        "testing and deployment plan"
    ]

    for section in planning_sections:
        if section not in plan_lower:
            warnings.append(
                f"Project Manager output is missing: {section.title()}."
            )

    # 4. Extract the weekly timeline.
    timeline_match = re.search(
        r"(?im)^#\s*3\.\s*Weekly Timeline\s*$([\s\S]*?)(?=^#\s*4\.|\Z)",
        project_plan
    )

    if not timeline_match:
        warnings.append("Could not identify the weekly timeline.")
        timeline = ""
    else:
        timeline = timeline_match.group(1)

    week_matches = list(re.finditer(
        r"(?im)^\s*Week\s+(\d+)\s*:\s*$",
        timeline
    ))

    detected_weeks = [
        int(match.group(1))
        for match in week_matches
    ]

    expected_weeks = list(range(1, duration_weeks + 1))

    # Check missing weeks.
    missing_weeks = sorted(
        set(expected_weeks) - set(detected_weeks)
    )

    if missing_weeks:
        warnings.append(
            "Timeline is missing weeks: "
            + ", ".join(map(str, missing_weeks))
            + "."
        )

    # Check extra weeks.
    extra_weeks = sorted(
        set(detected_weeks) - set(expected_weeks)
    )

    if extra_weeks:
        warnings.append(
            "Timeline contains weeks beyond the deadline: "
            + ", ".join(map(str, extra_weeks))
            + "."
        )

    # Check duplicate weeks.
    duplicates = sorted({
        week for week in detected_weeks
        if detected_weeks.count(week) > 1
    })

    if duplicates:
        warnings.append(
            "Duplicate weekly entries found: "
            + ", ".join(map(str, duplicates))
            + "."
        )

    # Check exact number and order of weekly entries.
    if detected_weeks != expected_weeks:
        warnings.append(
            "Weekly entries must appear exactly once, "
            "in order from Week 1 to Week "
            f"{duration_weeks}."
        )

    # 5. Validate each weekly entry.
    required_fields = [
        "Tasks",
        "Responsible Members",
        "Expected Outcome"
    ]

    weekly_member_numbers = set()

    for index, match in enumerate(week_matches):

        week_number = int(match.group(1))

        start = match.end()
        end = (
            week_matches[index + 1].start()
            if index + 1 < len(week_matches)
            else len(timeline)
        )

        week_content = timeline[start:end]

        for field in required_fields:

            field_pattern = (
                rf"(?ims)^\s*{re.escape(field)}\s*:\s*"
                rf"(.*?)"
                rf"(?=^\s*(?:Tasks|Responsible Members|Expected Outcome)\s*:|\Z)"
            )

            field_match = re.search(field_pattern, week_content)

            if not field_match:
                warnings.append(
                    f"Week {week_number} is missing the '{field}' field."
                )
                continue

            field_value = field_match.group(1).strip()

            if not field_value:
                warnings.append(
                    f"Week {week_number} has an empty '{field}' field."
                )

            # Collect members assigned specifically in weekly entries.
            if field == "Responsible Members":
                assigned_members = re.findall(
                    r"\bMember\s+(\d+)\b",
                    field_value,
                    re.IGNORECASE
                )

                if not assigned_members:
                    warnings.append(
                        f"Week {week_number} has no valid member assignments."
                    )

                weekly_member_numbers.update(
                    int(number) for number in assigned_members
                )

    # 6. Check team member assignments.
    member_numbers = re.findall(
        r"\bMember\s+(\d+)\b",
        project_plan,
        re.IGNORECASE
    )

    invalid_members = sorted({
        int(number)
        for number in member_numbers
        if int(number) < 1 or int(number) > team_size
    })

    if invalid_members:
        warnings.append(
            "Unavailable team members assigned: "
            + ", ".join(map(str, invalid_members))
            + "."
        )

    # Check that every team member appears in weekly assignments.
    for member in range(1, team_size + 1):
        if member not in weekly_member_numbers:
            warnings.append(
                f"Member {member} has no assignment in the weekly timeline."
            )

    # 7. Compare technologies between agents.
    architecture_technologies = find_technologies(architecture)
    plan_technologies = find_technologies(project_plan)

    unexpected_technologies = sorted(
        plan_technologies - architecture_technologies
    )

    if unexpected_technologies:
        warnings.append(
            "Project Manager introduced technologies not found "
            "in the Architect output: "
            + ", ".join(unexpected_technologies)
            + "."
        )

    return warnings


def generate_blueprint(
    idea: str,
    team_size: int,
    duration_weeks: int,
    skill_level: str
) -> dict:

    # STEP 1: Generate architecture.
    print("\n[1/3] Software Architect is working...")

    architecture = generate_architecture(
        idea=idea,
        team_size=team_size,
        duration_weeks=duration_weeks,
        skill_level=skill_level
    )

    if not architecture or architecture.startswith(
        "Architect Agent Error:"
    ):
        return {
            "success": False,
            "error": architecture or "Architect returned empty output.",
            "architecture": architecture or "",
            "project_plan": "",
            "warnings": []
        }

    # STEP 2: Generate project roadmap.
    print("\n[2/3] Project Manager is creating the roadmap...")

    project_plan = generate_project_plan(
        idea=idea,
        architecture=architecture,
        team_size=team_size,
        duration_weeks=duration_weeks,
        skill_level=skill_level
    )

    if not project_plan or project_plan.startswith(
        "Project Manager Agent Error:"
    ):
        return {
            "success": False,
            "error": project_plan or "Project Manager returned empty output.",
            "architecture": architecture,
            "project_plan": project_plan or "",
            "warnings": []
        }

    # STEP 3: Validate the blueprint.
    print("\n[3/3] Validating project blueprint...")

    warnings = validate_blueprint(
        architecture=architecture,
        project_plan=project_plan,
        team_size=team_size,
        duration_weeks=duration_weeks
    )

    success = len(warnings) == 0

    if success:
        print("\nBlueprint passed all validation checks.")
    else:
        print("\nBlueprint needs review:")

        for warning in warnings:
            print("-", warning)

    return {
        "success": success,
        "architecture": architecture,
        "project_plan": project_plan,
        "warnings": warnings
    }
