import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pytest
from server import app, clubs

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_points_display_public_access(client):
    """Test complet d'accès public au tableau des points sans login"""
    
    # 1. ACCÈS DIRECT SANS AUTHENTIFICATION
    response = client.get('/pointsDisplay')
    assert response.status_code == 200
    print("✓ Page accessible sans authentification")
    
    # 2. VÉRIFICATION TITRE ET STRUCTURE
    assert b"Clubs Points" in response.data
    assert b"<table>" in response.data
    assert b"<th>Club</th>" in response.data
    assert b"<th>Points</th>" in response.data
    print("✓ Structure HTML correcte")
    
    # 3. VÉRIFICATION DE TOUS LES CLUBS
    expected_clubs = ["Simply Lift", "Iron Temple", "She Lifts"]
    expected_points = ["13", "4", "12"]
    
    for club_name, points in zip(expected_clubs, expected_points):
        assert club_name.encode() in response.data, f"Club {club_name} non trouvé"
        assert points.encode() in response.data, f"Points {points} pour {club_name} non trouvés"
    print("✓ Tous les clubs et points affichés")
    
    # 4. VÉRIFICATION FORMAT DES DONNÉES
    # Vérifier que les données sont dans un tableau structuré
    assert b"<td>Simply Lift</td>" in response.data
    assert b"<td>13</td>" in response.data
    assert b"<td>Iron Temple</td>" in response.data  
    assert b"<td>4</td>" in response.data
    assert b"<td>She Lifts</td>" in response.data
    assert b"<td>12</td>" in response.data
    print("✓ Formatage des données correct")
    
    # 5. VÉRIFICATION LIEN DE RETOUR
    assert b'Back to login' in response.data or b'href="/"' in response.data
    print("✓ Lien de navigation présent")
    
    # 6. VÉRIFICATION ABSENCE D'ÉLÉMENTS PRIVÉS
    # La page ne doit pas contenir d'éléments nécessitant une connexion
    private_elements = [
        b"Book Places",
        b"Purchase",
        b"Logout",
        b"Welcome,"
    ]
    
    for private_element in private_elements:
        assert private_element not in response.data, f"Élément privé {private_element} trouvé"
    print("✓ Aucun élément privé affiché")
    
    # 7. VÉRIFICATION PERFORMANCE (optionnel)
    import time
    start_time = time.time()
    response = client.get('/pointsDisplay')
    end_time = time.time()
    
    response_time = end_time - start_time
    assert response_time < 2.0, f"Temps de réponse trop long: {response_time:.2f}s"
    print(f"✓ Temps de réponse acceptable: {response_time:.2f}s")
    
    print("✅ Test d'intégration tableau des points - COMPLET")
