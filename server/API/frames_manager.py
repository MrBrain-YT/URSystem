from flask import Flask, request, jsonify

from services.frames_manager import FramesManager
from API.access_checker import Access

class FramesManagerAPI:
    access = Access()
    
    def __init__(self, frames: dict=None):
        self.logger_module = "URFrames"
        if frames is not None:
            self.frames_manager = FramesManager(frames)
        else:
            self.frames_manager = FramesManager()
    
    def __call__(self, app:Flask) -> Flask:

        @app.route("/get-frames", methods=['POST'])
        @self.access.check_user(user_role="administrator", logger_module=self.logger_module)
        def get_frames():
            responce, code = self.frames_manager.get_frames_api()
            return jsonify(responce), code
            
        @app.route("/get-frame", methods=['POST'])
        @self.access.check_robot_or_user(user_role="user", logger_module=self.logger_module)
        def get_frame():
            info = request.json
            frame_id = info.get("id")
            responce, code = self.frames_manager.get_frame(frame_id=frame_id)
            return jsonify(responce), code
            
        @app.route("/set-frame", methods=['POST'])
        @self.access.check_robot_or_user(user_role="administrator", logger_module=self.logger_module)
        def set_frame():
            info = request.json
            frame_id = info.get("id")
            config = info.get("config")
            responce, code = self.frames_manager.set_frame(frame_id=frame_id, config=config)
            return jsonify(responce), code
            
        @app.route("/delete-frame", methods=['POST'])
        @self.access.check_user(user_role="administrator", logger_module=self.logger_module)
        def delete_frame():
            info = request.json
            frame_id = info.get("id")
            responce, code = self.frames_manager.delete_frame(frame_id=frame_id)
            return jsonify(responce), code
        
        return app