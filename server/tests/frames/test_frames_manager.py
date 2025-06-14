import pytest
import os
import sys

# Add project root to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from main import app

name_frame = "TestName"

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_create_frame_success(client):
    json = {
        "id": name_frame,
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/create-frame', json=json)
    print(response.get_json())
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_create_frame_error_exists(client):
    json = {
        "id": name_frame,
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/create-frame', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_get_frames_success(client):
    json = {
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/get-frames', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_get_frame_success(client):
    json = {
        "id": name_frame,
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/get-frame', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_set_frame_success(client):
    json = {
        "id": name_frame,
        "config": {"state": True},
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/set-frame', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True
    
def test_delete_frames_success(client):
    json = {
        "id": name_frame,
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/delete-frame', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_delete_frames_error_not_found(client):
    json = {
        "id": name_frame,
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/delete-frame', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_get_frame_error_not_found(client):
    json = {
        "id": name_frame,
        "config": "",
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/get-frame', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert "data" not in json
    assert json["status"] == False