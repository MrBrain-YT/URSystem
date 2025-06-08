from flask import Blueprint, request, jsonify

from services.bases_manager import BasesManager
from api.access_checker import Access

class BasesManagerAPI:
    access = Access()
    
    def __init__(self, bases:dict) -> None:
        self.logger_module = "URBases"
        if bases is not None:
            self.bases_manager = BasesManager(bases)
        else:
            self.bases_manager = BasesManager()

    def __call__(self) -> Blueprint:

        bases_bp = Blueprint("bases_api", __name__, url_prefix="/api")

        @bases_bp.route("/get-bases", methods=['POST'])
        @self.access.check_robot_or_user(user_role="user", logger_module=self.logger_module)
        def get_bases():
            response, code = self.bases_manager.get_bases_api()
            return jsonify(response), code
        
        @bases_bp.route("/get-base", methods=['POST'])
        @self.access.check_robot_or_user(user_role="user", logger_module=self.logger_module)
        def get_base():
            info = request.json
            base_name = info.get("id")
            response, code = self.bases_manager.get_base(base_name=base_name)
            return jsonify(response), code
        
        @bases_bp.route("/create-base", methods=['POST'])
        @self.access.check_user(user_role="administrator", logger_module=self.logger_module)
        def create_base():
            info = request.json
            base_name = info.get("id")
            response, code = self.bases_manager.create_base(base_name=base_name)
            return jsonify(response), code
        
        @bases_bp.route("/set-base", methods=['POST'])
        @self.access.check_user(user_role="administrator", logger_module=self.logger_module)
        def set_base():
            info = request.json
            base_name = info.get("id")
            base_data = info.get("data")
            response, code = self.bases_manager.set_base_data(base_name=base_name, base_data=base_data)
            return jsonify(response), code 
        
        @bases_bp.route("/delete-base", methods=['POST'])
        @self.access.check_user(user_role="administrator", logger_module=self.logger_module)
        def delete_base():
            info = request.json
            base_name = info.get("id")
            response, code = self.bases_manager.delete_base(base_name=base_name)
            return jsonify(response), code 
        
        return bases_bp