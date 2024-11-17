import shutil
import os
import importlib

from flask import Flask, request

from utils.loger import Loger

class KinematicsManager:
    
    def __init__(self, kinematics:dict=None):
        if kinematics is not None:
            globals()["kinematics"] = kinematics
    
    def __call__(self, app: Flask, loger: Loger) -> Flask:
        from server_functions import User, Robot
        from API.multi_robots_system import URMSystem
        from server_functions import System
        
        """ Add kinematics to system """
        @app.route("/AddKinematics", methods=['POST'])
        def AddKinematics():
            info = request.form
            if User.role_access(info.get("token"), "administrator"):
                zip_path = f"./kinematics/{request.files.get('file').filename}"
                request.files.get("file").save(zip_path)
                shutil.unpack_archive(filename=zip_path, extract_dir=zip_path.replace(".zip", ""), format="zip")
                os.remove(zip_path)
                loger.info("URSystem", f"Added new kinematic with work name: {request.files.get('file')}")
                return "True"
            else:
                loger.warning("URSystem", f"User access denied to add kinematic. User with token: {request.form.get('token')}")
                return "You don't have enough rights"

        """ Bind kinematics to robot """
        @app.route("/BindKinematics", methods=['POST'])
        def BindKinematics():
            info = request.form
            robots = URMSystem().get_robots()
            if User.role_access(info.get("token"), "administrator") and Robot.robot_access(robots, info.get("Robot"), info.get("Code")):
                robots[info.get("Robot")]["Kinematic"] = info.get('Kinematics') if \
                    os.path.exists(f"./kinematics/{info.get('Kinematics')}") else robots[info.get("Robot")]["Kinematic"]
                System().SaveToCache(robots=robots)
                
                if robots[info.get("Robot")]["Kinematic"] == info.get('Kinematics'):
                    loger.info("URSystem", f"Was created associate kinematics-{info.get('Kinematics')} and robot-{info.get('Robot')}")
                    return "True"
                else:
                    loger.error("URSystem", f"Not created associate kinematics-{info.get('Kinematics')} and robot-{info.get('Robot')}")
                    return "It was not possible to associate kinematics with the robot because it is missing"
            else:
                loger.warning("URSystem", f"User access denied to bind kinematic. User with token: {request.form.get('token')}")
                return "You don't have enough rights"
            
        return app
            
    @staticmethod
    def update_kinematics_data():
        from API.multi_robots_system import URMSystem
        kinematics = {}
        robots:dict = URMSystem().get_robots()
        for robot in robots:
            if robots.keys()[robot]["Kinematic"] == "None":
                kinematics[robot] = "None"
            else:
                try:
                    kinematics[robot] = importlib.import_module(
                        f'kinematics.{robots.keys()[robot]["Kinematic"]}.kin')
                except:
                    # send to logs!
                    print(f"For robot '{robot}' kinematic file not found ")
                    
        globals()["kinematics"] = kinematics
        
    @staticmethod
    def get_kinematics():
        return globals()["kinematics"]