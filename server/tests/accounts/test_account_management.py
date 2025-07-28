import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tests.config import client, TestData
from services.accounts_manager import AccountManager

def test_create_account_success(client):
    json = {
        "name": TestData.new_account_name,
        "password": TestData.new_account_password,
        "role": TestData.new_account_role,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/create-account', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_create_account_error_exist(client):
    json = {
        "name": TestData.new_account_name,
        "password": TestData.new_account_password,
        "role": TestData.new_account_role,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/create-account', json=json)
    json = response.get_json()
    assert response.status_code == 400
    assert json["status"] == False

def test_get_accounts_success(client):
    json = {
        "name": TestData.super_admin_login,
        "password": TestData.super_admin_password,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-accounts', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert "data" != {}
    assert json["status"] == True
    

def test_change_password_success(client):
    json = {
        "name": TestData.new_account_name,
        "password": "123456",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/change-password', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True
    json = {
        "name": TestData.new_account_name,
        "password": TestData.new_account_password,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/change-password', json=json)
    
def test_change_password_error_system_role(client):
    json = {
        "name": "",
        "password": "12345",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/change-password', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert "data" not in json
    assert json["status"] == False
    
def test_change_password_error_account_not_found(client):
    json = {
        "name": "Harry_Poter",
        "password": "12345",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/change-password', json=json)
    assert response.status_code == 404
    json = response.get_json()
    assert json["status"] == False
    
def test_get_user_token_success(client):
    json = {
        "name": TestData.new_account_name,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-token', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True
    
def test_get_user_token_error_system_role(client):
    json = {
        "name": "",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-token', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert "data" not in json
    assert json["status"] == False
    
def test_get_user_token_error_not_found(client):
    json = {
        "name": "Harry_Poter",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-token', json=json)
    assert response.status_code == 404
    json = response.get_json()
    assert "data" not in json
    assert json["status"] == False
    
def test_change_token_success(client):
    json = {
        "name": TestData.new_account_name,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/change-token', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True
    AccountManager().change_token(name="user",
        token="cf57f79a27f9610d7a925139b67dfd9ec2c6ddedd2bf572bf2a191a99dd83b8c")

def test_delete_account_success(client):
    json = {
        "name": TestData.new_account_name,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/delete-account', json=json)
    json = response.get_json()
    assert response.status_code == 200
    assert json["status"] == True

def test_delete_account_error_not_found(client):
    json = {
        "name": TestData.new_account_name,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/delete-account', json=json)
    json = response.get_json()
    assert response.status_code == 400
    assert json["status"] == False