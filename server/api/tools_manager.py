from flask import Blueprint, request, jsonify

from api.access_checker import Access
from services.tools_manager import ToolsManager

class ToolsManagerAPI:
    access = Access()
    
    def __init__(self, tools:dict=None):
        self.logger_module = "URTools"
        if tools is not None:
            self.tools_manager = ToolsManager(tools)
        else:
            self.tools_manager = ToolsManager()
    
    def __call__(self) -> Blueprint:
        
        tools_bp = Blueprint("tools_api", __name__, url_prefix="/api")

        # get tools
        @tools_bp.route("/get-tools", methods=['POST'])
        @self.access.check_user(user_role="administrator", logger_module=self.logger_module)
        def get_tools():
            response, code = self.tools_manager.get_tools_api()
            return jsonify(response), code

        # get and set tool configuration
        @tools_bp.route("/get-tool", methods=['POST'])
        @self.access.check_user(user_role="user", logger_module=self.logger_module)
        def get_tool_data():
            info = request.json
            tool_id = info.get("id")
            response, code = self.tools_manager.get_tool_data(
                    tool_id=tool_id
                )
            return jsonify(response), code
        
        @tools_bp.route("/set-tool", methods=['POST'])
        @self.access.check_user(user_role="user", logger_module=self.logger_module)
        def set_tool_data():
            info = request.json
            tool_id = info.get("id")
            parameter = info.get("parameter")
            parametr_config = info.get("value")
            response, code = self.tools_manager.set_tool_data(
                    tool_id=tool_id,
                    parameter=parameter,
                    config=parametr_config
                )
            return jsonify(response), code
            
        # set tool calibration data
        @tools_bp.route("/set-tool-calibration", methods=['POST'])
        @self.access.check_user(user_role="administrator", logger_module=self.logger_module)
        def set_calibration():
            info = request.json
            tool_id = info.get("id")
            calibration_data = info.get("calibration_data")
            response, code = self.tools_manager.set_calibration_data(tool_id=tool_id, calibration_data=calibration_data)
            return jsonify(response), code
            
        # create tool 
        @tools_bp.route("/create-tool", methods=['POST'])
        @self.access.check_user(user_role="administrator", logger_module=self.logger_module)
        def create_tool():
            info = request.json
            tool_id = info.get("id")
            response, code = self.tools_manager.create_tool(tool_id=tool_id)
            return jsonify(response), code

        # delete tool
        @tools_bp.route("/delete-tool", methods=['POST'])
        @self.access.check_user(user_role="administrator", logger_module=self.logger_module)
        def delete_tool():
            info = request.json
            tool_id = info.get("id")
            response, code = self.tools_manager.delete_tool(tool_id=tool_id)
            return jsonify(response), code
            
        return tools_bp