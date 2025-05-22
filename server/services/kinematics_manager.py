import shutil
import os
import importlib

from utils.logger import Logger
from services.multi_robots_manager import MultiRobotsManager
from configuration.cache.file_cache import save_to_cache

kinematics = {}

class KinematicsManager:
    kinematics = kinematics
    logger = Logger()
    multi_robots_manager = MultiRobotsManager()
    
    def __init__(self, kinematics:dict=None) -> None:
        self.logger_module = "URKinematics"
        if kinematics is not None:
            self.kinematics.update(kinematics)
    
    def get_kinematics(self) -> dict:
        return self.kinematics
    
    def update_kinematics_data(self) -> None:
        from server.API.multi_robots_manager import MultiRobotsManager
        kinematics = {}
        robots:dict = self.multi_robots_manager.get_robots()
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
                    
        self.kinematics.update(kinematics)
        
    """ Add kinematics to system """
    def add_kinematic(self, kinematic_file) -> tuple:
        zip_path = f"./kinematics/{kinematic_file.filename}"
        kinematic_file.save(zip_path)
        shutil.unpack_archive(filename=zip_path, extract_dir=zip_path.replace(".zip", ""), format="zip")
        os.remove(zip_path)
        log_message = f"Added new kinematic with id: {kinematic_file}"
        self.logger.info(module=self.logger_module, msg=log_message)
        return {"status": True, "info": log_message}, 200


    """ Bind kinematics to robot """
    def bind_kinematic(self, robot_name:str, kinematic_id:str) -> tuple:
        robots = self.multi_robots_manager.get_robots()
        robots[robot_name]["Kinematic"] = kinematic_id if \
            os.path.exists(f"./kinematics/{kinematic_id}") else robots[robot_name]["Kinematic"]
        save_to_cache(robots=robots)
        
        if robots[robot_name]["Kinematic"] == kinematic_id:
            log_message = f"Was created associate kinematics-{kinematic_id} and robot-{robot_name}"
            self.logger.info(module=self.logger_module, msg=log_message)
            return {"status": True, "info": log_message}, 200
        else:
            log_message = f"Not created associate kinematics-{kinematic_id} and robot-{robot_name}"
            self.logger.error(module=self.logger_module, msg=log_message)
            return {"status": True, "info": log_message}, 400