from flask import Blueprint, request, jsonify

from api.access_checker import Access
from services.multi_robots_manager import MultiRobotsManager

robots = {}

class MultiRobotsManagerAPI:
    robots = robots
    access = Access()
    
    def __init__(self, robots:dict=None):
        self.logger_module = "URMSystem"
        if robots is not None:
            self.multi_robot_manager = MultiRobotsManager(robots)
        else:
            self.multi_robot_manager = MultiRobotsManager()
    
    def __call__(self) -> Blueprint:
        
        robots_bp = Blueprint("robots_api", __name__, url_prefix="/api")
        
        # add robot
        @robots_bp.route("/crate-robot", methods=['POST'])
        @self.access.check_user(user_role="administrator", logger_module=self.logger_module)
        def create_robot():
            info = request.json
            robot_name = info.get("robot")
            robot_angle = info.get("angle")
            secret_code = info.get("code")
            password = info.get("password")
            kinematic_id = info.get("id")
            response, code = self.multi_robot_manager.create_robot(
                    robot_name=robot_name,
                    robot_angle=robot_angle,
                    secret_code=secret_code,
                    password=password,
                    kinematic_id=kinematic_id
                )
            return jsonify(response), code

        # Import robot cache
        @robots_bp.route("/import-cache", methods=['POST'])
        @self.access.check_user(user_role="SuperAdmin", logger_module=self.logger_module)
        def import_cache():
            info = request.json
            robots = info.get("robots")
            tools = info.get("tools")
            frames = info.get("frames")
            bases = info.get("bases")
            response, code = self.multi_robot_manager.import_cache(
                    import_robots=robots,
                    import_tools=tools,
                    import_bases=bases,
                    import_frames=frames
                )
            return jsonify(response), code
            
        # Export robot cache from cache file
        @robots_bp.route("/export-file-cache", methods=['POST'])
        @self.access.check_user(user_role="SuperAdmin", logger_module=self.logger_module)
        def export_file_cache():
            response, code = self.multi_robot_manager.export_file_cache()
            return jsonify(response), code
        
        # Export robot cache from RAM
        @robots_bp.route("/export-cache", methods=['POST'])
        @self.access.check_user(user_role="SuperAdmin", logger_module=self.logger_module)
        def export_ram_cache():
            response, code = self.multi_robot_manager.export_ram_cache()
            return jsonify(response), code

        # get robot
        @robots_bp.route("/get-robot", methods=['POST'])
        @self.access.check_user(user_role="administrator", logger_module=self.logger_module)
        def get_robot():
            info = request.json
            robot_name = info.get("robot")
            response, code = self.multi_robot_manager.get_robot(robot_name=robot_name)
            return jsonify(response), code
            
        # get robots
        @robots_bp.route("/get-robots", methods=['POST'])
        @self.access.check_user(user_role="administrator", logger_module=self.logger_module)
        def get_robots_api():
            response, code = self.multi_robot_manager.get_robots_api()
            return jsonify(response), code

        # delete robot
        @robots_bp.route("/delete-robot", methods=['POST'])
        @self.access.check_user(user_role="administrator", logger_module=self.logger_module)
        def delete_robot():
            info = request.json
            robot_name = info.get("robot")
            response, code = self.multi_robot_manager.delete_robot(robot_name=robot_name)
            return jsonify(response), code
            
        return robots_bp