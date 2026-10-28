
from flask import Flask, request, jsonify, send_from_directory
from cosine_similarity import cosine_similarity

app = Flask(__name__)


@app.route("/")
def home():
    return send_from_directory(".", "frontend.html")


@app.route("/<path:filename>")
def files(filename):
    return send_from_directory(".", filename)


def skills_to_vector(user_skills, required_skills):
    user_set = {
        skill.strip().lower()
        for skill in user_skills.split(",")
        if skill.strip()
    }

    required_set = {
        skill.strip().lower()
        for skill in required_skills.split(",")
        if skill.strip()
    }

    all_skills = sorted(user_set | required_set)

    user_vector = [1 if skill in user_set else 0 for skill in all_skills]
    required_vector = [
        1 if skill in required_set else 0 for skill in all_skills
    ]

    return user_vector, required_vector


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}

    name = data.get("name", "User").strip()
    goal = data.get("goal", "Python Developer").strip()
    skills = data.get("skills", "").strip()
    level = data.get("level", "Beginner").strip()

    # Basic example of required skills for each career
    career_skills = {
        "python developer": "python, git, flask, sql",
        "data analyst": "excel, sql, python, power bi",
        "web developer": "html, css, javascript, git",
    }

    required_skills = career_skills.get(
        goal.lower(),
        "python, problem solving, git"
    )

    user_vector, required_vector = skills_to_vector(
        skills, required_skills
    )

    if any(user_vector) and any(required_vector):
        similarity = cosine_similarity(user_vector, required_vector)
    else:
        similarity = 0.0

    roadmap = {
        "name": name,
        "career_goal": goal,
        "current_level": level,
        "current_skills": skills,
        "required_skills": required_skills,
        "skill_similarity_percent": round(similarity * 100, 2),
        "steps": [
            {
                "week": "Week 1",
                "title": "Learn the fundamentals",
                "tasks": [
                    f"Review the basics needed for {goal}",
                    "Practice core concepts every day",
                    "Write notes about what you learn"
                ]
            },
            {
                "week": "Week 2",
                "title": "Build core skills",
                "tasks": [
                    f"Practice these skills: {required_skills}",
                    "Complete beginner exercises",
                    "Save your practice work"
                ]
            },
            {
                "week": "Week 3",
                "title": "Create a small project",
                "tasks": [
                    f"Build a small project related to {goal}",
                    "Upload your code to GitHub",
                    "Test and improve your project"
                ]
            },
            {
                "week": "Week 4",
                "title": "Prepare your portfolio",
                "tasks": [
                    "Improve your project README",
                    "Prepare a resume listing your skills",
                    "Practice career-related interview questions"
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
