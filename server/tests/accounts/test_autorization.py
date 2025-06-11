import pytest
import os
import sys
import hashlib

# Add project root to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from main import app
from configuration.server_token import reg_token

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_account_data_success(client):
    password = hashlib.sha256("12345".encode(encoding="utf-8")).hexdigest()
    json = {
        "name": "SuperAdmin",
        "password": password,
        "server_token": reg_token
    }
    response = client.post('/api/get-account-data', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_get_account_data_error_password(client):
    json = {
        "name": "SuperAdmin",
        "password": "lkjgneiruhh45",
        "server_token": reg_token
    }
    response = client.post('/api/get-account-data', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_get_account_data_error_role(client):
    json = {
        "name": "",
        "password": "",
        "server_token": reg_token
    }
    response = client.post('/api/get-account-data', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_get_account_data_error_name(client):
    json = {
        "name": "test",
        "password": "12345",
        "server_token": reg_token
    }
    response = client.post('/api/get-account-data', json=json)
    assert response.status_code == 404
    json = response.get_json()
    assert json["status"] == False

def test_get_account_data_error_server(client):
    json = {
        "name": "SuperAdmin",
        "password": "12345",
        "server_token": ""
    }
    response = client.post('/api/get-account-data', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False