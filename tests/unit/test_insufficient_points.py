import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from server import app, clubs, competitions


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_insufficient_points(client):
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