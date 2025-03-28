from flask import Flask, request, jsonify

class LogsManager:
    
    def __init__(self):
        self.loger_module = "URLogs"
    
    def __call__(self, app:Flask) -> Flask:
        from server_functions import User
        from utils.loger import Robot_loger, Loger
        from API.multi_robots_system import URMSystem
        from API.access_checker import Access

        access = Access()

        # get log
        @app.route("/GetRobotLogs", methods=['POST'])
        @access.check_user("user", loger_module=self.loger_module)
        def URLog():
            robots:dict = URMSystem().get_robots()
            User().update_token()
            return jsonify({"status": True, "info": f"The {request.json.get('Robot')} robot logs", "data": robots[request.json.get("Robot")]["Logs"]}), 200

        # add new robot log
        @app.route("/AddRobotLog", methods=['POST'])
        @access.check_user("user", loger_module=self.loger_module)
        def AddRobotLog():
            info = request.json
            Robot_loger(info.get("Robot")).debug(info.get("text"))
            User().update_token()
            return jsonify({"status": True, "info": "Log added"}), 200
        
        # add new system log
        @app.route("/AddSystemLog", methods=['POST'])
        @access.check_user("user", loger_module=self.loger_module)
        def AddSystemLog():
            info = request.json
            Loger().debug(info.get("module"), info.get("text"))
            User().update_token()
            return jsonify({"status": True, "info": "Log added"}), 200

        return app