from utils.logger import Logger
from utils.user_updater import update_token
from configuration.cache.file_cache import save_to_cache

tools = {}

class ToolsManager:
    tools = tools
    logger = Logger()
    
    def __init__(self, tools:dict=None) -> None:
        self.logger_module = "URTools"
        if tools is not None:
            self.tools.update(tools)
            
    def set_tools(self, tools: dict):
        self.tools.update(tools)
    
    def get_tools(self) -> dict:
        return self.tools
    
    # get tools
    def get_tools_api(self) -> tuple:
        update_token()
        return {"status": True, "info": "All tools data", "data": self.tools}, 200
    
    def get_tool_data(self, tool_id:str) -> tuple:
        if self.tools.get(tool_id) is not None:
            return {"status": True, "info": "Tool value", "data": self.tools[tool_id]}, 200
        else:
            log_message = f"The tool '{tool_id}' has not been created and cannot be modified"
            self.logger.error(module=self.logger_module, msg=log_message)
            return {"status": False, "info": log_message}, 400
        
    def set_tool_data(self, tool_id:str, parameter:str, config:str) -> tuple:
        if self.tools.get(tool_id) is not None:
            self.tools[tool_id][parameter] = config
            save_to_cache(tools=self.tools)
            update_token()
            return {"status": True, "info": "New tool value has been setted", "request_type": "write"}, 200
        else:
            log_message = f"The tool {tool_id} has not been created and cannot be modified"
            self.logger.error(module=self.logger_module, msg=log_message)
            return {"status": False, "info": log_message}, 400
        
    # set tool calibration data
    def set_calibration_data(self, tool_id:str, calibration_data:dict) -> tuple:
        if self.tools.get(tool_id) is not None:
            if isinstance(calibration_data, dict):
                self.tools[tool_id]["calibrated_vector"] = calibration_data
                save_to_cache(tools=self.tools)
                update_token()
                log_message = f"The tool {tool_id} was been setted calibration data" + str(calibration_data)
                self.logger.info(module=self.logger_module, msg=log_message)
                return {"status": True, "info": log_message}, 200
            else:
                log_message = f"Calibration data not valid"
                self.logger.error(module=self.logger_module, msg=log_message)
                return {"status": False, "info": log_message}, 400
        else:
            log_message = f"The tool was not found"
            self.logger.error(module=self.logger_module, msg=log_message)
            return {"status": False, "info": log_message}, 403
        
    # creating tool 
    def create_tool(self, tool_id:str) -> tuple:
        if tool_id not in [i for i in self.tools.keys()]:
            self.tools[tool_id] = {}
            save_to_cache(tools=self.tools)
            update_token()
            log_message = f"Tool {tool_id} was created"
            self.logger.info(module=self.logger_module, msg=log_message)
            return {"status": True, "info": log_message}, 200
        else:
            log_message = f"The tool {tool_id} already exists"
            self.logger.error(module=self.logger_module, msg=log_message)
            return {"status": True, "info": log_message}, 400
        
    # delete tool
    def delete_tool(self, tool_id:str) -> tuple:
        from services.multi_robots_manager import MultiRobotsManager
        if self.tools.get(tool_id) is not None:
            robots = MultiRobotsManager().get_robots()
            del self.tools[tool_id]
            for key, value in robots.items():
                    if robots[key]["Tool"] == tool_id:
                        robots[key]["Tool"] = ""
            save_to_cache(robots=robots, tools=self.tools)
            update_token()
            log_message = f"Tool {tool_id} was deleted"
            self.logger.info(module=self.logger_module, msg=log_message)
            return {"status": True, "info": log_message}, 200
        else:
            log_message = f"The tool was not found"
            self.logger.error(module=self.logger_module, msg=log_message)
            return {"status": False, "info": log_message}, 403