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

def test_cannot_book_more_than_12_places(client):
    test_club = clubs[0]
    test_competition = competitions[0]

    # Sauvegarde des valeurs initiales
    initial_places = int(test_competition['numberOfPlaces'])
    initial_points = int(test_club['points'])

    # Simulation de réservation de 13 places (au-dessus de la limite)
    response = client.post('/purchasePlaces', data={
        'competition': test_competition['name'],
        'club': test_club['name'],
        'places': 13
    }, follow_redirects=True)

    # Vérifications
    assert response.status_code == 400
    assert b"Error: You cannot book more than 12 places" in response.data
    assert int(test_competition['numberOfPlaces']) == initial_places
    assert int(test_club['points']) == initial_points

