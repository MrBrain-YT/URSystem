from flask import Flask, request, jsonify

from services.bases_manager import BasesManager
from API.access_checker import Access

class BasesManagerAPI:
    access = Access()
    
    def __init__(self, bases:dict) -> None:
        self.logger_module = "URBases"
        if bases is not None:
            self.bases_manager = BasesManager(bases)
        else:
            self.bases_manager = BasesManager()

    def __call__(self, app:Flask) -> Flask:

        @app.route("/get-bases", methods=['POST'])
        @self.access.check_user(user_role="administrator", logger_module=self.logger_module)
        def get_bases():
            responce, code = self.bases_manager.get_bases_api()
            return jsonify(responce), code
        
        @app.route("/get-base", methods=['POST'])
        @self.access.check_robot_or_user(user_role="user", logger_module=self.logger_module)
        def get_base():
            info = request.json
            base_name = info.get("id")
            responce, code = self.bases_manager.get_base(base_name=base_name)
            return jsonify(responce), code
        
        @app.route("/create-base", methods=['POST'])
        @self.access.check_user(user_role="administrator", logger_module=self.logger_module)
        def create_base():
            info = request.json
            base_name = info.get("id")
            responce, code = self.bases_manager.create_base(base_name=base_name)
            return jsonify(responce), code
        
        @app.route("/set-base", methods=['POST'])
        @self.access.check_user(user_role="administrator", logger_module=self.logger_module)
        def set_base():
            info = request.json
            base_name = info.get("id")
            base_data = info.get("data")
            responce, code = self.bases_manager.set_base_data(base_name=base_name, base_data=base_data)
            return jsonify(responce), code 
        
        @app.route("/delete-base", methods=['POST'])
        @self.access.check_user(user_role="administrator", logger_module=self.logger_module)
        def delete_base():
            info = request.json
            base_name = info.get("id")
            responce, code = self.bases_manager.delete_base(base_name=base_name)
            return jsonify(responce), code 
        
        return app