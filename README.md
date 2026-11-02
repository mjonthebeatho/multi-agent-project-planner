# Multi-Agent Project Planner

An AI-powered application that transforms software project ideas into structured software architectures and development roadmaps.

The application uses two specialized AI agents — an AI Software Architect and an AI Project Manager — to generate a coordinated project plan based on the user's requirements.

## Features

- **AI Software Architect:** Generates software architecture, functional and non-functional requirements, technology stack recommendations, database design, and security considerations.
- **AI Project Manager:** Creates a structured development roadmap based on the generated architecture.
- **Automated Roadmap Generation:** Generates weekly milestones, task assignments, dependencies, and expected deliverables.
- **Output Validation:** Checks generated plans for missing sections, timeline inconsistencies, and other structural issues.
- **Downloadable Project Plan:** Allows users to download the generated project plan.
- **Local AI Processing:** Uses Ollama and a locally hosted language model without requiring a paid API key.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Ollama | Local language model execution |
| Llama 3.2 (1B) | Language model |
| Streamlit | Web application interface |
| Git & GitHub | Version control |

## How It Works

1. The user enters a project idea, team size, project duration, and team experience level.
2. The AI Software Architect generates the technical architecture.
3. The AI Project Manager uses the architecture to create a development roadmap.
4. The validation module checks the generated outputs.
5. The application displays the architecture and project timeline and provides an option to download the project plan.

## Project Structure

```text
multi-agent-project-planner/
│
├── agents/
│   ├── architect.py
│   └── project_manager.py
│
├── services/
│   └── planner.py
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Ollama installed
- Git installed

### 1. Clone the Repository

```bash
git clone https://github.com/mjonthebeatho/multi-agent-project-planner.git
cd multi-agent-project-planner
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the AI Model

```bash
ollama pull llama3.2:1b
```

Ensure Ollama is running before starting the application.

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser.

## Future Improvements

- Improve agent collaboration and output quality.
- Introduce additional specialized agents.
- Enhance roadmap visualization.
- Add support for multiple export formats.
- Improve technology stack recommendations.

## Project Information

This project explores the use of multi-agent AI systems for automated software architecture design and project planning.

**Built using Python, Streamlit, and Ollama.**
