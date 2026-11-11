import os
import ollama
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv
from openai import OpenAI

from rag import create_knowledge_index, retrieve_context


# Load environment variables
ROOT = Path(__file__).resolve().parent
FRONTEND = ROOT

load_dotenv(ROOT / ".env")

# OpenAI API configuration
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

client = OpenAI(
    api_key=API_KEY,
    timeout=60.0,
    max_retries=2
) if API_KEY else None

app = Flask(__name__)


# ----------------------------------
# RAG KNOWLEDGE BASE
# ----------------------------------

rag_index = None
rag_chunks = []

def get_career_context(question):
    global rag_index, rag_chunks

    if rag_index is None:
        rag_index, rag_chunks = create_knowledge_index()

    return retrieve_context(question, rag_index, rag_chunks)


def generate_ai_response(question, context):

    prompt = f"""
You are PathPilot, a professional AI career guidance assistant.

Use the following retrieved career information:

{context}

User details:
{question}

Instructions:
1. Give personalized career guidance.
2. Identify missing skills.
3. Suggest learning resources and topics.
4. Recommend beginner projects.
5. Give a realistic learning sequence.
6. Use simple English.
7. Format with headings and bullet points.
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()


# ----------------------------------
# CAREER ROLE INFORMATION
# ----------------------------------

ROLE_DATA = {
    "Python Full Stack Developer": {
        "required": [
            "Python", "HTML", "CSS", "JavaScript",
            "SQL", "Flask", "REST API", "Git"
        ],
        "weeks": [
            ("Python revision",
             "Revise functions, collections, OOP and exceptions.",
             "Build a command-line task manager."),

            ("HTML and CSS",
             "Practise semantic HTML, forms, Flexbox, Grid and responsive design.",
             "Build a responsive portfolio page."),

            ("JavaScript",
             "Learn DOM, events, arrays, objects and fetch().",
             "Build an interactive expense tracker."),

            ("SQL and MySQL",
             "Practise tables, keys, joins, grouping and CRUD queries.",
             "Create an inventory database."),

            ("Flask and REST APIs",
             "Learn routes, JSON requests, responses and validation.",
             "Build a Flask CRUD API."),

            ("Integration and Git",
             "Connect frontend and backend; practise Git commits.",
             "Publish a full-stack mini project.")
        ]
    },

    "Frontend Developer": {
        "required": [
            "HTML", "CSS", "JavaScript",
            "Git", "Responsive Design", "REST API"
        ],
        "weeks": [
            ("HTML foundations",
             "Practise semantic HTML, forms and accessibility.",
             "Build a profile page."),

            ("CSS and responsive design",
             "Learn Flexbox, Grid and media queries.",
             "Build a mobile-friendly landing page."),

            ("JavaScript fundamentals",
             "Practise functions, arrays, objects, events and DOM.",
             "Build a quiz app."),

            ("API integration",
             "Use fetch(), JSON, loading states and error handling.",
             "Build a data dashboard."),

            ("Quality and Git",
             "Practise validation, accessibility and GitHub.",
             "Publish two polished projects."),

            ("Portfolio preparation",
             "Document projects and practise interview questions.",
             "Publish a portfolio with project demos.")
        ]
    },

    "Data Analyst": {
        "required": [
            "Python", "SQL", "Excel",
            "Data Visualization", "Statistics"
        ],
        "weeks": [
            ("Spreadsheets",
             "Practise formulas, sorting, filtering and pivot tables.",
             "Analyse a sample sales sheet."),

            ("SQL",
             "Learn SELECT, WHERE, JOIN and GROUP BY.",
             "Answer business questions using SQL."),

            ("Python for data",
             "Practise Python and Pandas data handling.",
             "Clean a sample dataset."),

            ("Statistics",
             "Review averages, distributions and correlation.",
             "Summarise a dataset."),

            ("Visualization",
             "Create charts and explain findings.",
             "Build a small analytics report."),

            ("Portfolio",
             "Document methods, assumptions and findings.",
             "Publish an analysis project.")
        ]
    },

    "Machine Learning Engineer": {
        "required": [
            "Python", "Statistics", "Pandas", "NumPy",
            "Machine Learning", "Model Evaluation", "Git"
        ],
        "weeks": [
            ("Python and data tools",
             "Revise Python, NumPy and Pandas.",
             "Explore and clean a dataset."),

            ("Statistics",
             "Study probability, correlation and train/test splits.",
             "Summarise a dataset statistically."),

            ("ML basics",
             "Learn regression, classification and preprocessing.",
             "Train a baseline model."),

            ("Model evaluation",
             "Practise metrics, validation and error analysis.",
             "Compare two models."),

            ("Project development",
             "Build a reproducible training pipeline.",
             "Create a prediction app."),

            ("Deployment and portfolio",
             "Learn model persistence, APIs and Git.",
             "Publish a documented project.")
        ]
    }
}


ALIASES = {
    "js": "JavaScript",
    "javascript": "JavaScript",
    "html5": "HTML",
    "css3": "CSS",
    "mysql": "SQL",
    "api": "REST API",
    "apis": "REST API",
    "ml": "Machine Learning",
    "github": "Git",
    "data visualisation": "Data Visualization",
    "scikit-learn": "Machine Learning"
}


# ----------------------------------
# RULE-BASED ROADMAP
# ----------------------------------

def create_roadmap(data):

    role = str(data.get("target_role", "")).strip()
    education = str(data.get("education", "")).strip()

    if role not in ROLE_DATA:
        raise ValueError("Please choose a supported target role.")

    if not education:
        raise ValueError("Please enter your education.")

    try:
        hours = int(data.get("hours_per_week", 7))
    except (TypeError, ValueError):
        raise ValueError("Study hours must be a number from 1 to 40.")

    if not 1 <= hours <= 40:
        raise ValueError("Study hours must be between 1 and 40.")

    raw = data.get("skills", "")

    parts = (
        raw.split(",")
        if isinstance(raw, str)
        else raw if isinstance(raw, list)
        else []
    )

    current = {
        ALIASES.get(str(x).strip().lower(), str(x).strip())
        for x in parts
        if str(x).strip()
    }

    required = ROLE_DATA[role]["required"]

    current_lower = {x.lower() for x in current}

    matched = [
        x for x in required
        if x.lower() in current_lower
    ]

    gaps = [
        x for x in required
        if x.lower() not in current_lower
    ]

    weeks = [
        {
            "week": i,
            "title": item[0],
            "focus": item[1],
            "task": item[2],
            "estimated_hours": hours
        }
        for i, item in enumerate(ROLE_DATA[role]["weeks"], 1)
    ]

    recommendations = (
        [
            f"Start learning {gaps[0]} and practise it in a small project."
        ]
        if gaps
        else [
            "Your skills match this checklist; deepen them through practical projects."
        ]
    )

    recommendations += [
        "Save your work in GitHub and write a clear README.",
        "Compare this plan with real job descriptions and update it as you learn."
    ]

    return {
        "target_role": role,
        "education": education,
        "experience": str(data.get("experience", "Fresher")),
        "skills_matched": matched,
        "skill_gaps": gaps,
        "skill_match_percentage": round(
            len(matched) / len(required) * 100
        ),
        "roadmap": weeks,
        "recommendations": recommendations,
        "note": "The roadmap uses predefined rules and AI-generated career guidance. The checklist score is not a measure of job readiness or a job guarantee."
    }


# ----------------------------------
# FLASK ROUTES
# ----------------------------------

@app.get("/")
def home():
    return send_from_directory(FRONTEND, "index.html")


@app.get("/<path:filename>")
def assets(filename):

    if filename not in {"style.css", "script.js"}:
        return jsonify({"error": "Not found"}), 404

    return send_from_directory(FRONTEND, filename)


@app.get("/api/roles")
def roles():
    return jsonify({
        "roles": list(ROLE_DATA.keys())
    })


@app.post("/api/roadmap")
def roadmap():

    data = request.get_json(silent=True) or {}

    try:
        result = create_roadmap(data)

        # Prepare a question using the user's career details
        question = (
            f"Target role: {result['target_role']}\n"
            f"Education: {result['education']}\n"
            f"Experience: {result['experience']}\n"
            f"Current skills: {data.get('skills', '')}\n"
            f"Missing skills: {', '.join(result['skill_gaps'])}"
        )
        # Retrieve relevant knowledge using RAG
        context = get_career_context(question)

        # Generate guidance using OpenAI GPT
        try:
            ai_guidance = generate_ai_response(question, context)
        except Exception:
            app.logger.exception("AI guidance generation failed")
            ai_guidance = (
                "AI guidance is temporarily unavailable. "
                "Please try again later. Your basic roadmap is available."
            )

        result["ai_guidance"] = ai_guidance

        return jsonify(result)

    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    except Exception:
        app.logger.exception("Roadmap generation failed")
        return jsonify({
            "error": "Unable to generate the roadmap. Please check the server configuration."
        }), 500


# ----------------------------------
# RUN APPLICATION
# ----------------------------------

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.getenv("PORT", 5000)),
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true"
    )
