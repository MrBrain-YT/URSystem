from flask import Blueprint, request, jsonify

from services.robot_manager import RobotManager
from api.access_checker import Access

class RobotManagerAPI:
    access = Access()
    
    def __init__(self, robots:dict=None):
        self.logger_module = "URManager"
        self.robot_manager = RobotManager(robots)
    
    def __call__(self) -> Blueprint:
        
        robot_bp = Blueprint("robot_api", __name__, url_prefix="/api")

        """ Get current robot position """
        @robot_bp.route('/get-position', methods=['POST'])
        @self.access.check_robot_or_user(user_role="user", logger_module=self.logger_module)
        def get_position():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            response, code = self.robot_manager.get_position(
                robot_name=robot_name,
                token=token
            )
            return jsonify(response), code
        
        """ Get robot position id """
        @robot_bp.route('/get-position-id', methods=['POST'])
        @self.access.check_robot_or_user(user_role="user", logger_module=self.logger_module)
        def get_position_id():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            response, code = self.robot_manager.get_position_id(
                robot_name=robot_name,
                token=token
            )
            return jsonify(response), code
        
        """ Get current robot speed """
        @robot_bp.route('/get-speed', methods=['POST'])
        @self.access.check_robot
        def get_speed():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            response, code = self.robot_manager.get_speed(
                robot_name=robot_name,
                token=token
            )
            return jsonify(response), code
        
        """ Get current robot position """
        @robot_bp.route('/get-cartesian-position', methods=['POST'])
        @self.access.check_robot_or_user(user_role="user", logger_module=self.logger_module)
        def get_catesian_position():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            response, code = self.robot_manager.get_catesian_position(
                robot_name=robot_name,
                token=token
            )
            return jsonify(response), code
        
        """ Get robot angles count """
        @robot_bp.route('/get-angles-count', methods=['POST'])
        @self.access.check_robot_or_user(user_role="user", logger_module=self.logger_module)
        def get_angles_count():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            response, code = self.robot_manager.get_angles_count(
                robot_name=robot_name,
                token=token
            )
            return jsonify(response), code

        """ Set current robot motor position """
        @robot_bp.route('/set-motors-position', methods=['POST'])
        @self.access.check_robot
        def set_motors_position():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            angles = info.get("angles")
            response, code = self.robot_manager.set_motors_position(
                robot_name=robot_name,
                token=token,
                angles=angles
            )
            return jsonify(response), code
        
        """ Get robot ready parameter """
        @robot_bp.route('/get-ready', methods=['POST'])
        @self.access.check_robot
        def get_ready_state():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            response, code = self.robot_manager.get_ready_state(
                robot_name=robot_name,
                token=token
            )
            return jsonify(response), code

        ''' Get emergency stop '''
        @robot_bp.route('/get-emergency', methods=['POST'])
        @self.access.check_robot_or_user(user_role="user", logger_module=self.logger_module)
        def get_emergency_state():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            response, code = self.robot_manager.get_emergency_state(
                robot_name=robot_name,
                token=token
            )
            return jsonify(response), code

        """ Set robot ready parameter """
        @robot_bp.route('/set-ready', methods=['POST'])
        @self.access.check_robot
        def set_ready_state():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            state = info.get("state")
            response, code = self.robot_manager.set_ready_state(
                robot_name=robot_name,
                token=token,
                state=state
            )
            return jsonify(response), code

        """ Set robot position id """
        # TODO: determine access to the function (who has access)
        @robot_bp.route('/set-position-id', methods=['POST'])
        @self.access.check_robot_user(user_role="user", logger_module=self.logger_module)
        def set_position_id():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            position_id = info.get("id")
            response, code = self.robot_manager.set_position_id(
                robot_name=robot_name,
                token=token,
                position_id=position_id
            )
            return jsonify(response), code
          
        ''' Activate and deactivate emergency stop '''
        @robot_bp.route('/set-emergency', methods=['POST'])
        @self.access.check_robot_user(user_role="user", logger_module=self.logger_module)
        def set_emergency_state():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            state = info.get("state")
            response, code = self.robot_manager.set_emergency_state(
                robot_name=robot_name,
                token=token,
                state=state
            )
            return jsonify(response), code

        """ current robot position"""
        @robot_bp.route('/set-position', methods=['POST'])
        @self.access.check_robot_user_prog_token(user_role="user", logger_module=self.logger_module)
        def set_position():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            angles = info.get("angles")
            angles_data = info.get("angles_data")
            response, code = self.robot_manager.set_position(
                robot_name=robot_name,
                token=token,
                angles=angles,
                angles_data=angles_data
            )
            return jsonify(response), code
        
        """ Remove current robot point position """
        @robot_bp.route('/remove-current-point-position', methods=['POST'])
        @self.access.check_robot_user_prog_token(user_role="user", logger_module=self.logger_module)
        def remove_current_point_position():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            response, code = self.robot_manager.remove_current_point_position(
                robot_name=robot_name,
                token=token
            )
            return jsonify(response), code

        """ Remove all robot point positions """
        @robot_bp.route('/remove-all-point-position', methods=['POST'])
        @self.access.check_robot_user_prog_token(user_role="user", logger_module=self.logger_module)
        def remove_all_point_position():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            response, code = self.robot_manager.remove_all_point_position(
                robot_name=robot_name,
                token=token
            )
            return jsonify(response), code

        """ current home position"""
        @robot_bp.route('/set-home-position', methods=['POST'])
        @self.access.check_robot_user_prog(user_role="user", logger_module=self.logger_module)
        def set_home_position():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            angles = info.get("angles")
            response, code = self.robot_manager.set_home_position(
                robot_name=robot_name,
                token=token,
                angles=angles
            )
            return jsonify(response), code
        
        """ current robot speed """
        @robot_bp.route('/set-speed', methods=['POST'])
        @self.access.check_robot_user_prog_token(user_role="user", logger_module=self.logger_module)
        def set_speed():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            angles = info.get("angles")
            angles_data = info.get("angles_data")
            response, code = self.robot_manager.set_speed(
                robot_name=robot_name,
                token=token,
                angles=angles,
                angles_data=angles_data
            )
            return jsonify(response), code
        
        """ Remove current robot point speed """
        @robot_bp.route('/remove-current-point-speed', methods=['POST'])
        @self.access.check_robot_user_prog_token(user_role="user", logger_module=self.logger_module)
        def remove_current_point_speed():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            response, code = self.robot_manager.remove_current_point_speed(
                robot_name=robot_name,
                token=token
            )
            return jsonify(response), code

        """ Remove all robot point speeds """
        @robot_bp.route('/remove-all-point-speed', methods=['POST'])
        @self.access.check_robot_user_prog_token(user_role="user", logger_module=self.logger_module)
        def remove_all_point_speed():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            response, code = self.robot_manager.remove_all_point_speed(
                robot_name=robot_name,
                token=token
            )
            return jsonify(response), code

        """ standard robot speed"""
        @robot_bp.route('/set-standard-speed', methods=['POST'])
        @self.access.check_robot_user_prog(user_role="user", logger_module=self.logger_module)
        def set_standard_speed():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            angles = info.get("angles")
            response, code = self.robot_manager.set_standard_speed(
                robot_name=robot_name,
                token=token,
                angles=angles
            )
            return jsonify(response), code
        
        """ Set program """
        @robot_bp.route('/set-program', methods=['POST'])
        @self.access.check_robot_user(user_role="user", logger_module=self.logger_module)
        def set_program():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            program = info.get("program")
            response, code = self.robot_manager.set_program(
                robot_name=robot_name,
                token=token,
                program=program
            )
            return jsonify(response), code
        
        """ Delete program """
        @robot_bp.route('/delete-program', methods=['POST'])
        @self.access.check_robot_user(user_role="user", logger_module=self.logger_module)
        def delete_program():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            response, code = self.robot_manager.delete_program(
                robot_name=robot_name,
                token=token
            )
            return jsonify(response), code
        
        """ Get XYZ from angles robot position """
        @robot_bp.route('/angles-to-cartesian', methods=['POST'])
        @self.access.check_robot_user(user_role="user", logger_module=self.logger_module)
        def angles_to_cartesian():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            angles = info.get("angles")
            angles_data = info.get("angles_data")
            response, code = self.robot_manager.angles_to_cartesian(
                robot_name=robot_name,
                token=token,
                angles=angles,
                angles_data=angles_data
            )
            return jsonify(response), code
        
        """ Get angle from XYZ robot position """
        @robot_bp.route('/cartesian-to-angles', methods=['POST'])
        @self.access.check_robot_user(user_role="user", logger_module=self.logger_module)
        def cartesian_to_angles():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            position = info.get("position")
            positions_data = info.get("positions_data")
            coords_system = info.get("coordinate_system")
            response, code = self.robot_manager.cartesian_to_angles(
                robot_name=robot_name,
                token=token,
                position=position,
                positions_data=positions_data,
                coordinate_system=coords_system
            )
            return jsonify(response), code
        
        """ Set current robot XYZ position """
        @robot_bp.route('/set-cartesian-position', methods=['POST'])
        @self.access.check_robot_user_prog_token(user_role="user", logger_module=self.logger_module)
        def set_cartesian_position():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            position = info.get("position")
            positions_data = info.get("positions_data")
            coords_system = info.get("coordinate_system")
            response, code = self.robot_manager.set_cartesian_position(
                robot_name=robot_name,
                token=token,
                position=position,
                positions_data=positions_data,
                coordinate_system=coords_system
            )
            return jsonify(response), code
        
        ''' Set minimal angle of rotation '''
        @robot_bp.route('/set-min-angles', methods=['POST'])
        @self.access.check_robot_user_prog(user_role="administrator", logger_module=self.logger_module)
        def set_min_angles():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            angles = info.get("angles")
            response, code = self.robot_manager.set_min_angles(
                robot_name=robot_name,
                token=token,
                angles=angles
            )
            return jsonify(response), code

        ''' Set maximum angle of rotation '''
        @robot_bp.route('/set-max-angles', methods=['POST'])
        @self.access.check_robot_user_prog(user_role="administrator", logger_module=self.logger_module)
        def set_max_angles():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            angles = info.get("angles")
            response, code = self.robot_manager.set_max_angles(
                robot_name=robot_name,
                token=token,
                angles=angles
            )
            return jsonify(response), code

        ''' Set program is running '''
        @robot_bp.route('/set-program-run', methods=['POST'])
        @self.access.check_user(user_role="System", logger_module=self.logger_module)
        def set_program_run_state():
            info = request.json
            robot_name = info.get("robot")
            state = info.get("state")
            response, code = self.robot_manager.set_program_run_state(robot_name=robot_name, state=state)
            return jsonify(response), code
        
        # set robot tool
        @robot_bp.route("/set-robot-tool", methods=['POST'])
        @self.access.check_robot_user(user_role="user", logger_module=self.logger_module)
        def set_robot_tool():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            tool_id = info.get("id")
            response, code = self.robot_manager.set_robot_tool(
                robot_name=robot_name,
                token=token,
                tool_id=tool_id
            )
            return jsonify(response), code

        # set robot tool
        @robot_bp.route("/set-robot-base", methods=['POST'])
        @self.access.check_robot_user(user_role="user", logger_module=self.logger_module)
        def set_robot_base():
            info = request.json
            robot_name = info.get("robot")
            token = info.get("token")
            base_id = info.get("id")
            response, code = self.robot_manager.set_robot_base(
                robot_name=robot_name,
                token=token,
                base_id=base_id
            )
            return jsonify(response), code

        return robot_bp