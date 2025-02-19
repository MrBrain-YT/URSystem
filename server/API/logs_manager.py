from flask import Flask, request, jsonify

class LogsManager:
    
    def __init__(self):
        self.loger_module = "URLogs"
    
    def __call__(self, app:Flask) -> Flask:
        from server_functions import User
        from utils.loger import Robot_loger
        from API.multi_robots_system import URMSystem
        from API.access_checker import Access

        access = Access()

        # get log
        @app.route("/URLog", methods=['POST'])
        @access.check_user("user", loger_module=self.loger_module)
        def URLog():
            robots:dict = URMSystem().get_robots()
            User().update_token()
            return jsonify({"status": True, "info": f"The {request.json.get('Robot')} robot logs", "data": robots[request.json.get("Robot")]["Logs"]}), 200

        # add new log
        @app.route("/URLogs", methods=['POST'])
        @access.check_user("user", loger_module=self.loger_module)
        def URLogs():
            info = request.json
            Robot_loger(info.get("Robot")).debug(info.get("Text"))
            User().update_token()
            return jsonify({"status": True, "info": "Log added"}), 200

        return app