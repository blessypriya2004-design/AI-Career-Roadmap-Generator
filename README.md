# PathPilot – AI Career Roadmap Generator

PathPilot is an AI-powered career guidance web application built using Python, Flask, HTML, CSS, and JavaScript. It helps users identify skill gaps and generate personalized career learning roadmaps based on their education, current skills, experience, and target job role.

## Features

- Personalized career guidance for different job roles.
- Skill gap identification.
- Career knowledge retrieval using RAG.
- AI-generated guidance using Ollama and Llama 3.2.
- Learning resources and beginner project suggestions.
- Step-by-step learning roadmap.
- Responsive web interface.
- Flask-based REST API.

## Supported Career Roles

- Python Full Stack Developer
- Frontend Developer
- Data Analyst
- Machine Learning Engineer

## Technology Stack

**Frontend**
- HTML5
- CSS3
- JavaScript

**Backend**
- Python
- Flask

**RAG (Retrieval-Augmented Generation)**
- Sentence Transformers
- FAISS
- Career knowledge documents

**LLM**
- Ollama
- Llama 3.2 (3B)

## How It Works

1. The user enters their education, skills, experience, and target career role.
2. The Flask backend processes the user information.
3. The RAG system retrieves relevant career information from the career knowledge documents using FAISS and Sentence Transformers.
4. The retrieved context is passed to the Llama 3.2 model through Ollama.
5. The LLM generates personalized career guidance and a learning roadmap.
6. The result is displayed on the web application.

## Project Structure

```text
AI-Career-Roadmap-Generator/
│
├── app.py
├── rag.py
├── script.js
├── style.css
├── index.html
├── frontend.html
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
└── career_docs/
    └── career_knowledge.txt
```

## Requirements

- Python 3.10 or newer
- Ollama
- Llama 3.2 (3B) model

## Installation and Setup (Windows)

### 1. Clone the repository

```powershell
git clone https://github.com/blessypriya2004-design/AI-Career-Roadmap-Generator.git
```

### 2. Open the project folder

```powershell
cd AI-Career-Roadmap-Generator
```

If the repository contains a nested project folder, open the inner folder containing `app.py` and `requirements.txt`.

### 3. Create a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 4. Install Python dependencies

```powershell
pip install -r requirements.txt
```

### 5. Install and download the Ollama model

Install Ollama from:

https://ollama.com/download/windows

Then run:

```powershell
ollama pull llama3.2:3b
```

### 6. Start the application

Make sure Ollama is running, then execute:

```powershell
python app.py
```

### 7. Open the application

Visit:

http://127.0.0.1:5000

## API

`POST /api/roadmap`

Accepts user career information and returns a personalized career roadmap with AI-generated guidance.

## Important Notes

- Ollama runs the Llama 3.2 model locally.
- No OpenAI API credits are required for the current Ollama-based implementation.
- The Sentence Transformers embedding model may download automatically during the first run.
- AI responses depend on the retrieved career documents and the local LLM.
- The application requires Ollama and the downloaded model to be available when generating AI guidance.

## Future Enhancements

- User authentication and profile management.
- Database integration.
- More career knowledge documents.
- Improved roadmap personalization.
- Additional AI-powered career recommendations.

## Author

Blessy Priya
Updated project documentation.
My project is successfully uploaded to GitHub.


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
