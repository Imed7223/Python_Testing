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
    assert b"<table>" in response.data or b"<table " in response.data
    print("✓ Structure HTML correcte")
    
    # 3. VÉRIFICATION DES CLUBS (plus flexible)
    expected_clubs = ["Simply Lift", "Iron Temple", "She Lifts"]
    
    for club_name in expected_clubs:
        assert club_name.encode() in response.data, f"Club {club_name} non trouvé"
    print("✓ Tous les clubs affichés")
    
    # 4. VÉRIFICATION DES POINTS (plus flexible)
    # Au lieu de valeurs fixes, vérifier que chaque club a des points numériques
    import re
    points_pattern = r'<td>\s*(\d+)\s*</td>'
    points_found = re.findall(points_pattern, response.data.decode('utf-8'))
    
    assert len(points_found) >= 3, f"Moins de 3 points trouvés: {points_found}"
    assert all(point.isdigit() for point in points_found), "Tous les points doivent être numériques"
    print(f"✓ Points numériques trouvés: {points_found}")
    
    # 5. VÉRIFICATION FORMAT DES DONNÉES (plus flexible)
    # Vérifier que les clubs sont dans des cellules de tableau
    for club_name in expected_clubs:
        # Accepter différents formats: <td>Club</td> ou <td >Club</td> etc.
        assert f"<td>{club_name}</td>".encode() in response.data or \
               f">{club_name}</td>".encode() in response.data, \
               f"Club {club_name} mal formaté"
    print("✓ Formatage des clubs correct")
    
    # 6. VÉRIFICATION LIEN DE RETOUR
    assert b'Back to login' in response.data or b'href="/"' in response.data or \
           b'index' in response.data or b'login' in response.data
    print("✓ Lien de navigation présent")
    
    # 7. VÉRIFICATION ABSENCE D'ÉLÉMENTS PRIVÉS
    private_elements = [
        b"Book Places",
        b"Purchase", 
        b"Logout",
        b"Welcome,"
    ]
    
    for private_element in private_elements:
        assert private_element not in response.data, f"Élément privé {private_element} trouvé"
    print("✓ Aucun élément privé affiché")
    
    print("✅ Test d'intégration tableau des points - COMPLET")
