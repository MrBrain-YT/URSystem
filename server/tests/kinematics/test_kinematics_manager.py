import os
import sys

from werkzeug.datastructures import FileStorage

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tests.config import client, TestData
from services.kinematics_manager import KinematicsManager

def test_add_kinematic_success(client):
    # used service for checking 
    kinematic_file = FileStorage(open("tests/test_files/test_kinematic.zip", "rb"), f"{TestData.kinematic_name}.zip", name="test")
    json_resp, code = KinematicsManager().add_kinematic(kinematic_file)
    assert code == 200
    assert json_resp["status"] == True

def test_bind_kinematic_success(client):
    json = {
        "robot": TestData.robot_name,
        "code": TestData.robot_secret_code,
        "id": TestData.kinematic_name,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/bind-kinematic', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_bind_kinematic_error_not_found(client):
    json = {
        "robot": TestData.robot_name,
        "code": TestData.robot_secret_code,
        "id": "",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/bind-kinematic', json=json)
    assert response.status_code == 404
    json = response.get_json()
    assert json["status"] == False

def test_unbind_kinematic_success(client):
    json = {
        "robot": TestData.robot_name,
        "code": TestData.robot_secret_code,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/unbind-kinematic', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True
    json = {
        "robot": TestData.robot_name,
        "id": TestData.kinematic_name,
        "code": TestData.robot_secret_code,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/bind-kinematic', json=json)

def test_unbind_kinematic_error_not_found(client):
    json = {
        "robot": "",
        "code": TestData.robot_secret_code,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/unbind-kinematic', json=json)
    assert response.status_code == 403
    json = response.get_json()
    assert json["status"] == False

def test_remove_kinematic_success(client):
    # used service for checking 
    json = {
        "id": TestData.kinematic_name,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/delete-kinematic', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True
    
def test_remove_kinematic_error_not_found(client):
    # used service for checking 
    json = {
        "id": "",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/delete-kinematic', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False