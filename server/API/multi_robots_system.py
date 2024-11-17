import sqlite3
import ast
import secrets
import os

from flask import Flask, request

from utils.loger import Loger

class URMSystem:
    
    def __init__(self, robots:dict=None):
        if robots is not None:
            globals()["robots"] = robots
            
    @staticmethod
    def set_robots(robots: dict):
        globals()["robots"] = robots
        
    @staticmethod
    def get_robots():
            return globals()["robots"]
    
    def __call__(self, app:Flask, loger:Loger) -> Flask:
        from server_functions import System, User
        from API.frames_manager import FramesManager
        from API.tools_manager import ToolsManager
        
        # add robot
        @app.route("/CreateRobot", methods=['POST'])
        def CreateRobot():
            info = request.form
            users:dict = globals()["users"]
            robots = globals()["robots"]
            if User.role_access(info.get("token"), "administrator", users):
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
                        "Kinematic" : f"./kinematics/{info.get('Kinematics')}" if info.get('Kinematics') != "None" else "None", 
                        "Logs" : "", 
                        "RobotReady" : "True",
                        "Emergency":"False",
                        "SecureCode":  info.get("Code") if info.get("Code") != None else "None",
                        "XYZposition" : {
                            "X": 0.0,
                            "Y": 0.0,
                            "Z": 0.0,
                            }
                        }
                System().SaveToCache(robots=robots)
                User().update_token()
                loger.info("URMS", f"Robot named {info.get('Robot')} was created")
                return "True"
            else:
                return "You don't have enough rights"

        # Import robot cache
        @app.route("/ImportCache", methods=['POST'])
        def ImportCache():
            info = request.form
            frames:dict = FramesManager().get_frames()
            users:dict = globals()["users"]
            robots = globals()["robots"]
            tools:dict = ToolsManager().get_tools()
            if User.role_access(info.get("token"), "SuperAdmin", users):
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
                loger.info("URSystem", f"Cache was imorted")
                return "True"
            else:
                return "You don't have enough rights"
            
        # Export robot cache
        @app.route("/ExportCache", methods=['POST'])
        def ExportCache():
            info = request.form
            if User.role_access(info.get("token"), "SuperAdmin"):
                with open("./configuration/robots_cache.py", "r") as file:
                    cache = file.read()
                loger.info("URSystem", f"Cache was exported")
                return cache
            else:
                return "You don't have enough rights"

        # get robot
        @app.route("/GetRobot", methods=['POST'])
        def GetRobot():
            info = request.form
            frames = FramesManager().get_frames()
            robots = globals()["robots"]
            try:
                if User.role_access(info.get("token"), "administrator"):
                    User().update_token()
                    return str(robots[info.get("Robot")])
                else:
                    return "You don't have enough rights"
            except:
                return "You don't have enough rights"
            
        # get robots
        @app.route("/GetRobots", methods=['POST'])
        def GetRobots():
            info = request.form
            frames = FramesManager().get_frames()
            robots = globals()["robots"]
            if User().role_access(info.get("token"), "administrator"):
                User().update_token()
                return robots
            else:
                return "You don't have enough rights"

        # delete robot
        @app.route("/DelRobot", methods=['POST'])
        def DelRobot():
            info = request.form
            robots = globals()["robots"]
            if User.role_access(info.get("token"), "administrator"):
                del robots[info.get("Robot")]
                User().update_token()
                loger.info("URSystem", f"Robot was deleted user with token: {info.get('token')}")
                return "True"
            else:
                return "You don't have enough rights"
            
        return app