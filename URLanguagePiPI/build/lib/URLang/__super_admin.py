"""  module for additional commands for the SuperAdmin.

The tokenizer class is used to automatically send a token to the system class after registration.

"""

import shutil
import os
import json

import requests

from . import roles
from . import __admin

token = ""
class tokenizer():

    def __init__(self, token) -> None:
        self.token = token

    def set_token(self) -> None:
        global token
        token = self.token

# United robotics system 
class system(__admin.system):

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.token = token
        super().__init__(host, port, self.token)

    def add_kinematic(self ,path:str) -> None:
        shutil.copy2(path, f'{os.getcwd()}\\kinematics')

    def delete_user(self, name:str) -> str:
        url = f"https://{self.host}:{self.port}/DeleteAccount"
        data = {
            "name": name,
            "token": self.token
            }
        resp = requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text
        return resp

    def add_user(self, name:str, password:str, role:roles) -> str:
        url = f"https://{self.host}:{self.port}/CreateAccount"
        data = {
            "name": name,
            "password": password,
            "user_role": role,
            "token": self.token
            }
        resp = requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text
        return resp
    
    def get_user_accounts(self) -> str:
        url = f"https://{self.host}:{self.port}/GetAccounts"
        data = {"token": self.token}
        resp = requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text
        return resp
    
    def change_password(self, name:str, password:str) -> str:
        url = f"https://{self.host}:{self.port}/ChangePass"
        data = {
            "name": name,
            "password": password,
            "token": self.token
        }
        resp = requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text
        return resp
    