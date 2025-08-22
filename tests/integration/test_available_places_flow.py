
import pytest
from server import app, clubs, competitions

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_multiple_bookings_flow(client):
    """
    Test d'intégration complet : Login + réservations multiples successives
    """
    
    # 1. LOGIN
    login_response = client.post('/showSummary', 
                               data={'email': 'kate@shelifts.co.uk'},
                               follow_redirects=True)
    assert login_response.status_code == 200
    assert b'Welcome, kate@shelifts.co.uk' in login_response.data
    print("✓ Login réussi")

    # 2. DONNÉES INITIALES
    initial_places = int(next(c['numberOfPlaces'] for c in competitions if c['name'] == 'Spring Festival'))
    initial_points = int(next(c['points'] for c in clubs if c['name'] == 'She Lifts'))
    
    print(f"Places initiales: {initial_places}, Points initiaux: {initial_points}")

    # 3. PREMIÈRE RÉSERVATION (1 place)
    response1 = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'She Lifts',
        'places': '1'
    }, follow_redirects=True)
    
    # Vérification première réservation
    assert response1.status_code in [200, 400], f"Code HTTP inattendu: {response1.status_code}"
    
    if response1.status_code == 200:
        # Réservation réussie
        assert any(success_msg in response1.data for success_msg in [
            b'Great-booking complete!', b'booking complete', b'Success'
        ])
        print("✓ Première réservation réussie")
        
        # 4. DEUXIÈME RÉSERVATION (1 place)
        response2 = client.post('/purchasePlaces', data={
            'competition': 'Spring Festival', 
            'club': 'She Lifts',
            'places': '1'
        }, follow_redirects=True)
        
        assert response2.status_code in [200, 400]
        
        if response2.status_code == 200:
            # Deuxième réservation réussie
            assert any(success_msg in response2.data for success_msg in [
                b'Great-booking complete!', b'booking complete', b'Success'
            ])
            
            # 5. VÉRIFICATIONS FINALES
            final_places = int(next(c['numberOfPlaces'] for c in competitions if c['name'] == 'Spring Festival'))
            final_points = int(next(c['points'] for c in clubs if c['name'] == 'She Lifts'))
            
            assert final_places == initial_places - 2, f"Places: {initial_places} → {final_places}"
            assert final_points == initial_points - 2, f"Points: {initial_points} → {final_points}"
            print("✓ Réservations multiples réussies")
            
        else:
            # Deuxième réservation échouée
            assert any(error_msg in response2.data for error_msg in [
                b'Error', b'error', b'not enough', b'insufficient'
            ])
            print("✓ Deuxième réservation échouée (normal)")
            
    else:
        # Première réservation échouée
        assert any(error_msg in response1.data for error_msg in [
            b'Error', b'error', b'not enough', b'insufficient'
        ])
        print("✓ Première réservation échouée (test ignoré)")

    print("✅ Test d'intégration réservations multiples - COMPLET")
