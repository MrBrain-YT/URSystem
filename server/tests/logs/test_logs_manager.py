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

def test_add_robot_log_success(client):
    json = {
        "robot": "First",
        "text": "test_msg",
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/add-robot-log', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_get_robot_logs_success(client):
    json = {
        "robot": "First",
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/get-robot-logs', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_add_system_log_success(client):
    json = {
        "module": "AutoTests",
        "text": "test_msg",
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/add-system-log', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_get_system_logs_success(client):
    json = {
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/get-system-logs', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True