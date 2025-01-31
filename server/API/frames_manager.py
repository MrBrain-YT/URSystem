import json

from flask import Flask, request

class FramesManager:
    
    def __init__(self, frames: dict=None):
        self.loger_module = "URFrames"
        if frames is not None:
            globals()["frames"] = frames
        
    def get_frames(self) -> dict:
        return globals()["frames"]
    
    def set_frame(self, frames: dict) -> None:
        globals()["frames"] = frames
    
    def __call__(self, app:Flask) -> Flask:
        from server_functions import System, User
        from API.access_checker import Access

        access = Access()
        
        """ URFrames """
        @app.route("/GetFrames", methods=['POST'])
        @access.check_user(user_role="administrator", loger_module=self.loger_module)
        def GetFrames():
            return json.dumps({"status": True, "info": f"All frames", "data": globals()["frames"]}), 200

            
        @app.route("/GetFrame", methods=['POST'])
        @access.check_robot_or_user(user_role="user")
        def GetFrame():
            info = request.form
            if globals()["frames"].get(info.get("id")) is not None:
                return json.dumps({"status": True, "info": f"Value from frame with id {info.get('id')}", "data": globals()["frames"].get(info.get("id"))}), 200
            else:
                return json.dumps({"status": False, "info": f"Frame '{info.get('id')}' not found"}), 400
            
        @app.route("/SetFrame", methods=['POST'])
        @access.check_robot_or_user(user_role="administrator")
        def SetFrame():
            info = request.form
            globals()["frames"][info.get("id")] = info.get("config")
            System().SaveToCache(frames=globals()["frames"])
            User().update_token()
            return json.dumps({"status": True, "info": f"The value has been changed in frame with id {info.get('id')}"}), 200

            
        @app.route("/DelFrame", methods=['POST'])
        @access.check_user(user_role="administrator", loger_module=self.loger_module)
        def DelFrame():
            info = request.form
            del globals()["frames"][info.get("id")]
            System().SaveToCache(frames=globals()["frames"])
            User().update_token()
            return json.dumps({"status": True, "info": f"Frame with id {info.get('id')} has ben deleted"}), 200

        
        return app