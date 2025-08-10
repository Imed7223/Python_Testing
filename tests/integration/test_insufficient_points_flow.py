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

def test_points_update_insufficient_points(client):
    """Test intégration complet - points non déduits quand réservation impossible"""
    # 1. Setup - données de test
    TEST_CLUB = "Iron Temple"  # Doit avoir 4 points dans clubs.json
    TEST_COMPETITION = "Spring Festival"
    PLACES_REQUIRED = 5  # > points disponibles
    
    # 2. Pré-test - vérification données
    club = next(c for c in clubs if c['name'] == TEST_CLUB)
    initial_points = int(club['points'])
    assert initial_points < PLACES_REQUIRED, "Configuration incorrecte pour le test"

    # 3. Execution - 2 requêtes simulées
    # a. Login (si nécessaire)
    client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    
    # b. Tentative réservation
    response = client.post('/purchasePlaces',
                         data={
                             'competition': TEST_COMPETITION,
                             'club': TEST_CLUB,
                             'places': str(PLACES_REQUIRED)
                         },
                         follow_redirects=True)

    # 4. Vérifications
    # a. Message d'erreur
    assert b"Your club doesn't have enough points" in response.data or \
           b"doesn&#39;t have enough points" in response.data
    
    # b. Code statut (200 car follow_redirects=True)
    assert response.status_code == 400
    
    # c. Points inchangés
    updated_club = next(c for c in clubs if c['name'] == TEST_CLUB)
    assert int(updated_club['points']) == initial_points, \
        f"Points modifiés incorrectement (avant: {initial_points}, après: {updated_club['points']})"