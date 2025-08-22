import sys
import os
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import app, clubs, competitions

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_max_12_places_integration_flow(client):
    """
    Test d'intégration complet du flux: 
    Login -> Tentative réservation 15 places -> Vérification erreur
    """
    
    test_club = clubs[0]  # "Simply Lift"
    test_competition = competitions[0]  # "Spring Festival"
    
    initial_places = int(test_competition['numberOfPlaces'])
    initial_points = int(test_club['points'])

    # LOGIN
    login_response = client.post('/showSummary', 
                               data={'email': test_club['email']},
                               follow_redirects=True)
    assert login_response.status_code == 200

    # TENTATIVE RÉSERVATION 15 PLACES
    booking_data = {
        'competition': test_competition['name'],
        'club': test_club['name'],
        'places': '15'
    }
    
    purchase_response = client.post('/purchasePlaces', 
                                  data=booking_data,
                                  follow_redirects=True)
    
    # DEBUG
    print(f"Status: {purchase_response.status_code}")
    print(f"Content contains 'Error': {b'Error' in purchase_response.data}")
    print(f"Content contains 'Welcome': {b'Welcome' in purchase_response.data}")
    
    # VÉRIFICATIONS PRINCIPALES
    # 1. Le message d'erreur doit apparaître (plusieurs possibilités)
    error_patterns = [
        b"cannot book more than 12",
        b"maximum 12", 
        b"limit of 12",
        b"12 places",
        b"Error:",
        b"error:"
    ]
    
    has_error = any(pattern in purchase_response.data for pattern in error_patterns)
    assert has_error, "Aucun message d'erreur de limite détecté"
    
    # 2. Les données ne doivent PAS être modifiées
    current_points = int(test_club['points'])
    current_places = int(test_competition['numberOfPlaces'])
    
    assert current_points == initial_points, f"Points modifiés: {initial_points} -> {current_points}"
    assert current_places == initial_places, f"Places modifiées: {initial_places} -> {current_places}"
    
    # 3. Vérification que nous sommes sur la bonne page
    # Au lieu de chercher le nom du club, cherchez des éléments de la page welcome
    assert b'Welcome,' in purchase_response.data or b'Competitions:' in purchase_response.data
