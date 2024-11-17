from flask import Flask, request

class FramesManager:
    
    def __init__(self, frames: dict=None):
        if frames is not None:
            globals()["frames"] = frames
        
    def get_frames(self) -> dict:
        return globals()["frames"]
    
    def set_frame(self, frames: dict) -> None:
        globals()["frames"] = frames
    
    def __call__(self, app:Flask) -> Flask:
        from server_functions import Robot, System, User
        """ URFrames """
        @app.route("/GetFrames", methods=['POST'])
        def GetFrames():
            info = request.form
            if User.role_access(info.get("token"), "administrator"):
                return str(globals()["frames"])
            else:
                return "You don't have enough rights"
            
        @app.route("/GetFrame", methods=['POST'])
        def GetFrame():
            info = request.form
            if User.role_access(info.get("token"), "user") or Robot.is_robot(info.get("token")):
                return str(globals()["frames"].get(info.get("id")))
            else:
                return "You don't have enough rights"
            
        @app.route("/SetFrame", methods=['POST'])
        def SetFrame():
            info = request.form
            if User.role_access(info.get("token"), "administrator") or Robot.is_robot(info.get("token")):
                globals()["frames"][info.get("id")] = info.get("config")
                System().SaveToCache(frames=globals()["frames"])
                User().update_token()
                return "True"
            else:
                return "You don't have enough rights"
            
        @app.route("/DelFrame", methods=['POST'])
        def DelFrame():
            info = request.form
            if User.role_access(info.get("token"), "administrator"):
                del globals()["frames"][info.get("id")]
                System().SaveToCache(frames=globals()["frames"])
                User().update_token()
                return "True"
            else:
                return "You don't have enough rights"
        
        return app