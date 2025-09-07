from typing import Union
import json
import copy

from services.multi_robots_manager import MultiRobotsManager
from utils.validator import RobotChecker, UserChecker
from configuration.cache.file_cache import save_to_cache
from services.robot_manager import RobotManager

def message_handler(message:str) -> Union[str, int]:
    """ If this function return:\n
        0 - close websocket connection\n
        1 - no send message\n
        2 - shutdown server\n
        str - send string message
    """
    # prepare robots data
    robots_copyed = copy.deepcopy(MultiRobotsManager().get_robots())
    for robot_name in robots_copyed.keys():
        del robots_copyed[robot_name]["SecureCode"]
        del robots_copyed[robot_name]["ProgramToken"]

    json_message = json.loads(message)
    if "token" in json_message:
        token = json_message["token"]
        if RobotChecker().is_robot(token):
            robot_name = UserChecker().get_robot_name(token)
            if "type" in json_message:
                if json_message["type"] == "set":
                    if "parameter" in json_message and "value" in json_message:
                        if json_message["parameter"] == "MotorsPosition":
                            if isinstance(json_message["value"], dict):
                                RobotManager().set_motors_position(robot_name=robot_name, angles=json_message["value"], token=token)
                            return 1
                        
                        elif json_message["parameter"] == "RobotReady":
                            if isinstance(json_message["value"], bool):
                                responce, code = RobotManager().set_ready_state(robot_name=robot_name, state=json_message["value"], token=token)
                                return json.dumps(responce)
                            return 1
                        
                        elif json_message["parameter"] == "PositionID" or json_message["parameter"] == "trigger":
                            if isinstance(json_message["value"], str):
                                RobotManager().set_position_id(robot_name=robot_name, position_id=json_message["value"], token=token)
                            return 1
                        
                        else:
                            return 1
                    else:
                        return 1 
                elif json_message["type"] == "command":
                    if json_message["name"] == "remove-position-point":
                        RobotManager().remove_current_point_position(robot_name=robot_name, token=token)
                        return 1
                    elif json_message["name"] == "remove-position-points":
                        RobotManager().remove_all_point_position(robot_name=robot_name, token=token)
                        return 1
                    elif json_message["name"] == "remove-speed-point":
                        RobotManager().remove_current_point_speed(robot_name=robot_name, token=token)
                        return 1
                    elif json_message["name"] == "remove-speed-points":
                        RobotManager().remove_all_point_speed(robot_name=robot_name, token=token)
                        return 1
                else:
                    return json.dumps(robots_copyed[robot_name])
            else:
                return json.dumps(robots_copyed[robot_name])
        
        elif UserChecker().role_access(token, "SuperAdmin"):
            if "type" in json_message:
                if json_message["type"] == "shutdown":
                    return 2
            return 1
        elif UserChecker().role_access(token, "user"):
            return json.dumps(robots_copyed)
        else:
            return 0
    else:
        return 0