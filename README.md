
# Multi-Agent Project Planner

An AI-powered project planning application that uses two specialized agents to generate software architecture and project timelines.

## Features

- AI Software Architect agent
- AI Project Manager agent
- Automated project roadmap generation
- Weekly milestones and task planning
- Downloadable project plans

## Tech Stack

- Python
- Ollama with a local language model
- Streamlit
- Pydantic
- Git and GitHub

## Prerequisites

- Python installed
- Ollama installed
- The `llama3.2:1b` model downloaded

## Setup

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

   `pip install -r requirements.txt`

4. Download the model:

   `ollama pull llama3.2:1b`

5. Run the application:

   `streamlit run app.py`

## Project Structure

- `app.py` — Web interface
- `agents/` — Specialized AI agents
- `services/` — Shared logic and agent coordination
- `requirements.txt` — Python dependencies
