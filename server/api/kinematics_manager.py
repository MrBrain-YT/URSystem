from flask import Blueprint, request, jsonify

from services.kinematics_manager import KinematicsManager
from api.access_checker import Access

class KinematicsManagerAPI:
    access = Access()
    
    def __init__(self, kinematics:dict=None):
        self.logger_module = "URKinematics"
        if kinematics is not None:
            self.kinematic_manager = KinematicsManager(kinematics)
        else:
            self.kinematic_manager = KinematicsManager()
    
    def __call__(self) -> Blueprint:
        
        kinematics_bp = Blueprint("kinematics_api", __name__, url_prefix="/api")
        
        """ Add kinematics to system """
        @kinematics_bp.route("/add-kinematic", methods=['POST'])
        @self.access.check_user(user_role="administrator", logger_module=self.logger_module)
        def add_kinematic():
            kinematic_file = request.files.get('file')
            response, code = self.kinematic_manager.add_kinematic(kinematic_file=kinematic_file)
            return jsonify(response), code

        """ Bind kinematics to robot """
        @kinematics_bp.route("/bind-kinematic", methods=['POST'])
        @self.access.check_user_and_robot_data(user_role="administrator", logger_module=self.logger_module)
        def bind_kinematic():
            info = request.json
            robot_name = info.get("robot")
            kinematic_id = info.get("id")
            response, code = self.kinematic_manager.bind_kinematic(robot_name=robot_name, kinematic_id=kinematic_id)
            return jsonify(response), code
        
        """ Unbind kinematics to robot """
        @kinematics_bp.route("/unbind-kinematic", methods=['POST'])
        @self.access.check_user_and_robot_data(user_role="administrator", logger_module=self.logger_module)
        def unbind_kinematic():
            info = request.json
            robot_name = info.get("robot")
            response, code = self.kinematic_manager.unbind_kinematic(robot_name=robot_name)
            return jsonify(response), code

        return kinematics_bp