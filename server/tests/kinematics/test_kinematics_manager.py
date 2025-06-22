import os
import shutil
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tests.config import client, TestData

def test_add_kinematic_success(client):
    # json = {
    #     "file": open("tests/test_files/test_kinematic.zip", "rb"),
    #     "token": TestData.super_admin_token
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
        "robot": TestData.robot_name,
        "code": TestData.robot_secret_code,
        "id": "test_kinematic",
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
        "id": "First",
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
    assert response.status_code == 404
    json = response.get_json()
    assert json["status"] == False

# TODO: add api method for removing kinematic folder
def test_remove_kinematic_success(client):
    # json = {
    #     "file": open("tests/test_files/test_kinematic.zip", "rb"),
    #     "token": TestData.super_admin_token
    # }
    # response = client.post('/api/add-kinematic', json=json)
    # print(response.data)
    # assert response.status_code == 200
    # json = response.get_json()
    # assert json["status"] == True
    shutil.rmtree("kinematics/test_kinematic")