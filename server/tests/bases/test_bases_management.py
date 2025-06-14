import pytest
import os
import sys

# Add project root to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from main import app

name_base = "TestName"

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_bases_success(client):
    json = {
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/get-bases', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_create_base_success(client):
    json = {
        "id": name_base,
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/create-base', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_create_base_error(client):
    json = {
        "id": name_base,
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/create-base', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_get_base_success(client):
    json = {
        "id": name_base,
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/get-base', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_get_base_error(client):
    json = {
        "id": "",
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/get-base', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert "data" not in json
    assert json["status"] == False

def test_set_base_data_success(client):
    json = {
        "id": name_base,
        "data": {"x": 0, "y": 0, "z": 0,"a": 0, "b": 0, "c": 0},
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/set-base', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_set_base_data_error_not_valid(client):
    json = {
        "id": name_base,
        "data": {"x": 0, "y": 0, "z": 0},
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/set-base', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_set_base_data_error_not_exixts(client):
    json = {
        "id": "",
        "data": {"x": 0, "y": 0, "z": 0,"a": 0, "b": 0, "c": 0},
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/set-base', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_delete_base_success(client):
    json = {
        "id": name_base,
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/delete-base', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_delete_base_error(client):
    json = {
        "id": name_base,
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/delete-base', json=json)
    print(response.get_json())
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False