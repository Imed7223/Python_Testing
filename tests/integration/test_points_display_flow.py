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

def test_points_display_public_access(client):  # <-- Ajoutez le paramètre client ici
    """Test accès public au tableau des points sans login"""
    response = client.get('/pointsDisplay')
    assert response.status_code == 200
    assert b'Simply Lift' in response.data
    assert b'13' in response.data  # Vérif données
