import sys
import os
import json
from threading import Thread

from websockets.sync.client import connect

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tests.config import TestData
from utils.websocket.data_transfer import WebsocketServer

# Start websocket server
websocket_p = Thread(target=lambda:WebsocketServer().start_websocket_server("0.0.0.0", 5001))
websocket_p.start()

def test_get_robot_data_error():
    with connect("ws://127.0.0.1:5001", subprotocols=["json"]) as websocket:
        websocket.send(json.dumps({"token": "123"}))
        try:
            websocket.recv()
            assert False
        except:
            assert True

def test_get_robot_data_success():
    with connect("ws://127.0.0.1:5001", subprotocols=["json"]) as websocket:
        websocket.send(json.dumps({"token": TestData.robot_token}))
        message = websocket.recv()
        robot_data = json.loads(message)
    assert robot_data != {}
    assert isinstance(robot_data, dict)
    
def test_set_robot_ready_success():
    with connect("ws://127.0.0.1:5001", subprotocols=["json"]) as websocket:
        json_data = json.dumps({
            "token": TestData.robot_token,
            "type": "set",
            "parameter": "RobotReady",
            "value": True
        })
        websocket.send(json_data)
        message = websocket.recv()
        robot_data = json.loads(message)
    # Shutdown server
    with connect("ws://127.0.0.1:5001", subprotocols=["json"]) as websocket:
        websocket.send(json.dumps({"token": TestData.super_admin_token, "type": "shutdown"}))
        
    assert robot_data != {}
    assert isinstance(robot_data, dict)