from typing import Callable
from functools import wraps

from flask import request, jsonify

from utils.loger import Loger

class Access:
    
    def __init__(self):
        self.loger = Loger()

    @staticmethod
    def check_robot(func:Callable):
        """Checker for only robot account\n
        Using @check_robot
        """
        from server_functions import Robot
        @wraps(func)
        def wrapper(*args, **kwargs):
            info = request.json
            if Robot.is_robot(info.get("token")):
                return func(*args, **kwargs)
            else:
                return "Your account is not a robot account"
        return wrapper
    
    @staticmethod
    def check_robot_or_user(user_role:str):
        """Checker for robot or user account, if you need dont checking robot data (secure code)\n
        Using @check_robot_or_user(user_role="user")

        Args:
            user_role (str): User role ("user", "administrator", "SuperAdmin", "System")
        """
        from server_functions import Robot, User
        def check_robot_or_user_wrapper(func:Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                info = request.json
                if User.role_access(info.get("token"), user_role) or Robot.is_robot(info.get("token")):
                    return func(*args, **kwargs)
                else:
                    return jsonify({"status": False, "info": "You don't have enough rights"}), 403
            return wrapper
        return check_robot_or_user_wrapper
       
    def check_user(self, user_role:str, loger_module:str):
        """Checker for only user account\n
        Using @check_user(user_role="user", loger_module="URAccounts")

        Args:
            user_role (str): User role ("user", "administrator", "SuperAdmin", "System")
            loger_module (str): loger Module that adds a log entry
        """
        from server_functions import User
        def check_user_wrapper(func:Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                info = request.json
                if User.role_access(info.get("token"), user_role):
                    return func(*args, **kwargs)
                else:
                    self.loger.warning(module=loger_module, msg=f"User access denied. User with token: {info.get('token')}")
                    return jsonify({"status": False, "info": "You don't have enough rights"}), 403
            return wrapper
        return check_user_wrapper
    
    def check_user_and_robot_data(self, user_role:str, loger_module:str):
        """Checker for user account, if you need checking robot data (secure code)\n
        Using @check_user_and_robot_data(user_role="user", loger_module="URAccounts")

        Args:
            user_role (str): User role ("user", "administrator", "SuperAdmin", "System")
            loger_module (str): loger Module that adds a log entry
        """
        from server_functions import User, Robot
        from API.multi_robots_system import URMSystem
        robots:dict = URMSystem().get_robots()
        def check_user_wrapper(func:Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                info = request.json
                if User.role_access(info.get("token"), user_role) and Robot.robot_access(robots, info.get("robot"), info.get("code")):
                    return func(*args, **kwargs)
                else:
                    self.loger.warning(module=loger_module, msg=f"User access denied to create account. User with token: {info.get('token')}")
                    return jsonify({"status": False, "info": "You don't have enough rights"}), 403
            return wrapper
        return check_user_wrapper
       
    def check_robot_user(self, user_role:str, loger_module:str):
        """Checker for user or robot account, if you need checking robot data (secure code)\n
        Using @check_robot_user(user_role="user", loger_module="URSystem")

        Args:
            user_role (str): User role ("user", "administrator", "SuperAdmin", "System")
        """
        from server_functions import User, Robot
        from API.multi_robots_system import URMSystem
        def check_robot_user_wrapper(func:Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                info = request.json
                robots:dict = URMSystem().get_robots()
                if (User.role_access(info.get("token"), user_role) and \
                Robot.robot_access(robots, info.get("robot"), info.get("code"))) or Robot.is_robot(info.get("token")):
                    return func(*args, **kwargs)
                else:
                    self.loger.warning(module=loger_module, msg=f"Access denied. User with token: {info.get('token')}")
                    return jsonify({"status": False, "info": "You are not on the users list"}), 403
            return wrapper
        return check_robot_user_wrapper
    
    @staticmethod
    def check_robot_user_prog_token(user_role:str):
        """Checker for user or robot account, if you need checking robot data (secure code), program token and robot or user account\n
        Using @check_robot_user_prog_token(user_role="user")

        Args:
            user_role (str): User role ("user", "administrator", "SuperAdmin", "System")
        """
        from server_functions import User, Robot
        from API.multi_robots_system import URMSystem
        def check_robot_user_prog_token_wrapper(func:Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                info = request.json
                robots:dict = URMSystem().get_robots()
                if ((User.role_access(info.get("token"), user_role) and \
                Robot.robot_access(robots, info.get("robot"), info.get("code"))) or Robot.is_robot(info.get("token")))\
                and Robot().check_program_token(info.get("robot"), info.get("program_token")) if robots[info.get("robot")]["Program"] != "" else True:
                    return func(*args, **kwargs)
                else:
                    return jsonify({"status": False, "info": "You are not on the users list or program token is not valid"}), 403
            return wrapper
        return check_robot_user_prog_token_wrapper
    
    
    def check_robot_user_prog(self, user_role:str, loger_module:str):
        """Checker for program robot and user account, if you need checking robot data (secure code) and value program in robot\n
        Using @check_robot_user_prog(user_role="user", loger_module="URSystem")

        Args:
            user_role (str): User role ("user", "administrator", "SuperAdmin", "System")
            loger_module (str): loger Module that adds a log entry
        """
        from server_functions import User, Robot
        from API.multi_robots_system import URMSystem
        def check_robot_user_prog_wrapper(func:Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                info = request.json
                robots:dict = URMSystem().get_robots()
                if robots[info.get("robot")]["Program"] == "":
                    if User.role_access(info.get("token"), user_role) and Robot.robot_access(robots, info.get("robot"), info.get("code")):
                        return func(*args, **kwargs)
                    else:
                        self.loger.warning(module=loger_module, msg=f"User access denied to set robot {info.get('robot')} minimal angles. User with token: {request.json.get('token')}")
                        return jsonify({"status": False, "info": "You don't have enough rights"}), 403
                else:
                    self.loger.warning(module=loger_module, msg=f"The robot executes an automatic program. It is currently not possible to change the MinAngles parameter. User with token: {info.get('token')}")
                    return jsonify({"status": False, "info": "The robot executes an automatic program. It is currently not possible to change the parameter"}), 403
            return wrapper
        return check_robot_user_prog_wrapper