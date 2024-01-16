import json

import requests

class Robot():
    
    def __init__(self, host:str, port:int, token:str) -> None:
        self.__host = host
        self.__port = port
        self.__token = token

    def ptp(self, robot_name:str , angles:list, code:str) -> None:
        url = f"https://{self.__host}:{str(self.__port)}/CurentPosition"
        data = {
            "Robot": robot_name,
            "token": self.__token,
            "Code" : code
            }
        for i in range(1, len(angles)+1):
            data[f"J{i}"] = angles[i-1]
        requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False)))

    def lin(self, robot_name:str, angles:list, code:str) -> None:
        # Lin robot moving
        url = "https://127.0.0.1:5000/GetRobot"
        data = {
            "Robot": robot_name,
            "token": self.__token
            }
        resp = requests.post(url, verify=False, data=json.loads(json.dumps(data, ensure_ascii=False))).text
        angles_diff = [abs(i - int(json.loads(str(json.loads(resp.replace("'", '"'))["Position"]).replace("'", '"'))["J1"])) for i in angles]
        maxAng = max(angles_diff)

        # send current position
        url = f"https://{self.__host}:{str(self.__port)}/CurentPosition"
        data = {
            "Robot": robot_name,
            "token": self.__token,
            "Code" : code
            }
        for i in range(1, len(angles)+1):
            data[f"J{i}"] = angles[i-1]
        requests.post(url,  verify=True,data=json.loads(json.dumps(data, ensure_ascii=False)))

        # send current speed
        url = f"https://{self.__host}:{str(self.__port)}/CurentSpeed"
        data = {
            "Robot": robot_name,
            "token": self.__token,
            "Code" : code
            }
        for i in range(1, len(angles)+1):
            data[f"J{i}"] = angles_diff[i-1]/maxAng
        requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False)))


    def circ(self, code:str) -> None:
        pass

    def get_log(self, robot_name:str) -> str:
        url = f"https://{self.__host}:{str(self.__port)}/URLog"
        data = {
            "Robot": robot_name,
            "token": self.__token
            }
        return requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text

    def get_last_log(self, robot_name:str) -> str:
        url = f"https://{self.__host}:{str(self.__port)}/URLog"
        data = {
            "Robot": robot_name,
            "token": self.__token
            }
        return requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text.split("\n")[-1]
    
    def debug(self,robot_name:str , text:str) -> str:
        url = f"https://{self.__host}:{str(self.__port)}/URLogs"
        data = {
            "Robot": robot_name,
            "Type": "DEBUG",
            "Text": text
            }
        return requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text
    
    
    def set_program(self, robot_name:str , program:str, code:str) -> str:
        url = f"https://{self.__host}:{str(self.__port)}/SetProgram"
        data = {
            "Robot": robot_name,
            "Program": program.encode().hex(),
            "token": self.__token,
            "Code" : code
            }
        return requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text
    
    def delete_program(self, robot_name:str, code:str) -> str:
        url = f"https://{self.__host}:{str(self.__port)}/DeleteProgram"
        data = {
            "Robot": robot_name,
            "token": self.__token,
            "Code" : code
            }
        return requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text

    
    
    