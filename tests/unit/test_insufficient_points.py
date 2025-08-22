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
    """Test simplifié pour points insuffisants"""
    club_name = "Iron Temple"  # 4 points
    initial_points = int(next(c['points'] for c in clubs if c['name'] == club_name))
    
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': club_name,
        'places': '5'  # Plus que les 4 points disponibles
    }, follow_redirects=True)
    
    # Vérifications essentielles seulement
    assert b"points" in response.data or b"Error" in response.data
    assert int(next(c['points'] for c in clubs if c['name'] == club_name)) == initial_points
