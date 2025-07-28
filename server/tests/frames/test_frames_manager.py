import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tests.config import client, TestData

def test_create_frame_success(client):
    json = {
        "id": TestData.frame_name,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/create-frame', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_create_frame_error_exists(client):
    json = {
        "id": TestData.frame_name,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/create-frame', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_get_frames_success(client):
    json = {
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-frames', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_get_frame_success(client):
    json = {
        "id": TestData.frame_name,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-frame', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_set_frame_success(client):
    json = {
        "id": TestData.frame_name,
        "config": {"state": True},
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-frame', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True
    
def test_delete_frames_success(client):
    json = {
        "id": TestData.frame_name,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/delete-frame', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_delete_frames_error_not_found(client):
    json = {
        "id": TestData.frame_name,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/delete-frame', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_get_frame_error_not_found(client):
    json = {
        "id": TestData.frame_name,
        "config": "",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-frame', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert "data" not in json
    assert json["status"] == False