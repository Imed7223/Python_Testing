import pytest
from datetime import datetime, timedelta
from server import app, clubs, competitions

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_booking_past_competition(client):
    # Création d'une compétition passée
    past_competition = {
        "name": "Past Competition Test",
        "date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
        "numberOfPlaces": "5"
    }
    competitions.append(past_competition)

    # Création d'un club fictif
    test_club = {
        "name": "Test Club",
        "points": "10",
        "email": "test@club.com"
    }
    clubs.append(test_club)

    # Appel de la route /book avec compétition passée
    response = client.get(f"/book/{past_competition['name']}/{test_club['name']}")

    # Vérification que le message d'erreur apparaît
    assert b"Cannot book places for past competitions." in response.data
    # Vérification que la page de réservation n'est pas affichée
    assert b"booking.html" not in response.data

    # Nettoyage pour ne pas polluer les autres tests
    competitions.remove(past_competition)
    clubs.remove(test_club)
