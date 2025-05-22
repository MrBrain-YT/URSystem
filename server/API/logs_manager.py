from flask import Flask, request, jsonify

from API.access_checker import Access
from services.logs_manager import LogsManager

class LogsManagerAPI:
    access = Access()
    
    
    def __init__(self):
        self.logger_module = "URLogs"
        self.logs_manager = LogsManager()
    
    def __call__(self, app:Flask) -> Flask:
        # get log
        @app.route("/get-robot-logs", methods=['POST'])
        @self.access.check_user("user", logger_module=self.logger_module)
        def get_robot_log():
            info = request.json
            robot_name = info.get("robot")
            timestamp = info.get("timestamp")
            responce, code = self.logs_manager.get_robot_log(robot_name=robot_name, timestamp=timestamp)
            return jsonify(responce), code

        # add new robot log
        @app.route("/add-robot-log", methods=['POST'])
        @self.access.check_user("user", logger_module=self.logger_module)
        def add_robot_debug_log():
            info = request.json
            robot_name = info.get("robot")
            message = info.get("text")
            responce, code = self.logs_manager.add_robot_debug_log(robot_name=robot_name, message=message)
            return jsonify(responce), code
        
        # add new system log
        @app.route("/add-system-log", methods=['POST'])
        @self.access.check_user("administrator", logger_module=self.logger_module)
        def add_system_debug_log():
            info = request.json
            module = info.get("module")
            message = info.get("text")
            responce, code = self.logs_manager.add_system_debug_log(module=module, message=message)
            return jsonify(responce), code
        
        # get system logs
        @app.route("/get-system-logs", methods=['POST'])
        @self.access.check_user("administrator", logger_module=self.logger_module)
        def get_system_log():
            info = request.json
            timestamp = info.get("timestamp")
            responce, code = self.logs_manager.get_system_log(timestamp=timestamp)
            return jsonify(responce), code

        return app