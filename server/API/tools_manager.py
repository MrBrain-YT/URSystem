from flask import Flask, request
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
            return str(tools)


        # get and set tool configuration
        @app.route("/URTool", methods=['POST'])
        @access.check_user(user_role="user", loger_module=self.loger_module)
        def Tool():
            info = request.form
            tools = globals()["tools"]
            if info.get("type") == "write":
                if info.get("id") in [i for i in tools.values()]:
                    tools[info.get("id")] = info.get("config")
                    System().SaveToCache(tools=tools)
                    User().update_token()
                    return "True"
                else:
                    loger.error("URTools", f"The tool {info.get('id')} has not been created and cannot be modified")
                    return "The tool has not been created"
            else:
                return tools[info.get("id")]


        # creating tool 
        @app.route("/URTC", methods=['POST'])
        @access.check_user(user_role="administrator", loger_module=self.loger_module)
        def URTC():
            info = request.form
            tools = globals()["tools"]
            if info.get("id") not in [i for i in tools.values()]:
                tools[info.get("id")] = ""
                System().SaveToCache(tools=tools)
                User().update_token()
                loger.info("URTools", f"Tool {info.get('id')} was created")
                return "True"
            else:
                loger.error("URTools", f"The tool {info.get('id')} already exists")
                return "The tool already exists"

            
        # delete tool
        @app.route("/URTD", methods=['POST'])
        @access.check_user(user_role="administrator", loger_module=self.loger_module)
        def URTD():
            info = request.form
            tools = globals()["tools"]
            del tools[info.get("id")]
            System().SaveToCache(tools=tools)
            User().update_token()
            loger.info("URTools", f"Tool {info.get('id')} was deleted")
            return "True"
            
        return app