import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pytest
from server import app, clubs, competitions
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def reset_data():
    # Recharge les données JSON pour chaque test
    clubs[:] = json.load(open('clubs.json'))['clubs']
    competitions[:] = json.load(open('competitions.json'))['competitions']       


def test_points_deduction(client):
    """Test que les points sont bien déduits après réservation"""
    # Données de test
    club_name = "Simply Lift"
    competition_name = "Spring Festival"
    places_required = 2
    
    # Points initiaux
    initial_points = int(next(c['points'] for c in clubs if c['name'] == club_name))
    
    # Faire la requête de réservation
    response = client.post('/purchasePlaces', data={
        'competition': competition_name,
        'club': club_name,
        'places': str(places_required)
    })
    
    # Vérifications
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    
    # Vérifier la mise à jour des points
    updated_points = int(next(c['points'] for c in clubs if c['name'] == club_name))
    assert updated_points == initial_points - places_required


def test_points_update_insufficient_points(client):
    """Test que les points ne sont pas déduits si réservation impossible"""
    # Données de test
    club_name = "Iron Temple"  # 4 points initialement
    competition_name = "Spring Festival"
    places_required = 5  # Plus que les points disponibles
    
    # Points initiaux
    initial_points = int(next(c['points'] for c in clubs if c['name'] == club_name))
    
    # Faire la requête de réservation
    response = client.post('/purchasePlaces', data={
        'competition': competition_name,
        'club': club_name,
        'places': str(places_required)
    })
    
    # Vérifications
    assert response.status_code == 400
    # Vérifie soit la version encodée HTML soit décodée
    assert (b"Your club doesn't have enough points" in response.data or 
            b"Your club doesn&#39;t have enough points" in response.data)
    
    # Vérifier que les points n'ont pas changé
    current_points = int(next(c['points'] for c in clubs if c['name'] == club_name))
    assert current_points == initial_points