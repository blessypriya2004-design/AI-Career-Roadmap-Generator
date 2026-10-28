
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory(".", "frontend.html")

@app.route("/<path:filename>")
def files(filename):
    return send_from_directory(".", filename)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}

    goal = data.get("goal", "your career").strip()
    skills = data.get("skills", "").strip()
    level = data.get("level", "Beginner").strip()

    roadmap = {
        "career_goal": goal,
        "current_level": level,
        "current_skills": skills,
        "skill_match": "Needs assessment",
        "steps": [
            {
                "week": "Week 1",
                "title": "Learn Python basics",
                "tasks": [
                    "Learn variables and data types",
                    "Practice if/else and loops",
                    "Solve 5 beginner coding problems"
                ]
            },
            {
                "week": "Week 2",
                "title": "Build programming skills",
                "tasks": [
                    "Learn functions and lists",
                    "Practice dictionaries and strings",
                    "Build a small Python project"
                ]
            },
            {
                "week": "Week 3",
                "title": "Learn web development",
                "tasks": [
                    "Learn HTML and CSS basics",
                    "Understand Flask routes",
                    "Build a simple web page"
                ]
            },
            {
                "week": "Week 4",
                "title": "Build a portfolio project",
                "tasks": [
                    "Create a Python project",
                    "Upload your project to GitHub",
                    "Prepare a resume and practice interview questions"
                ]
            }
        ]
    }

    return jsonify({
        "success": True,
        "message": "Career roadmap generated successfully!",
        "roadmap": roadmap
    })

if __name__ == "__main__":
    app.run()
