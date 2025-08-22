import sys
import os
import pytest

# Permet d'importer 'server' même si on lance le test depuis /tests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import app, clubs, competitions


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_cannot_book_more_than_12_places(client):
    # On prend le premier club et la première compétition
    test_club = clubs[0]
    test_competition = competitions[0]

    # Sauvegarde de l'état initial
    initial_places = int(test_competition['numberOfPlaces'])
    initial_points = int(test_club['points'])

    # Tentative de réservation de 13 places
    response = client.post('/purchasePlaces', data={
        'competition': test_competition['name'],
        'club': test_club['name'],
        'places': 13
    }, follow_redirects=True)

    # Statut HTTP attendu (par exemple 400 si tu l'as défini pour erreur)
    assert response.status_code == 400, "Le serveur devrait retourner un code 400 en cas de dépassement de limite"

    # Message d'erreur attendu dans la réponse
    assert b"Error: You cannot book more than 12 places" in response.data
    

    # Vérifier qu'aucune place n'a été déduite
    assert int(test_competition['numberOfPlaces']) == initial_places
    assert int(test_club['points']) == initial_points
