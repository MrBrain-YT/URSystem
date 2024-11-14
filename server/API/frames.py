from flask import Flask, request

from server.server_functions import Robot, System, User

class Frames:
    
    def __init__(self, app:Flask, Robots:dict, tools:dict, frames:dict, users:dict) -> Flask:
        """ URFrames """
        @app.route("/GetFrames", methods=['POST'])
        def GetFrames():
            info = request.form
            if User.role_access(info.get("token"), "administrator", users):
                return str(frames)
            else:
                return "You don't have enough rights"
            
        @app.route("/GetFrame", methods=['POST'])
        def GetFrame():
            info = request.form
            if User.role_access(info.get("token"), "user", users) or Robot.is_robot(info.get("token"), users):
                return str(frames.get(info.get("id")))
            else:
                return "You don't have enough rights"
            
        @app.route("/SetFrame", methods=['POST'])
        def SetFrame():
            info = request.form
            if User.role_access(info.get("token"), "administrator", users) or Robot.is_robot(info.get("token"), users):
                frames[info.get("id")] = info.get("config")
                System.SaveToCache(Robots, tools, frames)
                User.update_token()
                return "True"
            else:
                return "You don't have enough rights"
            
        @app.route("/DelFrame", methods=['POST'])
        def DelFrame():
            info = request.form
            if User.role_access(info.get("token"), "administrator", users):
                del frames[info.get("id")]
                System.SaveToCache(Robots, tools, frames)
                User.update_token()
                return "True"
            else:
                return "You don't have enough rights"
        
        return app