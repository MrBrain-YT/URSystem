import hashlib
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from tests.config import client, TestData

def test_create_robot_success(client):
    password = TestData.super_admin_password.encode(encoding="utf-8")
    password_hash = hashlib.sha256(password).hexdigest()
    json = {
        "robot": "TestRobot",
        "angle": 5,
        "code": "TestCode123",
        "password": password_hash,
        "id": None,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/create-robot', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_create_robot_error(client):
    password = TestData.super_admin_password.encode(encoding="utf-8")
    password_hash = hashlib.sha256(password).hexdigest()
    json = {
        "robot": "TestRobot",
        "angle": 5,
        "code": "TestCode123",
        "password": password_hash,
        "id": None,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/create-robot', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_import_cache_success(client):
    json = {
        "robots": {},
        "tools": {},
        "frames": {},
        "bases": {},
        "token": TestData.super_admin_token
    }
    response = client.post('/api/import-cache', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_export_file_cache_success(client):
    json = {
        "token": TestData.super_admin_token
    }
    response = client.post('/api/export-file-cache', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_export_cache_success(client):
    json = {
        "token": TestData.super_admin_token
    }
    response = client.post('/api/export-cache', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_get_robot_success(client):
    json = {
        "robot": "TestRobot",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-robot', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_get_robot_error(client):
    json = {
        "robot": "",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-robot', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert "data" not in json
    assert json["status"] == False

def test_get_robots_success(client):
    json = {
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-robots', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_delete_robot_success(client):
    json = {
        "robot": "TestRobot",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/delete-robot', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_delete_robot_error(client):
    json = {
        "robot": "TestRobot",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/delete-robot', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False