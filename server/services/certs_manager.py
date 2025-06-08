import os

from configuration.server_token import reg_token

class CertsManager:
    
    def __init__(self) -> None:
        self.certs = [name for name in os.listdir("certs") if ".crt" in name]
        
    def get_certificates(self) -> tuple:
        return {"status": True, "info": "Certs data", "data": self.certs}, 200
    
    def get_certificate_path(self, server_token:str, file_name:str) -> str:
        if server_token == reg_token:
            if file_name in self.certs:
                return f"certs/{file_name}"
                    