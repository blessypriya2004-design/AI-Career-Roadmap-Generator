# PathPilot — Career Roadmap Generator

A responsive career planning web application built with HTML, CSS, JavaScript, Python, and Flask. Users enter education, skills, target role, experience, and weekly study time to receive a skill checklist, gaps, a six-week plan, practice tasks, and recommendations.

## Features
- Four supported roles: Python Full Stack Developer, Frontend Developer, Data Analyst, and Machine Learning Engineer.
- Rule-based skill-gap checklist and role checklist percentage.
- Six-week learning plan with practical tasks.
- Download roadmap as a text file.
- Responsive UI and Flask JSON API.
- Basic automated tests.

## Technology
HTML5, CSS3, Vanilla JavaScript, Python 3.10+, Flask, pytest.

## Run on Windows
1. Install Python 3.10 or newer.
2. Open a terminal in the project root folder.
3. Create and activate a virtual environment:
   ```powershell
   py -m venv .venv
   .venv\Scripts\activate
   ```
4. Install Flask:
   ```powershell
   pip install -r backend/requirements.txt
   ```
5. Start the server:
   ```powershell
   python backend/app.py
   ```
6. Open `http://127.0.0.1:5000` in your browser.

## Run tests
```powershell
pip install pytest
pytest -q
```

## API
`GET /api/roles` returns supported roles. `POST /api/roadmap` accepts JSON fields: `education`, `target_role`, `experience`, `skills`, and `hours_per_week`.

## Important limitation
Despite the project name, this starter version does **not** call an external AI model or train a machine-learning model. It uses predefined role requirements and rules. The checklist percentage is not a measure of job readiness and does not guarantee employment. AI integration, database storage, login, and profile saving are not included yet.
