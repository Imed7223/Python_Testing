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


def test_complete_booking_flow(client):
    """Test complet : login -> sélection compétition -> réservation -> vérif points"""
    # Login
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert b'Welcome, john@simplylift.co' in response.data
    
    # Sélection compétition
    book_page = client.get('/book/Spring%20Festival/Simply%20Lift')
    assert b'Booking for Spring Festival' in book_page.data
    
    # Réservation
    purchase_response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '3'
    })
    assert b'Great-booking complete!' in purchase_response.data
    
    # Vérif déduction points
    club = next(c for c in clubs if c['name'] == 'Simply Lift')
    assert int(club['points']) == 10  # 13 - 3
