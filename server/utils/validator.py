import sqlalchemy as db

from databases.connection import users_table
from databases.database_manager import DBWorker

class RobotChecker:
    
    @staticmethod
    def check_angles(robot_name:str, angles:dict, robots:dict) -> None: 
        for i in range(1, int(robots[robot_name]["AngleCount"])+1):
            if float(angles.get(f"J{i}")) <= robots[robot_name]["MaxAngles"][f"J{i}"] and\
                float(angles.get(f"J{i}")) >= robots[robot_name]["MinAngles"][f"J{i}"]:
                pass
            else:
                return False
    
    @staticmethod
    def robot_access(Robots:dict, name:str, code:str) -> bool:
        return Robots[name]["SecureCode"] == code

    @staticmethod
    def is_robot(token:str) -> bool:
        from API.accounts_manager import AccountManager
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
    def check_program_token(robot_name:str, _program_token:str) -> bool:
        from server.API.multi_robots_manager import URMSystem
        robots:dict = URMSystem.get_robots()
        program_token = robots[robot_name]["ProgramToken"]
        if program_token == _program_token or program_token == "":
            return True
        else:
            return False
        
class UserChecker:
    
    @staticmethod
    def role_access(token:str, target_role:str) -> bool:
        from API.accounts_manager import AccountManager
        users:dict = AccountManager().get_users()
        tokens = []
        for name in [name for name in users.keys()]:
            tokens.append(users.get(name)["token"])
        if token in tokens:
            query = db.select(users_table.columns.role, users_table.columns.name).where(users_table.columns.token == token).select()
            role, name = DBWorker().send_select_query(query).fetchone()._tuple()
            # extracting a role from a token
            if role == "user": role_level = 1
            elif role == "robot": role_level = 1
            elif role == "administrator": role_level = 2
            elif role == "SuperAdmin": role_level = 3
            elif role == "System": role_level = 4
            # set target_role_level
            if target_role == "user": target_role_level = 1
            elif target_role == "robot": target_role_level = 1
            elif target_role == "administrator": target_role_level = 2
            elif target_role == "SuperAdmin": target_role_level = 3
            elif target_role == "System": target_role_level = 4
            # comparison of levels
            if role_level >= target_role_level and role != "robot":
                return True
            else:
                return False
        else:
            raise ValueError("Token incorrect")