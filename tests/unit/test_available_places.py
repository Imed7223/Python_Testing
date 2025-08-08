import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch
from server import app
from flask import Flask,render_template,request,redirect,flash,url_for
import pytest
from server import app, clubs, competitions


# Données de test simulées
mock_clubs = [
    {"name": "Test Club", "email": "test@example.com", "points": "30"}
]

mock_competitions = [
    {"name": "Test Competition", "date": "2025-12-31 10:00:00", "numberOfPlaces": "25"}
]

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def patch_data():
    """Injecte les données mockées avant chaque test"""
    with patch("server.loadClubs", return_value=mock_clubs), \
         patch("server.loadCompetitions", return_value=mock_competitions), \
         patch("server.clubs", mock_clubs), \
         patch("server.competitions", mock_competitions):
        yield

def test_available_places(client):
    response = client.post('/purchasePlaces', data={
        'competition': "Test Competition",
        'club': "Test Club",
        'places': '5'
    })
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data

def test_exceed_available_places(client):
    response = client.post('/purchasePlaces', data={
        'competition': "Test Competition",
        'club': "Test Club",
        'places': '26'
    })
    assert response.status_code == 200
    assert b"Error: Only" in response.data

def test_zero_places(client):
    response = client.post('/purchasePlaces', data={
        'competition': "Test Competition",
        'club': "Test Club",
        'places': '0'
    })
    assert response.status_code == 200
    assert b"The number of places must be a positive integer" in response.data

def test_negative_places(client):
    response = client.post('/purchasePlaces', data={
        'competition': "Test Competition",
        'club': "Test Club",
        'places': '-3'
    })
    assert response.status_code == 200
    assert b"The number of places must be a positive integer" in response.data