import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))
from app import app, create_roadmap

def test_roadmap_has_six_weeks():
    result = create_roadmap({'education':'B.Tech IT','target_role':'Python Full Stack Developer','skills':'Python, HTML, CSS, SQL','hours_per_week':7})
    assert len(result['roadmap']) == 6
    assert 'JavaScript' in result['skill_gaps']

def test_invalid_role_returns_400():
    response = app.test_client().post('/api/roadmap', json={'education':'B.Tech','target_role':'Unknown'})
    assert response.status_code == 400

def test_home_page_loads():
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert b'PathPilot' in response.data
