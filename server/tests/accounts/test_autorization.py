import hashlib
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from tests.config import client, TestData
from configuration.server_token import reg_token

def test_get_account_data_success(client):
    password = TestData.super_admin_password.encode(encoding="utf-8")
    password_hash = hashlib.sha256(password).hexdigest()
    json = {
        "name": "SuperAdmin",
        "password": password_hash,
        "server_token": reg_token
    }
    response = client.post('/api/get-account-data', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_get_account_data_error_password(client):
    json = {
        "name": TestData.super_admin_login,
        "password": "lkjgneiruhh45",
        "server_token": reg_token
    }
    response = client.post('/api/get-account-data', json=json)
    assert response.status_code == 401
    json = response.get_json()
    assert json["status"] == False

def test_get_account_data_error_system_role(client):
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

def test_get_account_data_error_server_token(client):
    json = {
        "name": TestData.super_admin_login,
        "password": TestData.super_admin_password,
        "server_token": ""
    }
    response = client.post('/api/get-account-data', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False