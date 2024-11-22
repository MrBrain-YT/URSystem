from flask import Flask, request

class LogsManager:
    
    def __call__(self, app:Flask, loger) -> Flask:
        from server_functions import User
        from utils.loger import Robot_loger
        from API.multi_robots_system import URMSystem
        from API.access_checker import Access

        access = Access(Loger=loger)

        # get log
        @app.route("/URLog", methods=['POST'])
        @access.check_user("user")
        def URLog():
            robots:dict = URMSystem().get_robots()
            User().update_token()
            return robots[request.form.get("Robot")]["Logs"] 

        # add new log
        @app.route("/URLogs", methods=['POST'])
        @access.check_user("user")
        def URLogs():
            info = request.form
            Robot_loger(info.get("Robot")).debug(info.get("Text"))
            User().update_token()
            return "True"

        return app