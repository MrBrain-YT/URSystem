import os

def save_to_cache(robots:dict=None, tools:dict=None, bases:dict=None, frames:dict=None) -> None:
    from services.multi_robots_manager import MultiRobotsManager
    from services.frames_manager import FramesManager
    from services.tools_manager import ToolsManager
    from services.bases_manager import BasesManager
    try:
        os.remove("./configuration/cache/robots_cache.py")
    except:
        return None
    with open("./configuration/cache/robots_cache.py", "w") as file:
        file.write(f"robots = {robots if robots is not None else MultiRobotsManager().get_robots()}")
        file.write(f"\ntools = {tools if tools is not None else ToolsManager().get_tools()}")
        file.write(f"\nbases = {bases if bases is not None else BasesManager().get_bases()}")
        file.write(f"\nframes = {frames if frames is not None else FramesManager().get_frames()}")
    if robots is not None:
        MultiRobotsManager().set_robots(robots)
    if tools is not None:
        ToolsManager().set_tools(tools)
    if frames is not None:
        FramesManager().set_frame(frames)