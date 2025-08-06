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

def test_login_with_valid_email(client):
    response = client.post('/showSummary', 
                         data={'email': 'simplylift@club.com'},
                         follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome' in response.data

def test_login_with_invalid_email(client):
    response = client.post('/showSummary',
                         data={'email': 'wrong@email.com'},
                         follow_redirects=True)
    assert response.status_code == 200
    assert b"Sorry, that email wasn&#39;t found." in response.data