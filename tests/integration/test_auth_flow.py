import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from server import app, clubs

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_complete_auth_integration_flow(client):
    """
    Test d'intégration complet du flux d'authentification
    """
    
    # 1. ACCÈS À LA PAGE D'ACCUEIL
    home_response = client.get('/')
    assert home_response.status_code == 200
    assert b'Welcome to the GUDLFT Registration Portal!' in home_response.data
    
    # Vérifications flexibles pour le formulaire de login
    login_form_patterns = [
        b'Enter your secretary email',
        b'Please enter your secretary email',
        b'secretary email',
        b'email',
        b'input type="email"',
        b'name="email"'
    ]
    
    has_login_form = any(pattern in home_response.data for pattern in login_form_patterns)
    assert has_login_form, "Formulaire de login non détecté sur la page d'accueil"
    print("✓ Page d'accueil accessible avec formulaire de login")

    # 2. CONNEXION AVEC EMAIL VALIDE
    valid_email = 'john@simplylift.co'
    login_response = client.post('/showSummary', 
                               data={'email': valid_email},
                               follow_redirects=True)
    
    assert login_response.status_code == 200
    assert b'Welcome, john@simplylift.co' in login_response.data
    assert b'Points available:' in login_response.data
    print("✓ Connexion réussie avec email valide")

    # 3. VÉRIFICATION TABLEAU DE BORD
    assert b'Spring Festival' in login_response.data or b'Fall Classic' in login_response.data
    print("✓ Données des compétitions affichées")

    # 4. DÉCONNEXION
    logout_response = client.get('/logout', follow_redirects=True)
    assert logout_response.status_code == 200
    assert b'Welcome to the GUDLFT Registration Portal!' in logout_response.data
    print("✓ Déconnexion réussie")

    # 5. TENTATIVE AVEC EMAIL INVALIDE
    invalid_email = 'nonexistent@club.com'
    failed_login_response = client.post('/showSummary',
                                      data={'email': invalid_email},
                                      follow_redirects=True)
    
    assert failed_login_response.status_code == 200
    
    # Vérifications flexibles pour le message d'erreur
    error_patterns = [
        b"Sorry, that email wasn't found",
        b"email wasn't found", 
        b"not found",
        b"invalid email",
        b"Sorry, that email wasn&#39;t found",
        b"error",
        b"Error"
    ]
    
    error_found = any(pattern in failed_login_response.data for pattern in error_patterns)
    assert error_found, "Message d'erreur pour email invalide non trouvé"
    print("✓ Erreur de connexion correctement gérée")

    print("✅ Test d'intégration flux d'authentification - COMPLET")
