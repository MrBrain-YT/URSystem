import os
from typing import Union

from utils.validator import ServerChecker, validate_types

class CertsManager:
    server_checker = ServerChecker()
    
    def __init__(self) -> None:
        self.certs = [name for name in os.listdir("certs") if ".crt" in name]
    
    @validate_types 
    def get_certificates(self) -> tuple:
        return {"status": True, "info": "Certs data", "data": self.certs}, 200
    
    @validate_types 
    def get_certificate_path(self, server_token:str, file_name:str) -> Union[str, None]:
        if self.server_checker.is_server_token(server_token):
            if file_name in self.certs:
                return f"certs/{file_name}"
                    