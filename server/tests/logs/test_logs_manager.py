import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tests.config import client, TestData

def test_add_robot_log_success(client):
    json = {
        "robot": TestData.robot_name,
        "text": "test_msg",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/add-robot-log', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_get_robot_logs_success(client):
    json = {
        "robot": TestData.robot_name,
        "token": TestData.super_admin_token
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
        "token": TestData.super_admin_token
    }
    response = client.post('/api/add-system-log', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_get_system_logs_success(client):
    json = {
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-system-logs', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True