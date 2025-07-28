import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tests.config import client, TestData

def test_get_certs_success(client):
    json = {
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-certs', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_download_cert_success(client):
    json = {
        "file_name": "localhost.crt",
        "server_token": TestData.server_token,
    }
    response = client.post('/api/download-cert', json=json)
    assert response.status_code == 200

def test_download_cert_error_not_found(client):
    json = {
        "file_name": "",
        "server_token": TestData.server_token,
    }
    response = client.post('/api/download-cert', json=json)
    assert response.status_code == 404
    json = response.get_json()
    assert json["status"] == False
