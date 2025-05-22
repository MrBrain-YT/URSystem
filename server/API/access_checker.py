from typing import Callable
from functools import wraps

from flask import request, jsonify

from utils.logger import Logger
from utils.validator import RobotChecker, UserChecker

class Access:
    
    def __init__(self):
        self.loger = Logger()

    @staticmethod
    def check_robot(func:Callable):
        """Checker for only robot account\n
        Using @check_robot
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            info = request.json
            if RobotChecker().is_robot(info.get("token")):
                return func(*args, **kwargs)
            else:
                return "Your account is not a robot account"
        return wrapper
    
    def check_robot_or_user(self, user_role:str, logger_module:str):
        """Checker for robot or user account, if you need dont checking robot data (secure code)\n
        Using @check_robot_or_user(user_role="user")

        Args:
            user_role (str): User role ("user", "administrator", "SuperAdmin", "System")
        """
        
        def check_robot_or_user_wrapper(func:Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                info = request.json
                if UserChecker().role_access(info.get("token"), user_role) or RobotChecker().is_robot(info.get("token")):
                    return func(*args, **kwargs)
                else:
                    self.loger.warning(module=logger_module, msg=f"Access denied when calling {func.__name__}. User with token: {info.get('token')}")
                    return jsonify({"status": False, "info": "You don't have enough rights"}), 403
            return wrapper
        return check_robot_or_user_wrapper
       
    def check_user(self, user_role:str, logger_module:str):
        """Checker for only user account\n
        Using @check_user(user_role="user", logger_module="URAccounts")

        Args:
            user_role (str): User role ("user", "administrator", "SuperAdmin", "System")
            logger_module (str): loger Module that adds a log entry
        """
        
        def check_user_wrapper(func:Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                info = request.json
                if UserChecker().role_access(info.get("token"), user_role):
                    return func(*args, **kwargs)
                else:
                    self.loger.warning(module=logger_module, msg=f"Access denied when calling {func.__name__}. User with token: {info.get('token')}")
                    return jsonify({"status": False, "info": "You don't have enough rights"}), 403
            return wrapper
        return check_user_wrapper
    
    def check_user_and_robot_data(self, user_role:str, logger_module:str):
        """Checker for user account, if you need checking robot data (secure code)\n
        Using @check_user_and_robot_data(user_role="user", logger_module="URAccounts")

        Args:
            user_role (str): User role ("user", "administrator", "SuperAdmin", "System")
            logger_module (str): loger Module that adds a log entry
        """
        from services.multi_robots_manager import MultiRobotsManager

        def check_user_wrapper(func:Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                info = request.json
                robots:dict = MultiRobotsManager().get_robots()
                if UserChecker().role_access(info.get("token"), user_role) and RobotChecker().robot_access(robots, info.get("robot"), info.get("code")):
                    return func(*args, **kwargs)
                else:
                    self.loger.warning(module=logger_module, msg=f"Access denied when calling {func.__name__}. User with token: {info.get('token')}")
                    return jsonify({"status": False, "info": "You don't have enough rights"}), 403
            return wrapper
        return check_user_wrapper
       
    def check_robot_user(self, user_role:str, logger_module:str):
        """Checker for user or robot account, if you need checking robot data (secure code)\n
        Using @check_robot_user(user_role="user", logger_module="URSystem")

        Args:
            user_role (str): User role ("user", "administrator", "SuperAdmin", "System")
        """
        from services.multi_robots_manager import MultiRobotsManager
        
        def check_robot_user_wrapper(func:Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                info = request.json
                robots:dict = MultiRobotsManager().get_robots()
                if (UserChecker().role_access(info.get("token"), user_role) and \
                RobotChecker().robot_access(robots, info.get("robot"), info.get("code"))) or RobotChecker().is_robot(info.get("token")):
                    return func(*args, **kwargs)
                else:
                    self.loger.warning(module=logger_module, msg=f"Access denied when calling {func.__name__}. User with token: {info.get('token')}")
                    return jsonify({"status": False, "info": "You don't have enough rights"}), 403
            return wrapper
        return check_robot_user_wrapper
    
    def check_robot_user_prog_token(self, user_role:str, logger_module:str):
        """Checker for user or robot account, if you need checking robot data (secure code), program token and robot or user account\n
        Using @check_robot_user_prog_token(user_role="user")

        Args:
            user_role (str): User role ("user", "administrator", "SuperAdmin", "System")
        """
        from services.multi_robots_manager import MultiRobotsManager
        
        def check_robot_user_prog_token_wrapper(func:Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                info = request.json
                robots:dict = MultiRobotsManager().get_robots()
                if ((UserChecker().role_access(info.get("token"), user_role) and \
                RobotChecker().robot_access(robots, info.get("robot"), info.get("code"))) or RobotChecker().is_robot(info.get("token")))\
                and RobotChecker().check_program_token(info.get("robot"), info.get("program_token")) if robots[info.get("robot")]["Program"] != "" else True:
                    return func(*args, **kwargs)
                else:
                    self.loger.warning(module=logger_module, msg=f"Access denied when calling {func.__name__}. User with token: {info.get('token')}")
                    return jsonify({"status": False, "info": "Access denied or program token is not valid"}), 403
            return wrapper
        return check_robot_user_prog_token_wrapper
    
    
    def check_robot_user_prog(self, user_role:str, logger_module:str):
        """Checker for program robot and user account, if you need checking robot data (secure code) and value program in robot\n
        Using @check_robot_user_prog(user_role="user", logger_module="URSystem")

        Args:
            user_role (str): User role ("user", "administrator", "SuperAdmin", "System")
            logger_module (str): loger Module that adds a log entry
        """
        from services.multi_robots_manager import MultiRobotsManager
        
        def check_robot_user_prog_wrapper(func:Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                info = request.json
                robots:dict = MultiRobotsManager().get_robots()
                if UserChecker().role_access(info.get("token"), user_role) and RobotChecker().robot_access(robots, info.get("robot"), info.get("code")):
                    if robots[info.get("robot")]["Program"] == "":
                        return func(*args, **kwargs)
                    else:
                        log_message = f"The robot executes an automatic program. It is currently not possible to change the parameter. User with token: {info.get('token')}"
                        self.loger.warning(module=logger_module, msg=log_message)
                        return jsonify({"status": False, "info": "The robot executes an automatic program. It is currently not possible to change the parameter"}), 200
                else:
                    self.loger.warning(module=logger_module, msg=f"Access denied when calling {func.__name__}. User with token: {info.get('token')}")
                    return jsonify({"status": False, "info": "You don't have enough rights"}), 403
                
            return wrapper
        return check_robot_user_prog_wrapper