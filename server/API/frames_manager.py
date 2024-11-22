from flask import Flask, request

class FramesManager:
    
    def __init__(self, frames: dict=None):
        if frames is not None:
            globals()["frames"] = frames
        
    def get_frames(self) -> dict:
        return globals()["frames"]
    
    def set_frame(self, frames: dict) -> None:
        globals()["frames"] = frames
    
    def __call__(self, app:Flask, loger) -> Flask:
        from server_functions import Robot, System, User
        from API.access_checker import Access

        access = Access(Loger=loger)
        
        """ URFrames """
        @app.route("/GetFrames", methods=['POST'])
        @access.check_user(user_role="administrator")
        def GetFrames():
            return str(globals()["frames"])

            
        @app.route("/GetFrame", methods=['POST'])
        @access.check_robot_or_user(user_role="user")
        def GetFrame():
            info = request.form
            return str(globals()["frames"].get(info.get("id")))
            
        @app.route("/SetFrame", methods=['POST'])
        @access.check_robot_or_user(user_role="administrator")
        def SetFrame():
            info = request.form
            globals()["frames"][info.get("id")] = info.get("config")
            System().SaveToCache(frames=globals()["frames"])
            User().update_token()
            return "True"

            
        @app.route("/DelFrame", methods=['POST'])
        @access.check_user(user_role="administrator")
        def DelFrame():
            info = request.form
            del globals()["frames"][info.get("id")]
            System().SaveToCache(frames=globals()["frames"])
            User().update_token()
            return "True"

        
        return app