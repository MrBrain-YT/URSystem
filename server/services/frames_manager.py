from typing import Any

from utils.user_updater import update_token
from configuration.cache.file_cache import save_to_cache

frames = {}

class FramesManager:
    frames = frames
    
    def __init__(self, frames: dict=None) -> None:
        if frames is not None:
            self.frames.update(frames)
        
    def get_frames(self) -> dict:
        return self.frames
    
    def set_frames(self, frames: dict) -> None:
        self.frames.update(frames)

    def get_frames_api(self) -> tuple:
        return {"status": True, "info": f"All frames", "data": self.frames}, 200

    def get_frame(self, frame_id:str) -> tuple:
        if self.frames.get(frame_id) is not None:
            return {"status": True, "info": f"Value from frame with id {frame_id}", "data": self.frames.get(frame_id)}, 200
        else:
            return {"status": False, "info": f"Frame '{frame_id}' not found"}, 400

    def set_frame(self, frame_id:str, config:Any) -> tuple:
        self.frames[frame_id] = config
        save_to_cache(frames=self.frames)
        update_token()
        return {"status": True, "info": f"The value has been changed in frame with id {frame_id}"}, 200

    def delete_frame(self, frame_id:str) -> tuple:
        if self.frames.get(frame_id) is not None:
            del self.frames[frame_id]
            save_to_cache(frames=self.frames)
            update_token()
            return {"status": True, "info": f"Frame with id {frame_id} has ben deleted"}, 200
        else:
            return {"status": False, "info": f"Frame not found"}, 400
    
    def create_frame(self, frame_id:str) -> tuple:
        print(self.frames)
        if self.frames.get(frame_id) is None:
            self.frames[frame_id] = {}
            save_to_cache(frames=self.frames)
            update_token()
            return {"status": True, "info": f"Frame with id {frame_id} has ben deleted"}, 200
        else:
            return {"status": False, "info": f"Frame already was created"}, 400