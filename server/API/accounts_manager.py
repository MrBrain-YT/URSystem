import secrets
import json

from flask import Flask, request, jsonify
import sqlalchemy as db

from utils.loger import Loger
from server_functions import users_table, conn

class AccountManager:
    
    def __init__(self, users:dict=None):
        self.loger_module = "URAccounts"
        if users is not None:
            globals()["users"] = users
    
    @staticmethod
    def get_users():
        return globals()["users"]
    
    @staticmethod
    def set_users(users:dict):
        globals()["users"] = users
    
    def __call__(self, app:Flask) -> Flask:
        from server_functions import User
        from configuration import server_token 
        from API.access_checker import Access

        loger = Loger()
        access = Access()
        
        @app.route("/CreateAccount", methods=['POST'])
        @access.check_user(user_role="administrator", loger_module=self.loger_module)
        def CreateAccount():
            info = request.json
            users:dict = globals()["users"]
            if info.get("name") not in users:
                token:str
                tokens = []
                for i in [i for i in users]:
                    tokens.append(users.get(i)["token"])
                while True:
                    token = secrets.token_hex(32)
                    if token not in tokens:
                        break
                
                # DB query send
                query = db.insert(users_table).values(name=info.get('name'), password=info.get('password'), role=info.get('user_role'), token=token)
                conn.execute(query)
                conn.commit()

                User().update_token()
                log_message = f"Account with name: {info.get('name')} was created"
                loger.info(module=self.loger_module, msg=log_message)
                return jsonify({"status": True, "info": log_message, "token": token}), 200
            else:
                log_message = f"The account has already been created"
                loger.info(module=self.loger_module, msg=log_message)
                return jsonify({"status": False, "info": log_message}), 400
            
        @app.route("/DeleteAccount", methods=['POST'])
        @access.check_user(user_role="SuperAdmin", loger_module=self.loger_module)
        def DeleteAccount():
            info = request.json
            users:dict = globals()["users"]
            if info.get("name") in users:
                if users[info.get("name")]["role"] not in {"SuperAdmin", "System"}:
                    # DB query send
                    query = users_table.delete().where(users_table.columns.name == info.get('name'))
                    conn.execute(query)
                    conn.commit()

                    User().update_token()
                    log_message = f"Account with name: {info.get('name')} was deleted"
                    loger.info(module=self.loger_module, msg=log_message)
                    return jsonify({"status": True, "info": log_message}), 200
            else:
                return jsonify({"status": False, "info": "No such account exists"}), 400
            
        # get account
        @app.route("/GetAccounts", methods=['POST'])
        @access.check_user(user_role="SuperAdmin", loger_module=self.loger_module)
        def GetAccounts():
            users:dict = globals()["users"]
            user = {}
            for info in users.copy():
                if users[info]["role"] not in {"SuperAdmin", "System"}:
                    user[info] = users.get(info)
            User().update_token()
            return jsonify({"status": True, "info": "Found users", "users": json.dumps(user)}), 200
            
        # get role account
        @app.route("/GetRoleAccount", methods=['POST'])
        def GetRoleAccount():
            info = request.json
            users:dict = globals()["users"]
            if info.get("server_token") == server_token.reg_token:
                User().update_token()
                if info.get("name") in users:
                    if users[info.get("name")]["role"] not in {"System"}:
                        if users[info.get("name")]["password"] == info.get("password"):
                            role = users[info.get('name')]['role']
                            token = users[info.get('name')]['token']
                            return jsonify({"status": True, "info": "User found", "role": role, "token": token}), 200
                        else:
                            loger.error(module=self.loger_module, msg=f"Password incorrect")
                            return jsonify({"status": False, "info": "Password incorrect"}), 400
                    else:
                        loger.error(module=self.loger_module, msg=f"Account data with the System role cannot be transferred") # TODO: add ip address user to log
                        return jsonify({"status": False, "info": "Account data with the System role cannot be transferred"}), 400
                else:
                    loger.error(module=self.loger_module, msg=f"Name not in users")
                    return jsonify({"status": False, "info": "Name not in users"}), 404
            else:
                loger.error(module=self.loger_module, msg=f"Server token incorrect")
                return jsonify({"status": False, "info": "Server token incorrect"}), 400

        # change password
        @app.route("/ChangePass", methods=['POST'])
        @access.check_user(user_role="SuperAdmin", loger_module=self.loger_module)
        def change_password():
            info = request.json
            users:dict = globals()["users"]
            if info.get("name") in users:
                if info.get("name") != "":
                    # DB query send
                    query = users_table.update().where(
                        users_table.columns.name == info.get('name')).values(password=info.get('password'))
                    conn.execute(query)
                    conn.commit()

                    User().update_token()
                    log_message = f"Password was changed for account with name: {info.get('name')}"
                    loger.info(module=self.loger_module, msg=log_message)
                    return jsonify({"status": True, "info": log_message}), 200
                loger.error(module=self.loger_module, msg=f"You try change password system account")
                return jsonify({"status": False, "info": "You try change password system account"}), 400
            else:
                loger.error(module=self.loger_module, msg=f"Name not in users")
                return jsonify({"status": False, "info": "Name not in users"}), 404
        # get user token
        @app.route("/GetToken", methods=['POST'])
        @access.check_user(user_role="SuperAdmin", loger_module=self.loger_module)
        def get_user_token():
            info = request.json
            users:dict = globals()["users"]
            if info.get("name") in users:
                if info.get("name") != "":
                    query = db.select(users_table.columns.token).where(db.and_(users_table.columns.name == info.get('name'), users_table.columns.password == info.get('password')))
                    token = conn.execute(query).fetchone()._tuple()
                    return jsonify({"status": True, "info": "", "token": token}), 200
                else:
                    loger.error(module=self.loger_module, msg=f"You try get token system account")
                    return jsonify({"status": False, "info": "You try get token system account"}), 400
            else:
                loger.error(module=self.loger_module, msg=f"Name not in users")
                return jsonify({"status": False, "info": "Name not in users"}), 404

        # change user token
        @app.route("/ChangeToken", methods=['POST'])
        @access.check_user(user_role="SuperAdmin", loger_module=self.loger_module)
        def changetoken():
            info = request.json
            users:dict = globals()["users"]
            while True:
                token = secrets.token_hex(32)
                tokens = []
                for i in [i for i in users]:
                    tokens.append(users.get(i)["token"])
                if token not in tokens:
                    break
            # DB query send
            query = users_table.update().where(db.and_(
                users_table.columns.name == info.get('name'),
                users_table.columns.password == info.get('password'),
                users_table.columns.role != "System"),
                users_table.columns.role != "robot").values(token=token)
            conn.execute(query)
            conn.commit()

            log_message = f"Token was changed for account with name: {info.get('name')}"
            loger.info(module=self.loger_module, msg=log_message)
            return jsonify({"status": True, "info": log_message, "token": token}), 200

        return app