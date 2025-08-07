import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pytest
from server import app, clubs

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_points_display_route(client):
    """Test que la route /pointsDisplay renvoie le bon template avec les données"""
    response = client.get('/pointsDisplay')
    assert response.status_code == 200
    assert b"Clubs Points" in response.data
    
    # Vérifier que tous les clubs sont affichés
    for club in clubs:
        assert club['name'].encode() in response.data
        assert club['points'].encode() in response.data

def test_points_display_content(client):
    """Test le contenu spécifique du tableau des points"""
    response = client.get('/pointsDisplay')
    
    # Vérifier le format du tableau
    assert b"<table>" in response.data
    assert b"<th>Club</th>" in response.data
    assert b"<th>Points</th>" in response.data
    
    # Vérifier un club spécifique
    test_club = clubs[0]
    assert f"<td>{test_club['name']}</td>".encode() in response.data
    assert f"<td>{test_club['points']}</td>".encode() in response.data
