"""  Authorizing users and passing their token to the class corresponding to their role

To get users in the __get_role function, a server token is sent to the server,
which is created by the person who runs this server. After receiving data from the server,
it is checked with input data (username, password),
the received token is transferred to the tokenizer class and the system class is issued from a specific role module.

"""

import json

import requests

from . import __user as User
from . import __admin as Admin
from . import __super_admin as SuperAdmin


class Auth():
    def __init__(self, ip:str, port:int, server_token:str) -> None:
        self.ip = ip
        self.port = port
        self.server_token = server_token

    def __get_role(self, name, password):
        try:
            url = f"https://{self.ip}:{self.port}/GetRoleAccount"
            data = {
                "name": name,
                "password": password, 
                "server_token": self.server_token
                }
            resp = requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text
            if resp != "False":
                return resp.split(",")[0], resp.split(",")[1] 
            else:
                raise ValueError("Wrong login or password")
        except:
            raise ValueError("Wrong login or password")

    def user(self, name, password) -> User:
        if name != "":
            role, token = self.__get_role(name, password)
            if role != "System":
                User.tokenizer(token).set_token()
                return User
            elif role == "System":
                raise TypeError("It is impossible to use the system account")
    
    def admin(self, name, password) -> Admin:
        if name != "":
            role, token = self.__get_role(name, password)
            if role != "user" and role != "System":
                Admin.tokenizer(token).set_token()
                return Admin
            elif role == "System":
                raise TypeError("It is impossible to use the system account")
            else:
                raise TypeError("You don't have enough rights")
        
    def SuperAdmin(self, name, password) -> SuperAdmin:
        if name != "":
            role, token = self.__get_role(name, password)
            if role != "user" and role != "administrator" and role != "System":
                SuperAdmin.tokenizer(token).set_token()
                return SuperAdmin
            elif role == "System":
                raise TypeError("It is impossible to use the system account")
            else:
                raise TypeError("You don't have enough rights")
        else: 
            raise TypeError("Name cannot be empty")