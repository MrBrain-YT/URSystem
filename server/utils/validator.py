from typing import Union

import sqlalchemy as db

from databases.connection import users_table
from databases.database_manager import DBWorker
from services.accounts_manager import AccountManager
from services.multi_robots_manager import MultiRobotsManager

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
        robots:dict = MultiRobotsManager.get_robots()
        program_token = robots[robot_name]["ProgramToken"]
        if program_token == _program_token or program_token == "":
            return True
        else:
            return False
        
class UserChecker:
    
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
            if role_level >= target_role_level and role != "robot":
                return True
            else:
                return False
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
