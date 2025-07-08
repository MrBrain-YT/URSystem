from typing import Union, get_type_hints, Any, get_args
from functools import wraps

import sqlalchemy as db

from databases.connection import users_table
from databases.database_manager import DBWorker

import configuration.server_token as server_auth_token

def validate_types(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            hints = get_type_hints(func)
            
            # Проверка позиционных аргументов
            for arg, value in zip(func.__code__.co_varnames, args):
                if arg in hints:
                    if hints[arg] != Any:
                        assert isinstance(value, hints[arg]), f"Argument {arg} must be {hints[arg]}"
            # Проверка именованных аргументов
            for key, value in kwargs.items():
                if key in hints:
                    if hints[key] != Any:
                        # if isinstance(hints[key], typing._UnionGenericAlias):
                        if len(get_args(hints[key])) > 1:
                            is_correct = False
                            for list_value in get_args(hints[key]):
                                if isinstance(value, list_value):
                                    is_correct = True
                            assert is_correct
                        else:
                            assert isinstance(value, hints[key]),f"Argument {key} must be {hints[key]}"
            
            result = func(*args, **kwargs)
            # Проверка возвращаемого значения
            # if 'return' in hints:
            #     if hints['return'] != Any:
            #         assert isinstance(result, hints['return']), f"Return value must be {hints['return']}"
            return result
        
        except AssertionError as e:
            return {"status": False, "info": "Received data not valid"}, 400
    return wrapper

class RobotChecker:
    
    @staticmethod
    def check_angles(robot_name:str, angles:dict, robots:dict) -> bool: 
        for i in range(1, int(robots[robot_name]["AngleCount"])+1):
            if float(angles.get(f"J{i}")) <= robots[robot_name]["MaxAngles"][f"J{i}"] and\
                float(angles.get(f"J{i}")) >= robots[robot_name]["MinAngles"][f"J{i}"]:
                pass
            else:
                return False
        return True
    
    @staticmethod
    def robot_access(robots:dict, name:str, code:str) -> bool:
        if name in robots:
            return robots[name]["SecureCode"] == code
        else:
            return True

    @staticmethod
    def is_robot(token:str) -> bool:
        from services.accounts_manager import AccountManager
        users:dict = AccountManager().get_users()
        tokens = []
        for i in [i for i in users]:
            tokens.append(users.get(i)["token"])
        if token in tokens:
            # Get role from token
            query = db.select(
                users_table.columns.role
            ).where(users_table.columns.token == token)
            role = DBWorker().send_select_query(query).fetchone()

            return role[0] == "robot"
        else:
            raise ValueError("Token incorrect")
       
    @staticmethod 
    def auto_robot_name_finder(robot_name:Union[str, None], token) -> Union[str, None]:
        robot_name_by_token = UserChecker().get_robot_name(token)
        if robot_name_by_token is None:
            if robot_name is None:
                return None
        elif robot_name_by_token is not None:
            robot_name = robot_name_by_token
            
        if RobotChecker().robot_exists(robot_name):
            return robot_name
        else:
            return None
        
    @staticmethod
    def check_program_token(robot_name:str, _program_token:str) -> bool:
        from services.multi_robots_manager import MultiRobotsManager
        robots = MultiRobotsManager().get_robots()
        program_token = robots[robot_name]["ProgramToken"]
        return program_token == _program_token or program_token == ""
        
    @staticmethod
    def robot_exists(robot_name:str) -> bool:
        from services.multi_robots_manager import MultiRobotsManager
        robots = MultiRobotsManager().get_robots()
        return robot_name in robots
        
class UserChecker:
    
    @staticmethod    
    def is_user(user_name:str) -> bool:
        from services.accounts_manager import AccountManager
        """_summary_

        Args:
            user_name (str): User name

        Returns:
            bool: True if user exists, False otherwise
        """
        users:dict = AccountManager().get_users()
        return user_name in users
    
    @staticmethod
    def get_role_level(role:str) -> int:
        role_level:int
        if role == "user": role_level = 1
        elif role == "robot": role_level = 1
        elif role == "administrator": role_level = 2
        elif role == "SuperAdmin": role_level = 3
        elif role == "System": role_level = 4
        return role_level
    
    def role_access(self, token:str, target_role:str) -> bool:
        from services.accounts_manager import AccountManager
        users:dict = AccountManager().get_users()
        tokens = []
        for name in users.keys():
            tokens.append(users.get(name)["token"])

        if token in tokens:
            query = db.select(users_table.columns.role, users_table.columns.name).where(users_table.columns.token == token)
            role, name = DBWorker().send_select_query(query).fetchone()._tuple()
            # extracting a role from a token
            role_level = self.get_role_level(role)
            # set target_role_level
            target_role_level = self.get_role_level(target_role)
            # comparison of levels
            return role_level >= target_role_level and role != "robot"
        else:
            raise ValueError("Token incorrect")
        
    @staticmethod
    def get_account_data(token:str) -> dict:
        query = db.select(users_table).where(users_table.columns.token == token)
        user_data = DBWorker().send_select_query(query).fetchone()
        user_data = {
            "name": user_data[0],
            "password": user_data[1],
            "role": user_data[2],
            "token": user_data[3],
        }
        return user_data
    
    def get_robot_name(self, token:str) -> Union[str, None]:
        account_data = self.get_account_data(token)
        if account_data.get("role") == "robot":
            return account_data["name"]
        else:
            return None

class ServerChecker:
    
    @staticmethod
    def is_server_token(token:str) -> bool:
        return token == server_auth_token.reg_token
        
class BasesChecker:
    
    @staticmethod
    def base_exists(base_name:str) -> bool:
        from services.bases_manager import BasesManager
        bases = BasesManager().get_bases()
        return base_name in bases.keys()
        
    @staticmethod
    def data_is_valid(base_data:dict) -> bool:
        if isinstance(base_data, dict) and \
            (("x" in base_data and "y" in base_data and "z" in base_data) and\
            ("a" in base_data and "b" in base_data and "c" in base_data)):
                return True
        else:
            return False
        
class FramesChecker:
    
    @staticmethod
    def frame_exists(frame_name:str) -> bool:
        from services.frames_manager import FramesManager
        frames = FramesManager().get_frames()
        return frames.get(frame_name) is not None
    
class ToolsChecker:
    
    @staticmethod
    def tool_exists(tool_id:str) -> bool:
        from services.tools_manager import ToolsManager
        tools = ToolsManager().get_tools()
        return tools.get(tool_id) is not None
    
    @staticmethod
    def calibration_is_valid(calibration_data:dict) -> bool:
        if isinstance(calibration_data, dict):
            return True
        else:
            return False
        
    @staticmethod
    def calibration_is_exists(tool_id:str) -> bool:
        from services.tools_manager import ToolsManager
        tools = ToolsManager().get_tools()
        if tools[tool_id].get("calibrated_vector") is not None:
            return True
        else:
            return False