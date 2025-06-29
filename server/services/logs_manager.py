from typing import Union

from utils.user_updater import update_token
from utils.logger import Logger
from utils.validator import validate_types

class LogsManager:
    logger = Logger()
    
    def __init__(self) -> None:
        pass
 
    # get log
    @validate_types 
    def get_robot_log(self, robot_name:str, timestamp:int=None) -> tuple:
        if timestamp is not None:
            logs = Logger(robot_name=robot_name).get_logs(timestamp)
        else:
            logs = Logger(robot_name=robot_name).get_logs()
        update_token()
        return {"status": True, "info": f"The {robot_name} robot logs", "data": logs}, 200

    # add new robot log
    @validate_types 
    def add_robot_debug_log(self, robot_name:str, message:str) -> tuple:
        Logger(robot_name=robot_name).debug(message)
        update_token()
        return {"status": True, "info": "Log added"}, 200
    
    # add new system log
    @validate_types 
    def add_system_debug_log(self, module:str, message) -> tuple:
        self.logger.debug(module=module, msg=message)
        update_token()
        return {"status": True, "info": "Log added"}, 200
    
    # get system logs
    @validate_types 
    def get_system_log(self, timestamp:int=None) -> tuple:
        if timestamp is not None:
            logs = Logger().get_logs(timestamp)
        else:
            logs = Logger().get_logs()
        update_token()
        return {"status": True, "info": f"System logs", "data": logs}, 200
