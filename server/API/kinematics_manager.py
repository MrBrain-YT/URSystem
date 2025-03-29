import shutil
import os
import importlib

from flask import Flask, request, jsonify

from utils.loger import Loger

class KinematicsManager:
    
    def __init__(self, kinematics:dict=None):
        self.loger_module = "URKinematics"
        if kinematics is not None:
            globals()["kinematics"] = kinematics
    
    def __call__(self, app: Flask, loger: Loger) -> Flask:
        from server_functions import User, Robot
        from API.multi_robots_system import URMSystem
        from server_functions import System
        from API.access_checker import Access

        access = Access()
        
        """ Add kinematics to system """
        @app.route("/AddKinematics", methods=['POST'])
        @access.check_user(user_role="administrator", loger_module=self.loger_module)
        def AddKinematics():
            zip_path = f"./kinematics/{request.files.get('file').filename}"
            request.files.get("file").save(zip_path)
            shutil.unpack_archive(filename=zip_path, extract_dir=zip_path.replace(".zip", ""), format="zip")
            os.remove(zip_path)
            log_message = f"Added new kinematic with id: {request.files.get('file')}"
            loger.info("URSystem", log_message)
            return jsonify({"status": True, "info": log_message}), 200


        """ Bind kinematics to robot """
        @app.route("/BindKinematics", methods=['POST'])
        @access.check_user_and_robot_data(user_role="administrator", loger_module=self.loger_module)
        def BindKinematics():
            info = request.json
            robots = URMSystem().get_robots()
            robots[info.get("robot")]["Kinematic"] = info.get('id') if \
                os.path.exists(f"./kinematics/{info.get('id')}") else robots[info.get("robot")]["Kinematic"]
            System().SaveToCache(robots=robots)
            
            if robots[info.get("robot")]["Kinematic"] == info.get('id'):
                log_message = f"Was created associate kinematics-{info.get('id')} and robot-{info.get('robot')}"
                loger.info("URSystem", log_message)
                return jsonify({"status": True, "info": log_message}), 200
            else:
                log_message = f"Not created associate kinematics-{info.get('id')} and robot-{info.get('robot')}"
                loger.error("URSystem", log_message)
                return jsonify({"status": True, "info": log_message}), 400

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