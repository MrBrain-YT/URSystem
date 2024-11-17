from flask import Flask, request
from utils.loger import Loger

class ToolsManager:
    
    def __init__(self, tools:dict=None):
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
        
        # get tools
        @app.route("/URTools", methods=['POST'])
        def Tools():
            tools = globals()["tools"]
            if User.role_access(request.form.get("token"), "administrator"):
                User().update_token()
                return str(tools)
            else:
                loger.warning("URTools", f"User access denied to get tools. User with token: {request.form.get('token')}")
                return "You don't have enough rights"

        # get and set tool configuration
        @app.route("/URTool", methods=['POST'])
        def Tool():
            info = request.form
            tools = globals()["tools"]
            if User.role_access(info.get("token"), "user"):
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
            else:
                return "You are not on the users list"

        # creating tool 
        @app.route("/URTC", methods=['POST'])
        def URTC():
            info = request.form
            tools = globals()["tools"]
            if User.role_access(info.get("token"), "administrator"):
                if info.get("id") not in [i for i in tools.values()]:
                    tools[info.get("id")] = ""
                    System().SaveToCache(tools=tools)
                    User().update_token()
                    loger.info("URTools", f"Tool {info.get('id')} was created")
                    return "True"
                else:
                    loger.error("URTools", f"The tool {info.get('id')} already exists")
                    return "The tool already exists"
            else:
                loger.warning("URTools", f"User access denied to create tool. User with token: {request.form.get('token')}")
                return "You don't have enough rights"
            
        # delete tool
        @app.route("/URTD", methods=['POST'])
        def URTD():
            info = request.form
            tools = globals()["tools"]
            if User.role_access(info.get("token"), "administrator"):
                del tools[info.get("id")]
                System().SaveToCache(tools=tools)
                User().update_token()
                loger.info("URTools", f"Tool {info.get('id')} was deleted")
                return "True"
            else:
                loger.warning("URTools", f"User access denied to delete tool. User with token: {request.form.get('token')}")
                return "You don't have enough rights"
            
        return app