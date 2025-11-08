import ast
import secrets
import os
import copy

import sqlalchemy as db

from utils.logger import Logger
from utils.validator import RobotChecker, FramesChecker, BasesChecker, ToolsChecker, validate_types
from databases.connection import users_table
from databases.database_manager import DBWorker
from configuration.cache.file_cache import save_to_cache
from utils.user_updater import update_token
from services.frames_manager import FramesManager
from services.tools_manager import ToolsManager
from services.accounts_manager import AccountManager
from services.bases_manager import BasesManager

robots = {}

class MultiRobotsManager:
    robots = robots
    logger = Logger()
    frames_manager = FramesManager()
    tools_manager = ToolsManager()
    account_manager = AccountManager()
    bases_manager = BasesManager()
    robot_checker = RobotChecker()
    frames_checker = FramesChecker()
    bases_checker = BasesChecker()
    tools_checker = ToolsChecker()
    robot_name_finder = RobotChecker.robot_name_finder
    
    def __init__(self, robots:dict=None) -> None:
        self.logger_module = "URMSystem"
        if robots is not None:
            self.robots.update(robots)
            save_to_cache(robots=robots)
            
    def set_robots(self, robots: dict):
        self.robots.update(robots)
        
    def get_robots(self) -> dict:
        return self.robots

    # add robot
    @validate_types 
    def create_robot(self, robot_name:str, angle_count:int, secret_code:str, password:str, kinematic_id:str=None) -> tuple:
        from services.robot_manager import RobotManager
        
        if not self.robot_checker.robot_exists(robot_name):
            # create robot configuretion
            angles = {}
            for i in range(1, int(angle_count)+1):
                angles[f"J{i}"] = 0.0
            self.robots[robot_name] = {
                    "AngleCount" : angle_count,
                    "Tool" : "",
                    "Base" : "",
                    "Position" : angles.copy(),
                    "PositionID" : "",
                    "HomePosition" : angles.copy(),
                    "MotorsPosition" : angles.copy(),
                    "MotorsSpeed" : angles.copy(),
                    "StandardSpeed" : angles.copy(),
                    "PhysicalSpeed" : angles.copy(),
                    "MinAngles" : angles.copy(),
                    "MaxAngles" : angles.copy(),
                    "Program" : "", 
                    "ProgramRunning" : False,
                    "ProgramToken" : "", 
                    "Kinematic" : f"{kinematic_id}" if kinematic_id != None else None,
                    "RobotReady" : True,
                    "Emergency" : False,
                    "SecureCode":  secret_code if secret_code != None else "",
                    "XYZposition" : {
                        "x": 0.0,
                        "y": 0.0,
                        "z": 0.0,
                        "a": 0.0,
                        "b": 0.0,
                        "c": 0.0,
                        }
                    }
            account_data = self.account_manager.create_account(robot_name, password, "robot")[0]["data"]
            token = account_data["token"]
            
            save_to_cache(robots=self.robots)
            update_token()
            RobotManager().add_new_robot_ready(robot_name=robot_name)
            log_message = f"Robot named {robot_name} was created"
            self.logger.info(module=self.logger_module, msg=log_message)
            return {"status": True, "info": log_message, "token": token}, 200
        else:
            log_message = f"The robot `{robot_name}` already exists"
            self.logger.info(module=self.logger_module, msg=log_message)
            return {"status": False, "info": log_message}, 400

    # Import robot cache
    @validate_types 
    def import_cache(self, import_robots:dict, import_tools:dict, import_frames:dict, import_bases:dict) -> tuple:
        from services.robot_manager import RobotManager
        
        frames:dict = self.frames_manager.get_frames()
        users:dict = self.account_manager.get_users()
        tools:dict = self.tools_manager.get_tools()
        bases:dict = self.bases_manager.get_bases()
        robots_new_password = {}
        # import robots
        for robot_name in import_robots.keys():
            if self.robot_checker.robot_exists(robot_name):
                pass
            else:
                self.robots[robot_name] = import_robots[robot_name]
                # creating account for imported robot
                while True:
                    token = secrets.token_hex(32)
                    tokens = []
                    for i in [i for i in users]:
                        tokens.append(users.get(i)["token"])
                    if token not in tokens:
                        break
                    
                password = secrets.token_hex(10)
                query = db.insert(users_table).values(name=robot_name, password=password, role="robot", token=token)
                DBWorker().send_query(query=query)
                robots_new_password[robot_name] = password
                try:
                    os.mkdir(f'Logs/{robot_name}')
                except:
                    pass
                RobotManager().add_new_robot_ready(robot_name=robot_name)
                
        # import tools
        for tool_name in import_tools.keys():
            if self.tools_checker.tool_exists(tool_name):
                pass
            else:
                tools[tool_name] = import_tools[tool_name]
                
        # import frames
        for frames_name in import_frames.keys():
            if self.frames_checker.frame_exists(frames_name):
                pass
            else:
                frames[frames_name] = import_frames[frames_name]
        
        # import bases
        for base_name in import_bases.keys():
            if self.bases_checker.base_exists(base_name):
                pass
            else:
                bases[base_name] = import_bases[base_name]
                
        save_to_cache(robots=self.robots, tools=tools, frames=frames, bases=bases)
        log_message = "Cache was imorted"
        self.logger.info(module=self.logger_module, msg=log_message)
        return {"status": True, "info": log_message, "data": {"passwords" : robots_new_password}}, 200
        
    # Export robot cache from cache file
    def export_file_cache(self) -> tuple:
        with open("./configuration/cache/robots_cache.py", "r") as file:
            cache = file.read()

        new_cache = {
            "robots": ast.literal_eval(cache.split("\n")[0].lstrip("robots = ")),
            "tools": ast.literal_eval(cache.split("\n")[1].lstrip("tools = ")),
            "bases": ast.literal_eval(cache.split("\n")[2].lstrip("bases = ")),
            "frames": ast.literal_eval(cache.split("\n")[3].lstrip("frames = "))
        }
        for robot_name in new_cache["robots"].keys():
            del new_cache["robots"][robot_name]["ProgramToken"]
        
        self.logger.info(module=self.logger_module, msg="Current cache from cache file was exported")
        return {"status": True, "info": "Current cache from cache file", "data": new_cache}, 200
    
    # Export robot cache from RAM
    def export_ram_cache(self) -> tuple:
        frames:dict = copy.deepcopy(self.frames_manager.get_frames())
        tools:dict = copy.deepcopy(self.tools_manager.get_tools())
        bases:dict = copy.deepcopy(self.bases_manager.get_bases())
        robots = copy.deepcopy(self.robots)
        for robot_name in robots.keys():
            del robots[robot_name]["ProgramToken"]

        new_cache = {
            "robots": robots,
            "tools": tools,
            "bases": bases,
            "frames": frames,
        }
        self.logger.info(module=self.logger_module, msg="Current cache from RAM was exported")
        return {"status": True, "info": "Current cache from RAM", "data": new_cache}, 200

    # get robot
    @robot_name_finder
    @validate_types 
    def get_robot(self, robot_name:str) -> tuple:
        robots:dict = copy.deepcopy(self.robots)
        update_token()
        result = robots[robot_name] if robot_name in robots.keys() else None
        if result is not None:
            result.pop("ProgramToken", None)
            return {"status": True, "info": "Get robot data", "data": result}, 200
        else:
            return {"status": False, "info": "Robot not found"}, 400
        
    # get robots
    def get_robots_api(self) -> tuple:
        robots:dict = copy.deepcopy(self.robots)
        update_token()
        for robot_name in robots.keys():
            robots[robot_name].pop("ProgramToken", None)
        return {"status": True, "info": "All robots data", "data": robots}, 200

    # delete robot
    @validate_types 
    def delete_robot(self, robot_name:str) -> tuple:
        from services.robot_manager import RobotManager
        
        if self.robot_checker.robot_exists(robot_name):
            del self.robots[robot_name]
            RobotManager().remove_new_robot_ready(robot_name=robot_name)
            query = users_table.delete().where(db.and_(
                users_table.columns.name == robot_name,
                users_table.columns.role == "robot"))
            DBWorker().send_query(query=query)
            
            update_token()
            save_to_cache(robots=self.robots)
            self.logger.info(module=self.logger_module, msg=f"Robot was deleted user with token: {robot_name}")
            return {"status": True, "info": f"Robot '{robot_name}' was deleted"}, 200
        else:
            update_token()
            self.logger.info(module=self.logger_module, msg=f"Robot did not deleted user with token: {robot_name}")
            return {"status": False, "info": "Robot not found"}, 400