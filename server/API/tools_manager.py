from flask import Flask, request, jsonify

from utils.loger import Loger

class ToolsManager:
    
    def __init__(self, tools:dict=None):
        self.loger_module = "URTools"
        if tools is not None:
            globals()["tools"] = tools
            
    @staticmethod
    def set_tools(tools: dict):
        globals()["tools"] = tools
    
    @staticmethod
    def get_tools() -> dict:
        return globals()["tools"]
    
    def __call__(self, app:Flask, loger: Loger) -> Flask:
        from server_functions import System, User
        from API.access_checker import Access

        access = Access()
        
        # get tools
        @app.route("/URTools", methods=['POST'])
        @access.check_user(user_role="administrator", loger_module=self.loger_module)
        def Tools():
            tools = globals()["tools"]
            User().update_token()
            return jsonify({"status": True, "info": "All tools data", "data": tools}), 200


        # get and set tool configuration
        @app.route("/URTool", methods=['POST'])
        @access.check_user(user_role="user", loger_module=self.loger_module)
        def Tool():
            info = request.json
            tools = globals()["tools"]
            if tools.get(info.get("id")) is not None:
                if info.get("type") == "write":
                    tools[info.get("id")] = info.get("config")
                    System().SaveToCache(tools=tools)
                    User().update_token()
                    return jsonify({"status": True, "info": "New tool value has been setted", "request_type": "write"}), 200
                else:
                    return jsonify({"status": True, "info": "Tool value", "data": tools[info.get("id")], "request_type": "read"}), 200
            else:
                log_message = f"The tool {info.get('id')} has not been created and cannot be modified"
                loger.error("URTools", log_message)
                return jsonify({"status": False, "info": log_message}), 400

        # creating tool 
        @app.route("/URTC", methods=['POST'])
        @access.check_user(user_role="administrator", loger_module=self.loger_module)
        def URTC():
            info = request.json
            tools = globals()["tools"]
            if info.get("id") not in [i for i in tools.values()]:
                tools[info.get("id")] = ""
                System().SaveToCache(tools=tools)
                User().update_token()
                log_message = f"Tool {info.get('id')} was created"
                loger.info("URTools", log_message)
                return jsonify({"status": True, "info": log_message}), 200
            else:
                log_message = f"The tool {info.get('id')} already exists"
                loger.error("URTools", log_message)
                return jsonify({"status": True, "info": log_message}), 400

            
        # delete tool
        @app.route("/URTD", methods=['POST'])
        @access.check_user(user_role="administrator", loger_module=self.loger_module)
        def URTD():
            info = request.json
            tools = globals()["tools"]
            del tools[info.get("id")]
            System().SaveToCache(tools=tools)
            User().update_token()
            log_message = f"Tool {info.get('id')} was deleted"
            loger.info("URTools", log_message)
            return jsonify({"status": True, "info": log_message}), 200
            
        return app