# tests/test_app.py
import os
import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_health(client):
    rv = client.get("/health")
    assert rv.status_code == 200
    assert 'status' in rv.get_json()

def test_index(client):
    rv = client.get("/")
    assert rv.status_code == 200
