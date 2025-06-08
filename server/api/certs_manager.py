from flask import Blueprint, jsonify, send_file, request

from services.certs_manager import CertsManager
from api.access_checker import Access

class CertsManagerAPI:
    access = Access()
    
    def __init__(self) -> None:
        self.logger_module = "URCerts"
        self.certs_manager = CertsManager()

    def __call__(self) -> Blueprint:
        
        certs_bp = Blueprint("certs_api", __name__, url_prefix="/api")

        @certs_bp.post("/get-certs")
        @self.access.check_user(user_role="user", logger_module=self.logger_module)
        def get_certs():
            response, code = self.certs_manager.get_certificates()
            return jsonify(response), code
        
        @certs_bp.post("/api/download-cert")
        def download_cert():
            info = request.json
            token = info.get("server_token")
            file_name = info.get("file_name")
            file_path = self.certs_manager.get_certificate_path(
                server_token=token,
                file_name=file_name
            )
            return send_file(file_path, as_attachment=True)
        
        return certs_bp