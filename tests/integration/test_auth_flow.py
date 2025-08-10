import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_failed_login_flow(client):
    """Test flux complet de login invalide"""
    response = client.post('/showSummary', 
                         data={'email': 'wrong@email.com'},
                         follow_redirects=True)
    
    assert b"Sorry, that email wasn&#39;t found." in response.data
    assert b'Welcome to the GUDLFT Registration' in response.data
