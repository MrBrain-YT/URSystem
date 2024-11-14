import os
import sqlite3
import secrets

class Robot:
    def check_angles(info, Robots) -> None: 
        for i in range(1, int(Robots[info.get("Robot")]["AngleCount"])+1):
            if float(info.get(f"J{i}")) <= Robots[info.get("Robot")]["MaxAngles"][f"J{i}"] and float(info.get(f"J{i}")) >= Robots[info.get("Robot")]["MinAngles"][f"J{i}"]:
                pass
            else:
                return False
        
    def robot_access(Robots:dict, name:str, code:str):
        return Robots[name]["SecureCode"] == code

    def is_robot(token, users):
        tokens = []
        for i in [i for i in users]:
            tokens.append(users.get(i)["token"])
        if token in tokens:
            # Get role from token
            con = sqlite3.connect("databases\\Users.sqlite")
            cur = con.cursor()
            res = cur.execute(f"SELECT role, name FROM 'users' WHERE token = '{token}'")
            role, n = res.fetchone()
            con.close()
            if role == "robot": return True
            else: return False
        else:
            raise ValueError("Token incorrect")
    
    
class System:   
    def SaveToCache(Robots:dict, tools:dict, frames:dict) -> None:
        os.remove("./configuration/robots_cache.py")
        with open("./configuration/robots_cache.py", "w") as file:
            file.write(f"robots = {Robots}")
            file.write(f"\ntools = {tools}")
            file.write(f"\nframes = {frames}")

class User:
    def role_access(token, target_role, users) -> bool:
        tokens = []
        for i in [i for i in users]:
            tokens.append(users.get(i)["token"])
        if token in tokens:
            # Get role from token
            con = sqlite3.connect("databases\\Users.sqlite")
            cur = con.cursor()
            res = cur.execute(f"SELECT role, name FROM 'users' WHERE token = '{token}'")
            role, n = res.fetchone()
            con.close()
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
        users = {}
        con = sqlite3.connect("databases\\Users.sqlite")
        cur = con.cursor()
        res = cur.execute("SELECT * FROM 'users'")
        rows = res.fetchall()
        con.close()
        for i in rows:
            users[i[0]] = {"password": i[1],
                    "role": i[2],
                    "token": i[3]
                    }
        return users
    
    def update_token(self) -> dict:
        users = self.update_user_info()
        while True:
            token = secrets.token_hex(32)
            tokens = []
            for i in [i for i in users]:
                tokens.append(users.get(i)["token"])
            if token not in tokens:
                break
        con = sqlite3.connect("databases\\Users.sqlite")
        cur = con.cursor()
        cur.execute(f"UPDATE users SET token = '{token}' WHERE role = 'System' and name = '' and password = ''")
        con.commit()
        con.close()
        os.environ["SYSTEM_API_TOKEN"] = token
        return self.update_user_info()