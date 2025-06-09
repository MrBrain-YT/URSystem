import pytest
import os
import sys

# Add project root to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from main import app
from configuration.server_token import reg_token

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_account_data_success(client):
    json = {
        "name": "SuperAdmin",
        "password": "12345",
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
    assert json["info"] == "Password incorrect"
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
    assert json["info"] == "Account data with the System role cannot be transferred"
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
    assert json["info"] == "Name not in users"
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
    assert json["info"] == "Server token incorrect"
    assert json["status"] == False