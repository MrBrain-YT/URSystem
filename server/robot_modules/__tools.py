import json
import requests

class Tools():
    # tool creation is located in the admin console
    def __init__(self, host:str, port:str, token:str) -> None:
        self.host = host
        self.port = port
        self.token = token


    def get_tool_info(self, name:str) -> str:
        url = f"https://{self.host}:{self.port}/URTool"
        data = {
            "Id": name,
            "Type": "",
            "token": self.token
            }
        return requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text
    
    def set_tool_info(self, name:str, cfg:str) -> str:
        url = f"https://{self.host}:{self.port}/URTool"
        data = {
            "Id": name,
            "Type": "write",
            "Cfg": cfg,
            "token": self.token
            }
        return requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text