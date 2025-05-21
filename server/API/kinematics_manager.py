from flask import Flask, request, jsonify

from services.kinematics_manager import KinematicsManager
from API.access_checker import Access

class KinematicsManagerAPI:
    access = Access()
    
    def __init__(self, kinematics:dict=None):
        self.logger_module = "URKinematics"
        if kinematics is not None:
            self.kinematic_manager = KinematicsManager(kinematics)
        else:
            self.kinematic_manager = KinematicsManager()
    
    def __call__(self, app: Flask) -> Flask:
        
        
        """ Add kinematics to system """
        @app.route("/add-kinematic", methods=['POST'])
        @self.access.check_user(user_role="administrator", logger_module=self.logger_module)
        def add_kinematic():
            kinematic_file = request.files.get('file')
            responce, code = self.kinematic_manager.add_kinematic(kinematic_file=kinematic_file)
            return jsonify(responce), code


        """ Bind kinematics to robot """
        @app.route("/bind-kinematic", methods=['POST'])
        @self.access.check_user_and_robot_data(user_role="administrator", logger_module=self.logger_module)
        def bind_kinematic():
            info = request.json
            robot_name = info.get("robot")
            kinematic_id = info.get("id")
            responce, code = self.kinematic_manager.bind_kinematic(robot_name=robot_name, kinematic_id=kinematic_id)
            return jsonify(responce), code

        return app