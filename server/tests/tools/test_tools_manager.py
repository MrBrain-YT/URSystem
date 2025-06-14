import pytest
import os
import sys

# Add project root to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from main import app
from configuration.server_token import reg_token

name_tool = "TestName"

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_create_tool_success(client):
    json = {
        "id": name_tool,
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/create-tool', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_create_tool_error_already_exists(client):
    json = {
        "id": name_tool,
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/create-tool', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_get_tools_success(client):
    json = {
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/get-tools', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_get_tool_success(client):
    json = {
        "id": name_tool,
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/get-tool', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_get_tool_error_not_found(client):
    json = {
        "id": "",
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/get-tool', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert "data" not in json
    assert json["status"] == False

def test_set_tool_data_success(client):
    json = {
        "id": name_tool,
        "parameter": "test",
        "value": 5,
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/set-tool', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_set_tool_data_error_not_found(client):
    json = {
        "id": "",
        "parameter": "test",
        "value": 5,
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/set-tool', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_set_calibration_data_success(client):
    json = {
        "id": name_tool,
        "calibration_data": {"x": 0, "y": 0, "z": 0},
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/set-tool-calibration', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

# TODO: add validation callibarion data
def test_set_calibration_data_error_not_valid(client):
    json = {
        "id": name_tool,
        "calibration_data": [0, 0, 0],
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/set-tool-calibration', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_set_calibration_data_error_not_found(client):
    json = {
        "id": "",
        "calibration_data": {"x": 0, "n": 0, "b": 0},
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/set-tool-calibration', json=json)
    assert response.status_code == 404
    json = response.get_json()
    assert json["status"] == False

def test_delete_tool_success(client):
    json = {
        "id": name_tool,
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/delete-tool', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_delete_tool_error_not_found(client):
    json = {
        "id": name_tool,
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/delete-tool', json=json)
    assert response.status_code == 403
    json = response.get_json()
    assert json["status"] == False