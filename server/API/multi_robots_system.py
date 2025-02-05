import sqlite3
import ast
import secrets
import os
import json

from flask import Flask, request

from utils.loger import Loger
from server_functions import System

class URMSystem:
    
    def __init__(self, robots:dict=None):
        self.loger_module = "URMSystem"
        if robots is not None:
            globals()["robots"] = robots
            System.SaveToCache(robots=robots)
            
    @staticmethod
    def set_robots(robots: dict):
        globals()["robots"] = robots
        
    @staticmethod
    def get_robots() -> dict:
            return globals()["robots"]
    
    def __call__(self, app:Flask, loger:Loger) -> Flask:
        from server_functions import System, User
        from API.frames_manager import FramesManager
        from API.tools_manager import ToolsManager
        from API.accounts_manager import AccountManager
        from API.access_checker import Access
        from API.robot_manager import RobotManager
        
        access = Access()
        
        # add robot
        @app.route("/CreateRobot", methods=['POST'])
        @access.check_user(user_role="administrator", loger_module=self.loger_module)
        def CreateRobot():
            info = request.json
            robots = globals()["robots"]
            angles = {}
            for i in range(1, int(info.get("Angle"))+1):
                angles[f"J{i}"] = 0.0
            robots[info.get("Robot")] = {
                    "AngleCount" : int(info.get("Angle")),
                    "Position" : angles.copy(),
                    "HomePosition" : angles.copy(),
                    "MotorsPosition" : angles.copy(),
                    "MotorsSpeed" : angles.copy(),
                    "StandartSpeed" : angles.copy(),
                    "MinAngles" : angles.copy(),
                    "MaxAngles" : angles.copy(),
                    "Program" : "", 
                    "ProgramRunning" : "False",
                    "ProgramToken" : "", 
                    "Kinematic" : f"./kinematics/{info.get('Kinematics')}" if info.get('Kinematics') != "None" else "None", 
                    "Logs" : "", 
                    "RobotReady" : "True",
                    "Emergency":"False",
                    "SecureCode":  info.get("Code") if info.get("Code") != None else "None",
                    "is_robot_ready_setted_false": "True",
                    "XYZposition" : {
                        "X": 0.0,
                        "Y": 0.0,
                        "Z": 0.0,
                        }
                    }
            System().SaveToCache(robots=robots)
            User().update_token()
            RobotManager.add_new_robot_ready(info.get("Robot"))
            log_message = f"Robot named {info.get('Robot')} was created"
            loger.info("URMS", log_message)
            return json.dumps({"status": True, "info": log_message}), 200

        # Import robot cache
        @app.route("/ImportCache", methods=['POST'])
        @access.check_user(user_role="SuperAdmin", loger_module=self.loger_module)
        def ImportCache():
            info = request.json
            frames:dict = FramesManager().get_frames()
            users:dict = AccountManager().get_users()
            robots:dict = globals()["robots"]
            tools:dict = ToolsManager().get_tools()
            new_robots:dict = ast.literal_eval(info.get("robots"))
            new_tools:dict = ast.literal_eval(info.get("tools"))
            new_frames:dict = ast.literal_eval(info.get("frames"))
            # import robots
            con = sqlite3.connect("Databases\\Users.sqlite")
            cur = con.cursor()
            for robot_name in new_robots.keys():
                if robot_name in robots:
                    pass
                else:
                    robots[robot_name] = new_robots[robot_name]
                    # creating account for imported robot
                    while True:
                        token = secrets.token_hex(32)
                        tokens = []
                        for i in [i for i in users]:
                            tokens.append(users.get(i)["token"])
                        if token not in tokens:
                            break
                    cur.execute(f"INSERT INTO users VALUES ('{robot_name}', '{new_robots[robot_name]['password']}', 'robot', '{token}')")
                    try:
                        os.mkdir(f'Logs/{robot_name}')
                    except:
                        pass
            con.commit()
            con.close()
            RobotManager.add_new_robot_ready(robot_name)
            # import tools
            for tool_name in new_tools.keys():
                if tool_name in tools:
                    pass
                else:
                    tools[tool_name] = new_tools[tool_name]
                    
            # import frames
            for frames_name in new_frames.keys():
                if frames_name in tools:
                    pass
                else:
                    frames[frames_name] = new_frames[frames_name]
                    
            System().SaveToCache(robots=robots, tools=tools, frames=frames)
            log_message = "Cache was imorted"
            loger.info("URSystem", log_message)
            return json.dumps({"status": True, "info": log_message}), 200
            
        # Export robot cache from cache file
        @app.route("/ExportFileCache", methods=['POST'])
        @access.check_user(user_role="SuperAdmin", loger_module=self.loger_module)
        def ExportFileCache():
            with open("./configuration/robots_cache.py", "r") as file:
                cache = file.read()
                
            loger.info("URSystem", "Current cache from cache file was exported")
            new_cache = {
                "robots": ast.literal_eval(cache.split("\n")[0].lstrip("robots = ")),
                "tools": ast.literal_eval(cache.split("\n")[1].lstrip("robots = ")),
                "frames": ast.literal_eval(cache.split("\n")[2].lstrip("robots = ")),
            }
            return json.dumps({"status": True, "info": "Current cache from cache file", "data": new_cache}), 200
        
        # Export robot cache from RAM
        @app.route("/ExportCache", methods=['POST'])
        @access.check_user(user_role="SuperAdmin", loger_module=self.loger_module)
        def ExportCache():
            frames:dict = FramesManager().get_frames()
            robots:dict = globals()["robots"]
            tools:dict = ToolsManager().get_tools()
            
            loger.info("URSystem", "Current cache from RAM was exported")
            new_cache = {
                "robots": robots,
                "tools": tools,
                "frames": frames,
            }
            return json.dumps({"status": True, "info": "Current cache from RAM", "data": new_cache}), 200

        # get robot
        @app.route("/GetRobot", methods=['POST'])
        @access.check_user(user_role="administrator", loger_module=self.loger_module)
        def GetRobot():
            info = request.json
            robots:dict = globals()["robots"]
            User().update_token()
            result = robots[info.get("Robot")] if info.get("Robot") in robots.keys() else None
            if result is not None:
                return json.dumps({"status": True, "info": "Get robot data", "data": result}), 200
            else:
                return json.dumps({"status": False, "info": "Robot not found"}), 400
            
        # get robots
        @app.route("/GetRobots", methods=['POST'])
        @access.check_user(user_role="administrator", loger_module=self.loger_module)
        def GetRobots():
            robots:dict = globals()["robots"]
            User().update_token()
            return json.dumps({"status": True, "info": "All robots data", "data": robots}), 200

        # delete robot
        @app.route("/DelRobot", methods=['POST'])
        @access.check_user(user_role="administrator", loger_module=self.loger_module)
        def DelRobot():
            info = request.json
            robots:dict = globals()["robots"]
            if info.get("Robot") in robots.keys():
                del robots[info.get("Robot")]
                RobotManager.remove_new_robot_ready(info.get("Robot"))
                User().update_token()
                loger.info("URSystem", f"Robot was deleted user with token: {info.get('token')}")
                return json.dumps({"status": True, "info": f"Robot '{info.get('Robot')}' was deleted"}), 200
            else:
                User().update_token()
                loger.info("URSystem", f"Robot did not deleted user with token: {info.get('token')}")
                return json.dumps({"status": False, "info": "Robot not found"}), 400
            
        return app