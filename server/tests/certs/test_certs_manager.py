import pytest
import os
import sys

# Add project root to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from main import app
from configuration.server_token import reg_token

name_base = "TestName"

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_certs_success(client):
    json = {
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/get-certs', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_download_cert_success(client):
    json = {
        "file_name": "localhost.crt",
        "server_token": reg_token,
    }
    response = client.post('/api/download-cert', json=json)
    assert response.status_code == 200

def test_download_cert_error_not_found(client):
    json = {
        "file_name": "",
        "server_token": reg_token,
    }
    response = client.post('/api/download-cert', json=json)
    assert response.status_code == 404
    json = response.get_json()
    assert json["status"] == False
