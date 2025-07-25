import os
import sys
import time
from threading import Thread
import queue

# Add project root to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tests.config import client, TestData
from services.robot_manager import RobotManager
from tests.tools import test_tools_manager
from tests.bases import test_bases_management
from tests.kinematics import test_kinematics_manager

def set_ready(state:bool):
    from tests.config import app
    client = app.test_client()
    json = {
        "state": state,
        "token": TestData.robot_token
    }
    client.post('/api/set-ready', json=json)

def test_get_position_success(client):
    test_kinematics_manager.test_add_kinematic_success(client)
    test_kinematics_manager.test_bind_kinematic_success(client)
    json = {
        "robot": TestData.robot_name,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-position', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_get_position_error_robot_not_found(client):
    json = {
        "robot": "",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-position', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert "data" not in json
    assert json["status"] == False

def test_get_position_id_success(client):
    json = {
        "robot": TestData.robot_name,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-position-id', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_get_position_id_error_robot_not_found(client):
    json = {
        "robot": "",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-position-id', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert "data" not in json
    assert json["status"] == False

def test_get_speed_success(client):
    json = {
        "robot": TestData.robot_name,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-speed', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_get_speed_error_robot_not_found(client):
    json = {
        "robot": "",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-speed', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_get_cartesian_position_success(client):
    json = {
        "robot": TestData.robot_name,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-cartesian-position', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_get_cartesian_position_error_robot_not_found(client):
    json = {
        "robot": "",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-cartesian-position', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert "data" not in json
    assert json["status"] == False

def test_get_angles_count_success(client):
    json = {
        "robot": TestData.robot_name,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-angles-count', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_get_angles_count_error_robot_not_found(client):
    json = {
        "robot": "",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-angles-count', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert "data" not in json
    assert json["status"] == False

def test_set_motors_position_success(client):
    json = {
        "angles": {'J1': 126.206024, 'J2': 150.746567, 'J3': 141.730881, 'J4': -99.015686},
        "token": TestData.robot_token
    }
    response = client.post('/api/set-motors-position', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_set_motors_position_error_robot_not_found(client):
    json = {
        "angles": {'J1': 126.206024, 'J2': 150.746567, 'J3': 141.730881, 'J4': -99.015686},
        "token": ""
    }
    response = client.post('/api/set-motors-position', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_get_ready_state_success(client):
    json = {
        "robot": "hdfvhwegfvtevfuyberuy",
        "token": TestData.robot_token
    }
    response = client.post('/api/get-ready', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True
    

def test_get_ready_state_error_robot_not_found(client):
    json = {
        "robot": "",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-ready', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert "data" not in json
    assert json["status"] == False

def test_get_emergency_state_success(client):
    json = {
        "robot": TestData.robot_name,
        "token": TestData.robot_token
    }
    response = client.post('/api/get-emergency', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_get_emergency_state_error_robot_not_found(client):
    json = {
        "robot": "",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-emergency', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert "data" not in json
    assert json["status"] == False

def test_set_ready_state_success(client):
    json = {
        "state": False,
        "token": TestData.robot_token
    }
    response = client.post('/api/set-ready', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_set_ready_state_error_not_been_seted(client):
    def set_position():
        from tests.config import app
        client = app.test_client()
        json = {
            "robot": TestData.robot_name,
            "angles": {'J1': 0.0, 'J2': 0.0, 'J3': 0.0, 'J4': 0.0},
            "token": TestData.robot_token
        }
        client.post('/api/set-position', json=json)
        
    p1 = Thread(target=set_position)
    p2 = Thread(target=lambda: set_ready(True))   
    p1.start()
    time.sleep(1)
    p2.start()
    while p1.is_alive():
        pass
    
    json = {
        "state": True,
        "token": TestData.robot_token
    }
    response = client.post('/api/set-ready', json=json)
    
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_set_ready_state_error_robot_not_found(client):
    json = {
        "state": False,
        "token": ""
    }
    response = client.post('/api/set-ready', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_set_position_id_success(client):
    json = {
        "robot": TestData.robot_name,
        "id": "hello",
        "token": TestData.robot_token
    }
    response = client.post('/api/set-position-id', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_set_position_id_error_not_defined(client):
    json = {
        "robot": "",
        "state": False,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-position-id', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_set_emergency_state_success(client):
    # check set_emergency
    json = {
        "robot": TestData.robot_name,
        "state": True,
        "token": TestData.robot_token
    }
    response = client.post('/api/set-emergency', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True
    # revert to default value (False) for good result from other test
    json = {
        "robot": TestData.robot_name,
        "state": False,
        "token": TestData.robot_token
    }
    response = client.post('/api/set-emergency', json=json)
    # pass

def test_set_emergency_state_error_not_defined(client):
    json = {
        "robot": "",
        "state": True,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-emergency', json=json)
    assert response.status_code == 403
    json = response.get_json()
    assert json["status"] == False

def test_set_mutipoint_position_success(client):
    q = queue.Queue()
    set_ready(False)
    
    def set_position():
        from tests.config import app
        client = app.test_client()
        json = {
            "robot": TestData.robot_name,
            "angles_data": [
                {'J1': 126.206024, 'J2': 150.746567, 'J3': 141.730881, 'J4': -99.015686},
                {'J1': 0.206024, 'J2': 0.0, 'J3': 141.730881, 'J4': -99.015686},
                {'J1': 0, 'J2': 0, 'J3': 0, 'J4': 0},
            ],
            "token": TestData.robot_token
        }
        q.put(client.post('/api/set-position', json=json))
    
    p1 = Thread(target=set_position)
    p2 = Thread(target=lambda: set_ready(True))   
    p1.start()
    time.sleep(1)
    p2.start()
    while p1.is_alive():
        pass
    
    response = q.get()
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_set_mutipoint_position_error_array_not_valid(client):
    q = queue.Queue()
    set_ready(False)
    
    def set_position():
        from tests.config import app
        client = app.test_client()
        json = {
        "robot": TestData.robot_name,
        "angles_data": "",
        "token": TestData.robot_token
        }
        q.put(client.post('/api/set-position', json=json))

        
    p1 = Thread(target=set_position)
    p2 = Thread(target=lambda: set_ready(True))   
    p1.start()
    time.sleep(1)
    p2.start()
    while p1.is_alive():
        pass
    
    response = q.get()
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_set_position_error_robot_not_found(client):
    json = {
        "robot": "",
        "angles_data": "",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-position', json=json)
    assert response.status_code == 403
    json = response.get_json()
    assert json["status"] == False

def test_remove_current_point_position_success(client):
    json = {
        "robot": TestData.robot_name,
        "token": TestData.robot_token
    }
    response = client.post('/api/remove-current-point-position', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_remove_all_point_position_success(client):
    json = {
        "robot": TestData.robot_name,
        "token": TestData.robot_token
    }
    response = client.post('/api/remove-current-point-position', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_remove_current_point_position_error_not_multi_point(client):
    json = {
        "robot": TestData.robot_name,
        "token": TestData.robot_token
    }
    response = client.post('/api/remove-current-point-position', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False
    
def test_remove_all_point_position_error_not_multi_point(client):
    json = {
        "robot": TestData.robot_name,
        "token": TestData.robot_token
    }
    response = client.post('/api/remove-all-point-position', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_set_home_position_success(client):
    json = {
        "robot": TestData.robot_name,
        "angles": {'J1': 0, 'J2': 0, 'J3': 0, 'J4': 0},
        "code": TestData.robot_secret_code,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-home-position', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_set_home_position_error_not_correct(client):
    json = {
        "robot": TestData.robot_name,
        "angles": {'J1': 1000, 'J2': 1000, 'J3': 1000, 'J4': 1000},
        "code": TestData.robot_secret_code,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-home-position', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_set_speed_success(client):
    json = {
        "robot": TestData.robot_name,
        "angles_data": [
            {'J1': 126.206024, 'J2': 150.746567, 'J3': 141.730881, 'J4': -99.015686},
            {'J1': 0.0, 'J2': 0.0, 'J3': 0.0, 'J4': 0.0}
        ],
        "token": TestData.robot_token
    }
    response = client.post('/api/set-speed', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_set_speed_error_not_valid(client):
    json = {
        "robot": TestData.robot_name,
        "angles_data": {'J1': 126.206024, 'J2': 150.746567, 'J3': 141.730881, 'J4': -99.015686},
        "code": TestData.robot_secret_code,
        "token": TestData.robot_token
    }
    response = client.post('/api/set-speed', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_remove_current_point_speed_success(client):
    json = {
        "robot": TestData.robot_name,
        "token": TestData.robot_token
    }
    response = client.post('/api/remove-current-point-speed', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_remove_current_point_speed_error_not_multi_point(client):
    json = {
        "robot": TestData.robot_name,
        "token": TestData.robot_token
    }
    response = client.post('/api/remove-current-point-speed', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_remove_all_point_speed_success(client):
    json = {
        "robot": TestData.robot_name,
        "angles_data": [
            {'J1': 126.206024, 'J2': 150.746567, 'J3': 141.730881, 'J4': -99.015686},
            {'J1': 0.0, 'J2': 0.0, 'J3': 0.0, 'J4': 0.0}
        ],
        "token": TestData.robot_token
    }
    response = client.post('/api/set-speed', json=json)
    json = {
        "robot": TestData.robot_name,
        "token": TestData.robot_token
    }
    response = client.post('/api/remove-all-point-speed', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_remove_all_point_speed_error_not_multi_point(client):
    json = {
        "robot": TestData.robot_name,
        "token": TestData.robot_token
    }
    response = client.post('/api/remove-all-point-speed', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_set_standard_speed_success(client):
    json = {
        "robot": TestData.robot_name,
        "angles": {'J1': 1.0, 'J2': 1.0, 'J3': 1.0, 'J4': 1.0},
        "code": TestData.robot_secret_code,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-standard-speed', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_set_standard_speed_error_robot_not_found(client):
    json = {
        "robot": "",
        "angles": {'J1': 126.206024, 'J2': 150.746567, 'J3': 141.730881, 'J4': -99.015686},
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-standard-speed', json=json)
    assert response.status_code == 403
    json = response.get_json()
    assert json["status"] == False

def test_set_program_success(client):
    json = {
        "robot": TestData.robot_name,
        "program": "",
        "code": TestData.robot_secret_code,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-program', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_set_program_error_robot_not_found(client):
    json = {
        "robot": "",
        "program": "",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-program', json=json)
    assert response.status_code == 403
    json = response.get_json()
    assert json["status"] == False

def test_delete_program_success(client):
    json = {
        "robot": TestData.robot_name,
        "code": TestData.robot_secret_code,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/delete-program', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_delete_program_error_robot_not_found(client):
    json = {
        "robot": "",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/delete-program', json=json)
    assert response.status_code == 403
    json = response.get_json()
    assert json["status"] == False
    
# TODO: create normal kinematic module for tests
def test_angles_to_cartesian_success(client):
    json = {
        "robot": TestData.robot_name,
        "angles": {'J1': 126.206024, 'J2': 150.746567, 'J3': 141.730881, 'J4': -99.015686},
        "token": TestData.robot_token
    }
    response = client.post('/api/angles-to-cartesian', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True 

def test_angles_to_cartesian_error_not_valid(client):
    json = {
        "robot": TestData.robot_name,
        "angles_data": "",
        "token": TestData.robot_token
    }
    response = client.post('/api/angles-to-cartesian', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert "data" not in json
    assert json["status"] == False

def test_cartesian_to_angles_success(client):
    json = {
        "robot": TestData.robot_name,
        "position": {"x": 0, "y": 0, "z": 0, "a": 0, "b": 0, "c": 0},
        "coordinate_system": "world",
        "token": TestData.robot_token
    }
    response = client.post('/api/cartesian-to-angles', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_cartesian_to_angles_array_success(client):
    json = {
        "robot": TestData.robot_name,
        "positions_data": [
                {"x": 0, "y": 0, "z": 0, "a": 0, "b": 0, "c": 0},
                {"x": 10, "y": 10, "z": 10, "a": 10, "b": 10, "c": 10}
            ],
        "coordinate_system": "world",
        "token": TestData.robot_token
    }
    response = client.post('/api/cartesian-to-angles', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

def test_cartesian_to_angles_error_not_used_kinematic(client):
    # unbind kinematic
    json = {
        "robot": TestData.robot_name,
        "code": TestData.robot_secret_code,
        "token": TestData.super_admin_token
    }
    client.post('/api/unbind-kinematic', json=json)
    
    json = {
        "robot": TestData.robot_name,
        "position": {"x": 0, "y": 0, "z": 0, "a": 0, "b": 0, "c": 0},
        "coordinate_system": "world",
        "token": TestData.robot_token
    }
    response = client.post('/api/cartesian-to-angles', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert "data" in json
    assert json["status"] == True

    # bind kinematic
    json = {
        "robot": TestData.robot_name,
        "code": TestData.robot_secret_code,
        "id": TestData.kinematic_name,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/bind-kinematic', json=json)

def test_cartesian_to_angles_error_not_valid(client):
    json = {
        "robot": TestData.robot_name,
        "positions_data": {"x": 0, "y": 0, "z": 0, "a": 0, "b": 0, "c": 0},
        "coordinate_system": "world",
        "code": TestData.robot_secret_code,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/cartesian-to-angles', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert "data" not in json
    assert json["status"] == False

def test_cartesian_to_angles_error_robot_not_found(client):
    json = {
        "robot": "",
        "positions_data": [{"x": 0, "y": 0, "z": 0, "a": 0, "b": 0, "c": 0}],
        "coordinate_system": "world",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/cartesian-to-angles', json=json)
    assert response.status_code == 403
    json = response.get_json()
    assert "data" not in json
    assert json["status"] == False

def test_set_cartesian_position_success(client):
    q = queue.Queue()
    set_ready(False)
    
    def set_position():
        from tests.config import app
        client = app.test_client() 
        json = {
            "robot": TestData.robot_name,
            "code": TestData.robot_secret_code,
            "position": {"x": 0, "y": 0, "z": 0, "a": 0, "b": 0, "c": 0},
            "coordinate_system": "world",
            "token": TestData.super_admin_token
        }
        q.put(client.post('/api/set-cartesian-position', json=json))
    
    p1 = Thread(target=set_position)
    p2 = Thread(target=lambda: set_ready(True))   
    p1.start()
    time.sleep(1)
    p2.start()
    while p1.is_alive():
        pass
    
    response = q.get()
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_set_cartesian_position_array_success(client):
    q = queue.Queue()
    set_ready(False)
    
    def set_position():
        from tests.config import app
        client = app.test_client() 
        json = {
            "robot": TestData.robot_name,
            "code": TestData.robot_secret_code,
            "positions_data": [
                {"x": 0, "y": 0, "z": 0, "a": 0, "b": 0, "c": 0},
                {"x": 10, "y": 10, "z": 10, "a": 10, "b": 10, "c": 10}
            ],
            "coordinate_system": "world",
            "token": TestData.super_admin_token
        }
        q.put(client.post('/api/set-cartesian-position', json=json))
    
    p1 = Thread(target=set_position)
    p2 = Thread(target=lambda: set_ready(True))   
    p1.start()
    time.sleep(1)
    p2.start()
    while p1.is_alive():
        pass
    
    response = q.get()
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_set_cartesian_position_array_error_not_valid(client):
    json = {
        "robot": TestData.robot_name,
        "positions_data": "",
        "coordinate_system": "world",
        "code": TestData.robot_secret_code,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-cartesian-position', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_set_cartesian_position_error_robot_not_found(client):
    json = {
        "robot": "",
        "position": "",
        "coordinate_system": "world",
        "code": TestData.robot_secret_code,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-cartesian-position', json=json)
    assert response.status_code == 403
    json = response.get_json()
    assert json["status"] == False

def test_set_min_angles_success(client):
    json = {
        "robot": TestData.robot_name,
        "angles": {'J1': 0.0, 'J2': 0.0, 'J3': 0.0, 'J4': 0.0},
        "code": TestData.robot_secret_code,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-min-angles', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_set_min_angles_error_not_defined(client):
    json = {
        "robot": "",
        "angles": {'J1': 0.0, 'J2': 0.0, 'J3': 0.0, 'J4': 0.0},
        "code": TestData.robot_secret_code,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-min-angles', json=json)
    assert response.status_code == 403
    json = response.get_json()
    assert json["status"] == False

def test_set_max_angles_success(client):
    json = {
        "robot": TestData.robot_name,
        "angles": {'J1': 300.0, 'J2': 300.0, 'J3': 300.0, 'J4': 300.0},
        "code": TestData.robot_secret_code,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-max-angles', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_set_max_angles_error_not_defined(client):
    json = {
        "robot": "",
        "angles": {'J1': 300.0, 'J2': 300.0, 'J3': 300.0, 'J4': 300.0},
        "code": TestData.robot_secret_code,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-max-angles', json=json)
    assert response.status_code == 403
    json = response.get_json()
    assert json["status"] == False

def test_set_program_run_state_success(client):
    # used service for checking 
    json_resp, code = RobotManager().set_program_run_state("First", False)
    assert code == 200
    assert json_resp["status"] == True

def test_set_robot_tool_error_tool_not_for_robots(client):
    # create tool
    test_tools_manager.test_create_tool_success(client)
    
    json = {
        "robot": TestData.robot_name,
        "code": TestData.robot_secret_code,
        "id": TestData.tool_name,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-robot-tool', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert json["status"] == False

def test_set_robot_tool_success(client):
    # calibrate tool
    test_tools_manager.test_set_calibration_data_success(client)
    # set robot tool
    json = {
        "robot": TestData.robot_name,
        "code": TestData.robot_secret_code,
        "id": TestData.tool_name,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-robot-tool', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_set_robot_tool_empty_success(client):
    json = {
        "robot": TestData.robot_name,
        "code": TestData.robot_secret_code,
        "id": "",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-robot-tool', json=json)
    # delete tool
    test_tools_manager.test_delete_tool_success(client)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_set_robot_tool_empty_repeat_error(client):
    json = {
        "robot": TestData.robot_name,
        "code": TestData.robot_secret_code,
        "id": "",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-robot-tool', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == False

def test_set_robot_tool_error_robot_not_found(client):
    json = {
        "robot": "",
        "code": TestData.robot_secret_code,
        "id": "ToolID",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-robot-tool', json=json)
    assert response.status_code == 403
    json = response.get_json()
    assert json["status"] == False

def test_set_robot_tool_error_tool_not_found(client):
    json = {
        "robot": TestData.robot_name,
        "code": TestData.robot_secret_code,
        "id": "test",
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-robot-tool', json=json)
    assert response.status_code == 404
    json = response.get_json()
    assert json["status"] == False
    
def test_set_robot_base_success(client):
    # create base
    test_bases_management.test_create_base_success(client)
    # set base
    json = {
        "robot": TestData.robot_name,
        "id": TestData.base_name,
        "code": TestData.robot_secret_code,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-robot-base', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_set_robot_base_empty_success(client):
    json = {
        "robot": TestData.robot_name,
        "id": "",
        "code": TestData.robot_secret_code,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-robot-base', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == True

def test_set_robot_base_empty_repeate_error(client):
    json = {
        "robot": TestData.robot_name,
        "id": "",
        "code": TestData.robot_secret_code,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-robot-base', json=json)
    assert response.status_code == 200
    json = response.get_json()
    assert json["status"] == False

def test_set_robot_base_error_robot_not_found(client):
    json = {
        "robot": "",
        "id": TestData.base_name,
        "code": TestData.robot_secret_code,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-robot-base', json=json)
    assert response.status_code == 403
    json = response.get_json()
    assert json["status"] == False

def test_set_robot_base_error_base_not_found(client):
    # delete base
    test_bases_management.test_delete_base_success(client)
    json = {
        "robot": TestData.robot_name,
        "id": "TestBase",
        "code": TestData.robot_secret_code,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/set-robot-base', json=json)
    assert response.status_code == 404
    json = response.get_json()
    assert json["status"] == False
    # delete test kinematic
    test_kinematics_manager.test_remove_kinematic_success(client)