from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
ROOT = Path(__file__).resolve().parent
FRONTEND = ROOT / 'frontend'
app = Flask(__name__)

ROLE_DATA = {
    'Python Full Stack Developer': {
        'required': ['Python', 'HTML', 'CSS', 'JavaScript', 'SQL', 'Flask', 'REST API', 'Git'],
        'weeks': [
            ('Python revision', 'Revise functions, collections, OOP and exceptions.', 'Build a command-line task manager.'),
            ('HTML and CSS', 'Practise semantic HTML, forms, Flexbox, Grid and responsive design.', 'Build a responsive portfolio page.'),
            ('JavaScript', 'Learn DOM, events, arrays, objects and fetch().', 'Build an interactive expense tracker.'),
            ('SQL and MySQL', 'Practise tables, keys, joins, grouping and CRUD queries.', 'Create an inventory database.'),
            ('Flask and REST APIs', 'Learn routes, JSON requests, responses and validation.', 'Build a Flask CRUD API.'),
            ('Integration and Git', 'Connect frontend and backend; practise Git commits.', 'Publish a full-stack mini project.')
        ]
    },
    'Frontend Developer': {
        'required': ['HTML', 'CSS', 'JavaScript', 'Git', 'Responsive Design', 'REST API'],
        'weeks': [
            ('HTML foundations', 'Practise semantic HTML, forms and accessibility.', 'Build a profile page.'),
            ('CSS and responsive design', 'Learn Flexbox, Grid and media queries.', 'Build a mobile-friendly landing page.'),
            ('JavaScript fundamentals', 'Practise functions, arrays, objects, events and DOM.', 'Build a quiz app.'),
            ('API integration', 'Use fetch(), JSON, loading states and error handling.', 'Build a data dashboard.'),
            ('Quality and Git', 'Practise validation, accessibility and GitHub.', 'Publish two polished projects.'),
            ('Portfolio preparation', 'Document projects and practise interview questions.', 'Publish a portfolio with project demos.')
        ]
    },
    'Data Analyst': {
        'required': ['Python', 'SQL', 'Excel', 'Data Visualization', 'Statistics'],
        'weeks': [
            ('Spreadsheets', 'Practise formulas, sorting, filtering and pivot tables.', 'Analyse a sample sales sheet.'),
            ('SQL', 'Learn SELECT, WHERE, JOIN and GROUP BY.', 'Answer business questions using SQL.'),
            ('Python for data', 'Practise Python and Pandas data handling.', 'Clean a sample dataset.'),
            ('Statistics', 'Review averages, distributions and correlation.', 'Summarise a dataset.'),
            ('Visualization', 'Create charts and explain findings.', 'Build a small analytics report.'),
            ('Portfolio', 'Document methods, assumptions and findings.', 'Publish an analysis project.')
        ]
    },
    'Machine Learning Engineer': {
        'required': ['Python', 'Statistics', 'Pandas', 'NumPy', 'Machine Learning', 'Model Evaluation', 'Git'],
        'weeks': [
            ('Python and data tools', 'Revise Python, NumPy and Pandas.', 'Explore and clean a dataset.'),
            ('Statistics', 'Study probability, correlation and train/test splits.', 'Summarise a dataset statistically.'),
            ('ML basics', 'Learn regression, classification and preprocessing.', 'Train a baseline model.'),
            ('Model evaluation', 'Practise metrics, validation and error analysis.', 'Compare two models.'),
            ('Project development', 'Build a reproducible training pipeline.', 'Create a prediction app.'),
            ('Deployment and portfolio', 'Learn model persistence, APIs and Git.', 'Publish a documented project.')
        ]
    }
}

ALIASES = {'js': 'JavaScript', 'javascript': 'JavaScript', 'html5': 'HTML', 'css3': 'CSS', 'mysql': 'SQL', 'api': 'REST API', 'apis': 'REST API', 'ml': 'Machine Learning', 'github': 'Git', 'data visualisation': 'Data Visualization', 'scikit-learn': 'Machine Learning'}

def create_roadmap(data):
    role = str(data.get('target_role', '')).strip()
    education = str(data.get('education', '')).strip()
    if role not in ROLE_DATA:
        raise ValueError('Please choose a supported target role.')
    if not education:
        raise ValueError('Please enter your education.')
    try:
        hours = int(data.get('hours_per_week', 7))
    except (TypeError, ValueError):
        raise ValueError('Study hours must be a number from 1 to 40.')
    if not 1 <= hours <= 40:
        raise ValueError('Study hours must be between 1 and 40.')
    raw = data.get('skills', '')
    parts = raw.split(',') if isinstance(raw, str) else raw if isinstance(raw, list) else []
    current = {ALIASES.get(str(x).strip().lower(), str(x).strip()) for x in parts if str(x).strip()}
    required = ROLE_DATA[role]['required']
    current_lower = {x.lower() for x in current}
    matched = [x for x in required if x.lower() in current_lower]
    gaps = [x for x in required if x.lower() not in current_lower]
    weeks = [{'week': i, 'title': item[0], 'focus': item[1], 'task': item[2], 'estimated_hours': hours} for i, item in enumerate(ROLE_DATA[role]['weeks'], 1)]
    recommendations = ([f'Start learning {gaps[0]} and practise it in a small project.'] if gaps else ['Your skills match this checklist; deepen them through practical projects.'])
    recommendations += ['Save your work in GitHub and write a clear README.', 'Compare this plan with real job descriptions and update it as you learn.']
    return {'target_role': role, 'education': education, 'experience': str(data.get('experience', 'Fresher')), 'skills_matched': matched, 'skill_gaps': gaps, 'skill_match_percentage': round(len(matched) / len(required) * 100), 'roadmap': weeks, 'recommendations': recommendations, 'note': 'This starter version uses predefined rules, not an AI model. The checklist score is not a measure of job readiness or a job guarantee.'}

@app.get('/')
def home():
    return send_from_directory(FRONTEND, 'index.html')

@app.get('/<path:filename>')
def assets(filename):
    if filename not in {'style.css', 'script.js'}:
        return jsonify({'error': 'Not found'}), 404
    return send_from_directory(FRONTEND, filename)

@app.get('/api/roles')
def roles():
    return jsonify({'roles': list(ROLE_DATA.keys())})

@app.post('/api/roadmap')
def roadmap():
    data = request.get_json(silent=True) or {}
    try:
        return jsonify(create_roadmap(data))
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

if __name__ == '__main__':
    app.run(debug=True)
