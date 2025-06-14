import pytest
import os
import sys
import shutil

# Add project root to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_add_kinematic_success(client):
    # json = {
    #     "file": open("tests/test_files/test_kinematic.zip", "rb"),
    #     "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    # }
    # response = client.post('/api/add-kinematic', json=json)
    # print(response.data)
    # assert response.status_code == 200
    # json = response.get_json()
    # assert json["status"] == True
    os.mkdir("kinematics/test_kinematic")
    shutil.unpack_archive(filename="tests/test_files/test_kinematic.zip", extract_dir="kinematics/test_kinematic", format="zip")

def test_bind_kinematic_success(client):
    json = {
        "robot": "First",
        "code": "654123",
        "id": "test_kinematic",
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/bind-kinematic', json=json)
    print(response.text)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_bind_kinematic_error_not_found(client):
    json = {
        "robot": "First",
        "code": "654123",
        "id": "",
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/bind-kinematic', json=json)
    assert response.status_code == 404
    json = response.get_json()
    assert json["status"] == False

def test_unbind_kinematic_success(client):
    json = {
        "robot": "First",
        "code": "654123",
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/unbind-kinematic', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True
    json = {
        "robot": "First",
        "id": "First",
        "code": "654123",
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/bind-kinematic', json=json)

def test_unbind_kinematic_error_not_found(client):
    json = {
        "robot": "",
        "code": "654123",
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/unbind-kinematic', json=json)
    assert response.status_code == 404
    json = response.get_json()
    assert json["status"] == False

def test_remove_kinematic_success(client):
    # json = {
    #     "file": open("tests/test_files/test_kinematic.zip", "rb"),
    #     "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    # }
    # response = client.post('/api/add-kinematic', json=json)
    # print(response.data)
    # assert response.status_code == 200
    # json = response.get_json()
    # assert json["status"] == True
    shutil.rmtree("kinematics/test_kinematic")