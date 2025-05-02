import os
import secrets

import sqlalchemy as db

engine = db.create_engine("sqlite:///databases/Users.sqlite")
conn = engine.connect() 
metadata = db.MetaData()
users_table = db.Table("users",metadata, autoload_with=engine)

class Robot:
    def check_angles(info, Robots) -> None: 
        for i in range(1, int(Robots[info.get("robot")]["AngleCount"])+1):
            if float(info.get("angles").get(f"J{i}")) <= Robots[info.get("robot")]["MaxAngles"][f"J{i}"] and float(info.get("angles").get(f"J{i}")) >= Robots[info.get("robot")]["MinAngles"][f"J{i}"]:
                pass
            else:
                return False
        
    def robot_access(Robots:dict, name:str, code:str):
        return Robots[name]["SecureCode"] == code

    def is_robot(token):
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
            role = conn.execute(query).fetchone()

            if role == "robot": return True
            else: return False
        else:
            raise ValueError("Token incorrect")
        
    @staticmethod
    def check_program_token(robot_name:str, _program_token:str) -> bool:
        from API.multi_robots_system import URMSystem
        robots:dict = URMSystem.get_robots()
        program_token = robots[robot_name]["ProgramToken"]
        if program_token == _program_token or program_token == "":
            return True
        else:
            return False

class System:   
    
    @staticmethod
    def SaveToCache(robots:dict=None, tools:dict=None, frames:dict=None) -> None:
        from API.multi_robots_system import URMSystem
        from API.frames_manager import FramesManager
        from API.tools_manager import ToolsManager
        try:
            os.remove("./configuration/robots_cache.py")
        except:
            return None
        with open("./configuration/robots_cache.py", "w") as file:
            file.write(f"robots = {robots if robots is not None else URMSystem().get_robots()}")
            file.write(f"\ntools = {tools if tools is not None else ToolsManager().get_tools()}")
            file.write(f"\nframes = {frames if frames is not None else FramesManager().get_frames()}")
        if robots is not None:
            URMSystem().set_robots(robots)
        if tools is not None:
            ToolsManager().set_tools(tools)
        if frames is not None:
            FramesManager().set_frame(frames)

class User:
    
    @staticmethod
    def role_access(token, target_role) -> bool:
        from API.accounts_manager import AccountManager
        users:dict = AccountManager().get_users()
        tokens = []
        for name in [name for name in users.keys()]:
            tokens.append(users.get(name)["token"])

        if token in tokens:
            query = db.select(users_table.columns.role, users_table.columns.name).where(users_table.columns.token == token).select()
            role, name = conn.execute(query).fetchone()._tuple()
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

    @staticmethod
    def update_user_info():
        from API.accounts_manager import AccountManager
        users = {}
        query = users_table.select()
        rows = conn.execute(query).fetchall()
        for i in rows:
            users[i[0]] = {"password": i[1],
                    "role": i[2],
                    "token": i[3]
                    }
        AccountManager().set_users(users)
        return users
    
    def update_token(self) -> dict:
        users = self.update_user_info()
        tokens = []
        for i in [i for i in users]:
            tokens.append(users.get(i)["token"])
            
        while True:
            token = secrets.token_hex(32)
            if token not in tokens:
                break
        
        query = users_table.update().where(db.and_(users_table.columns.role == "System",
                    users_table.columns.name == "",
                    users_table.columns.password == "" 
                    )).values(token=token)
        conn.execute(query)
        conn.commit()

        os.environ["SYSTEM_API_TOKEN"] = token
        return self.update_user_info()