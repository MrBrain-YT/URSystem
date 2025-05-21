from flask import Flask, request, jsonify

from services.robot_manager import RobotManager
from API.access_checker import Access

class RobotManagerAPI:
    access = Access()
    
    def __init__(self, robots:dict=None):
        self.logger_module = "URManager"
        self.robot_manager = RobotManager(robots)
    
    def __call__(self, app: Flask) -> Flask:

        """ Get curent robot position """
        @app.route('/get-position', methods=['POST'])
        @self.access.check_robot_or_user(user_role="user", logger_module=self.logger_module)
        def get_position():
            info = request.json
            robot_name = info.get("robot")
            responce, code = self.robot_manager.get_position(robot_name=robot_name)
            return jsonify(responce), code
        
        """ Get robot position id """
        @app.route('/get-position-id', methods=['POST'])
        @self.access.check_robot_or_user(user_role="user", logger_module=self.logger_module)
        def get_position_id():
            info = request.json
            robot_name = info.get("robot")
            responce, code = self.robot_manager.get_position_id(robot_name=robot_name)
            return jsonify(responce), code
        
        """ Get curent robot speed """
        @app.route('/get-speed', methods=['POST'])
        @self.access.check_robot
        def get_speed():
            info = request.json
            robot_name = info.get("robot")
            responce, code = self.robot_manager.get_speed(robot_name=robot_name)
            return jsonify(responce), code
        
        """ Get curent robot position """
        @app.route('/get-cartesian-position', methods=['POST'])
        @self.access.check_robot_or_user(user_role="user", logger_module=self.logger_module)
        def get_catesian_position():
            info = request.json
            robot_name = info.get("robot")
            responce, code = self.robot_manager.get_catesian_position(robot_name=robot_name)
            return jsonify(responce), code
        
        """ Get robot angles count """
        @app.route('/get-angles-count', methods=['POST'])
        @self.access.check_robot_or_user(user_role="user", logger_module=self.logger_module)
        def get_angles_count():
            info = request.json
            robot_name = info.get("robot")
            responce, code = self.robot_manager.get_angles_count(robot_name=robot_name)
            return jsonify(responce), code
        
        """ Set curent robot motor position """
        @app.route('/set-motors-position', methods=['POST'])
        @self.access.check_robot
        def set_motors_position():
            info = request.json
            robot_name = info.get("robot")
            angles = info.get("angles")
            responce, code = self.robot_manager.set_motors_position(robot_name=robot_name, angles=angles)
            return jsonify(responce), code
        
        """ Get robot ready parameter """
        @app.route('/get-ready', methods=['POST'])
        @self.access.check_robot
        def get_ready_state():
            info = request.json
            robot_name = info.get("robot")
            responce, code = self.robot_manager.get_ready_state(robot_name=robot_name)
            return jsonify(responce), code
        
        ''' Get emergency stop '''
        @app.route('/get-emergency', methods=['POST'])
        @self.access.check_robot_or_user(user_role="user", logger_module=self.logger_module)
        def get_emergency_state():
            info = request.json
            robot_name = info.get("robot")
            responce, code = self.robot_manager.get_emergency_state(robot_name=robot_name)
            return jsonify(responce), code
        
        """ Set robot ready parameter """
        @app.route('/set-ready', methods=['POST'])
        @self.access.check_robot
        def set_ready_state():
            info = request.json
            robot_name = info.get("robot")
            state = info.get("state")
            responce, code = self.robot_manager.set_ready_state(robot_name=robot_name, state=state)
            return jsonify(responce), code
        
        """ Set robot position id """
        # TODO: determine access to the function (who has access)
        @app.route('/set-position-id', methods=['POST'])
        @self.access.check_robot_user(user_role="user", logger_module=self.logger_module)
        def set_position_id():
            info = request.json
            robot_name = info.get("robot")
            position_id = info.get("id")
            responce, code = self.robot_manager.set_position_id(
                    robot_name=robot_name,
                    position_id=position_id
                )
            return jsonify(responce), code
          
        ''' Activate and deativate emergency stop '''
        @app.route('/set-emergency', methods=['POST'])
        @self.access.check_robot_user(user_role="user", logger_module=self.logger_module)
        def set_emergency_state():
            info = request.json
            robot_name = info.get("robot")
            state = info.get("state")
            responce, code = self.robot_manager.set_emergency_state(robot_name=robot_name, state=state)
            return jsonify(responce), code
        
        """ Curent robot position"""
        @app.route('/set-position', methods=['POST'])
        @self.access.check_robot_user_prog_token(user_role="user", logger_module=self.logger_module)
        def set_position():
            info = request.json
            robot_name = info.get("robot")
            angles = info.get("angles")
            angles_data = info.get("angles_data")
            responce, code = self.robot_manager.set_position(
                    robot_name=robot_name,
                    angles=angles,
                    angles_data=angles_data
                )
            return jsonify(responce), code
        
        """ Remove curent robot point position """
        @app.route('/remove-curent-point-position', methods=['POST'])
        @self.access.check_robot_user_prog_token(user_role="user", logger_module=self.logger_module)
        def remove_curent_point_position():
            info = request.json
            robot_name = info.get("robot")
            responce, code = self.robot_manager.remove_curent_point_position(robot_name=robot_name)
            return jsonify(responce), code
        
        """ Remove all robot point positions """
        @app.route('/remove-all-point-position', methods=['POST'])
        @self.access.check_robot_user_prog_token(user_role="user", logger_module=self.logger_module)
        def remove_all_point_position():
            info = request.json
            robot_name = info.get("robot")
            responce, code = self.robot_manager.remove_all_point_position(robot_name=robot_name)
            return jsonify(responce), code
        
        """ Curent home position"""
        @app.route('/set-home-position', methods=['POST'])
        @self.access.check_robot_user_prog(user_role="user", logger_module=self.logger_module)
        def set_home_position():
            info = request.json
            robot_name = info.get("robot")
            angles = info.get("angles")
            responce, code = self.robot_manager.set_home_position(robot_name=robot_name, angles=angles)
            return jsonify(responce), code
        
        """ Curent robot speed """
        @app.route('/set-speed', methods=['POST'])
        @self.access.check_robot_user_prog_token(user_role="user", logger_module=self.logger_module)
        def set_speed():
            info = request.json
            robot_name = info.get("robot")
            angles = info.get("angles")
            angles_data = info.get("angles_data")
            responce, code = self.robot_manager.set_speed(
                    robot_name=robot_name,
                    angles=angles,
                    angles_data=angles_data
                )
            return jsonify(responce), code
        
        """ Remove curent robot point speed """
        @app.route('/remove-curent-point-speed', methods=['POST'])
        @self.access.check_robot_user_prog_token(user_role="user", logger_module=self.logger_module)
        def remove_curent_point_speed():
            info = request.json
            robot_name = info.get("robot")
            responce, code = self.robot_manager.remove_curent_point_speed(robot_name=robot_name)
            return jsonify(responce), code
            
        """ Remove all robot point speeds """
        @app.route('/remove-all-point-speed', methods=['POST'])
        @self.access.check_robot_user_prog_token(user_role="user", logger_module=self.logger_module)
        def remove_all_point_speed():
            info = request.json
            robot_name = info.get("robot")
            responce, code = self.robot_manager.remove_all_point_speed(robot_name=robot_name)
            return jsonify(responce), code
        
        """ Standart robot speed"""
        @app.route('/set-standart-speed', methods=['POST'])
        @self.access.check_robot_user_prog(user_role="user", logger_module=self.logger_module)
        def set_standart_speed():
            info = request.json
            robot_name = info.get("robot")
            angles = info.get("angles")
            responce, code = self.robot_manager.set_standart_speed(robot_name=robot_name, angles=angles)
            return jsonify(responce), code
        
        """ Set program """
        @app.route('/set-program', methods=['POST'])
        @self.access.check_robot_user(user_role="user", logger_module=self.logger_module)
        def set_program():
            info = request.json
            robot_name = info.get("robot")
            program = info.get("program")
            responce, code = self.robot_manager.set_program(robot_name=robot_name, program=program)
            return jsonify(responce), code
        
        """ Delete program """
        @app.route('/delete-program', methods=['POST'])
        @self.access.check_robot_user(user_role="user", logger_module=self.logger_module)
        def delete_program():
            info = request.json
            robot_name = info.get("robot")
            responce, code = self.robot_manager.delete_program(robot_name=robot_name)
            return jsonify(responce), code
        
        """ Get XYZ from angles robot position """
        @app.route('/angles-to-cartesian', methods=['POST'])
        @self.access.check_robot_user(user_role="user", logger_module=self.logger_module)
        def angles_to_cartesian():
            info = request.json
            robot_name = info.get("robot")
            angles = info.get("angles")
            angles_data = info.get("angles_data")
            responce, code = self.robot_manager.angles_to_cartesian(
                    robot_name=robot_name,
                    angles=angles,
                    angles_data=angles_data
                )
            return jsonify(responce), code
        
        """ Get angle from XYZ robot position """
        @app.route('/cartesian-to-angles', methods=['POST'])
        @self.access.check_robot_user(user_role="user", logger_module=self.logger_module)
        def cartesian_to_angles():
            info = request.json
            robot_name = info.get("robot")
            position = info.get("position")
            positions_data = info.get("positions_data")
            coords_system = info.get("coordinate_system")
            responce, code = self.robot_manager.cartesian_to_angles(
                    robot_name=robot_name,
                    position=position,
                    positions_data=positions_data,
                    coordinate_system=coords_system
                )
            return jsonify(responce), code
        
        """ Set curent robot XYZ position """
        @app.route('/set-cartesian-position', methods=['POST'])
        @self.access.check_robot_user_prog_token(user_role="user", logger_module=self.logger_module)
        def set_cartesian_position():
            info = request.json
            robot_name = info.get("robot")
            position = info.get("position")
            positions_data = info.get("positions_data")
            coords_system = info.get("coordinate_system")
            responce, code = self.robot_manager.set_cartesian_position(
                    robot_name=robot_name,
                    position=position,
                    positions_data=positions_data,
                    coordinate_system=coords_system
                )
            return jsonify(responce), code
        
        ''' Set minimal angle of rotation '''
        @app.route('/set-min-angles', methods=['POST'])
        @self.access.check_robot_user_prog(user_role="administrator", logger_module=self.logger_module)
        def set_min_angles():
            info = request.json
            robot_name = info.get("robot")
            angles = info.get("angles")
            responce, code = self.robot_manager.set_min_angles(robot_name=robot_name, angles=angles)
            return jsonify(responce), code
        
        ''' Set maximum angle of rotation '''
        @app.route('/set-max-angles', methods=['POST'])
        @self.access.check_robot_user_prog(user_role="administrator", logger_module=self.logger_module)
        def set_max_angles():
            info = request.json
            robot_name = info.get("robot")
            angles = info.get("angles")
            responce, code = self.robot_manager.set_max_angles(robot_name=robot_name, angles=angles)
            return jsonify(responce), code
        
        ''' Set program is running '''
        @app.route('/set-program-run', methods=['POST'])
        @self.access.check_user(user_role="System", logger_module=self.logger_module)
        def set_program_run_state():
            info = request.json
            robot_name = info.get("robot")
            state = info.get("state")
            responce, code = self.robot_manager.set_program_run_state(robot_name=robot_name, state=state)
            return jsonify(responce), code
        
        # set robot tool
        @app.route("/set-robot-tool", methods=['POST'])
        @self.access.check_robot_user(user_role="user", logger_module=self.logger_module)
        def set_robot_tool():
            info = request.json
            robot_name = info.get("robot")
            tool_id = info.get("id")
            responce, code = self.robot_manager.set_robot_tool(robot_name=robot_name, tool_id=tool_id)
            return jsonify(responce), code
        
        # set robot tool
        @app.route("/set-robot-base", methods=['POST'])
        @self.access.check_robot_user(user_role="user", logger_module=self.logger_module)
        def set_robot_base():
            info = request.json
            robot_name = info.get("robot")
            base_id = info.get("id")
            responce, code = self.robot_manager.set_robot_base(robot_name=robot_name, base_id=base_id)
            return jsonify(responce), code
        
        return app