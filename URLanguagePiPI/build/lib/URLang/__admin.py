"""  module for additional commands for the administrator.

The system class has a kwargs argument "token" so that a user
authorized by the SuperAdmin role can send commands belonging to the Admin role.
The tokenizer class is used to automatically send a token to the system class after registration.

"""

import shutil
import os
import json

import requests

from . import __tools
from . import __robot
from . import roles

admin_token = ""
class tokenizer():

    def __init__(self, token) -> None:
        self.token = token

    def set_token(self) -> None:
        global admin_token
        admin_token = self.token

# United robotics system 
class system(__robot.Robot, __tools.Tools):

    def __init__(self, host:str, port:int, *token) -> None:
        self.host = host
        self.port = port
        self.token = token if admin_token == "" else admin_token
        super().__init__(host, port, token=self.token)

    def add_kinematic(self ,path:str) -> None:
        shutil.copy2(path, f'{os.getcwd()}\\kinematics')

    def add_tool(self, id:str) -> str:
        url = f"https://{self.host}:{self.port}/URTC"
        data = {
            "Id": id,
            "token": self.token
        }
        resp = requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text
        return resp
    
    def add_robot(self, robot_name:str, angle_count:int, kinematics) -> str:
        url = f"https://{self.host}:{self.port}/CreateRobot"
        data = {
            "Robot": robot_name,
            "Angle": angle_count,
            "Kinematics" : kinematics,
            "token": self.token
            }
        resp = requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text
        return resp
    
    def delete_tool(self, id) -> str:
        url = f"https://{self.host}:{self.port}/URTD"
        data = {
            "Id": id,
            "token": self.token
            }
        resp = requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text
        return resp

    def delete_robot(self, robot_name:str) -> str:
        url = f"https://{self.host}:{self.port}/DelRobot"
        data = {
            "Robot": robot_name,
            "token": self.token
            }
        resp = requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text
        return resp

    def add_user(self, name:str, password:str) -> None:
        url = f"https://{self.host}:{self.port}/CreateAccount"
        data = {
            "name": name,
            "password": password,
            "User_role": roles.Roles.user,
            "token": self.token
            }
        resp = requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text
        return resp
    
    def get_robots(self) -> str:
        url = f"https://{self.host}:{self.port}/GetRobots"
        data = {
            "token": self.token
            }
        resp = requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text
        return resp

    def get_robot(self, robot_name:str) -> str:
        url = f"https://{self.host}:{self.port}/GetRobot"
        data = {
            "Robot": robot_name, 
            "token": self.token
            }
        resp = requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text
        return resp
    
    def add_log(self, robot_name:str, type:str, text:str) -> bool:
        url = f"https://{self.host}:{str(self.port)}/URLogs"
        data = {
            "Robot": robot_name,
            "Type": type,
            "Text": text,
            "token": self.token
            }
        return bool(requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text)
    
    def delete_logs(self, robot_name:str) -> bool:
        url = f"https://{self.host}:{str(self.port)}/URDLog"
        data = {
            "Robot": robot_name,
            "token": self.token
            }
        return bool(requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text)
