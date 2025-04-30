from flask import Flask, request, jsonify

class LogsManager:
    
    def __init__(self):
        self.loger_module = "URLogs"
    
    def __call__(self, app:Flask) -> Flask:
        from server_functions import User
        from utils.loger import Loger
        from API.access_checker import Access

        access = Access()

        # get log
        @app.route("/GetRobotLogs", methods=['POST'])
        @access.check_user("user", loger_module=self.loger_module)
        def URLog():
            info = request.json
            timestamp = info.get("timestamp")
            if timestamp is not None:
                logs = Loger(robot_name=request.json.get("robot")).get_logs(timestamp)
            else:
                logs = Loger(robot_name=request.json.get("robot")).get_logs()
            User().update_token()
            return jsonify({"status": True, "info": f"The {request.json.get('robot')} robot logs", "data": logs}), 200

        # add new robot log
        @app.route("/AddRobotLog", methods=['POST'])
        @access.check_user("user", loger_module=self.loger_module)
        def AddRobotLog():
            info = request.json
            Loger(robot_name=info.get("robot")).debug(info.get("text"))
            User().update_token()
            return jsonify({"status": True, "info": "Log added"}), 200
        
        # add new system log
        # @app.route("/AddSystemLog", methods=['POST'])
        # @access.check_user("user", loger_module=self.loger_module)
        # def AddSystemLog():
        #     info = request.json
        #     Loger().debug(info.get("module"), info.get("text"))
        #     User().update_token()
        #     return jsonify({"status": True, "info": "Log added"}), 200
        
        # get system logs
        @app.route("/GetSystemLogs", methods=['POST'])
        @access.check_user("administrator", loger_module=self.loger_module)
        def AddSystemLog():
            info = request.json
            User().update_token()
            timestamp = info.get("timestamp")
            if timestamp is not None:
                return jsonify({"status": True, "info": "System logs", "data": Loger().get_logs(timestamp)}), 200
            else:
                return jsonify({"status": True, "info": "System logs", "data": Loger().get_logs()}), 200

        return app