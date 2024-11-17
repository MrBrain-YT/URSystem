from flask import Flask, request

class LogsManager:
    
    def __call__(self, app:Flask, Robots:dict) -> Flask:
        from server_functions import User
        from utils.loger import Robot_loger

        # get log
        @app.route("/URLog", methods=['POST'])
        def URLog():
            if User.role_access(request.form.get("token"), "user"):
                User().update_token()
                return Robots[request.form.get("Robot")]["Logs"] 
            else:
                return "You are not on the users list"

        # add new log
        @app.route("/URLogs", methods=['POST'])
        def URLogs():
            info = request.form
            if User.role_access(info.get("token"), "user"):
                    Robot_loger(info.get("Robot")).debug(info.get("Text"))
                    User().update_token()
                    return "True"
            else:
                return "You are not on the users list"
        
        return app