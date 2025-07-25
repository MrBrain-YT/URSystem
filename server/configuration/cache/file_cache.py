import os
import json
import sys

def save_to_cache(robots:dict=None, tools:dict=None, bases:dict=None, frames:dict=None) -> None:
    from services.multi_robots_manager import MultiRobotsManager
    from services.frames_manager import FramesManager
    from services.tools_manager import ToolsManager
    from services.bases_manager import BasesManager
    
    if "pytest" in sys.modules:
        config_path = "./configuration/cache/auto_test/robots_cache.py"
    else:
        config_path = "./configuration/cache/robots_cache.py"
        
    with open(config_path, "w") as file:
        file.write(f"robots = {robots if robots is not None else MultiRobotsManager().get_robots()}")
        file.write(f"\ntools = {tools if tools is not None else ToolsManager().get_tools()}")
        file.write(f"\nbases = {bases if bases is not None else BasesManager().get_bases()}")
        file.write(f"\nframes = {frames if frames is not None else FramesManager().get_frames()}")
    if robots is not None:
        MultiRobotsManager().set_robots(robots)
        os.environ["ROBOTS"] = json.dumps(robots)
    if tools is not None:
        ToolsManager().set_tools(tools)
        os.environ["TOOLS"] = json.dumps(tools)
    if frames is not None:
        FramesManager().set_frames(frames)
        os.environ["FRAMES"] = json.dumps(frames)
    if bases is not None:
        BasesManager().set_bases(bases)
        os.environ["BASES"] = json.dumps(bases)