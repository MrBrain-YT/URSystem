import secrets
import sqlite3
import json

from flask import Flask, request, jsonify

from utils.loger import Loger

class AccountManager:
    
    def __init__(self, users:dict=None):
        self.loger_module = "URAccount"
        if users is not None:
            globals()["users"] = users
    
    @staticmethod
    def get_users():
        return globals()["users"]
    
    @staticmethod
    def set_users(users:dict):
        globals()["users"] = users
    
    def __call__(self, app:Flask, loger:Loger) -> Flask:
        from server_functions import User
        from configuration import server_token 
        from API.access_checker import Access

        access = Access()
        
        @app.route("/CreateAccount", methods=['POST'])
        @access.check_user(user_role="administrator", loger_module=self.loger_module)
        def CreateAccount():
            info = request.json
            users:dict = globals()["users"]

            if info.get("name") not in users:
                while True:
                    token = secrets.token_hex(32)
                    tokens = []
                    for i in [i for i in users]:
                        tokens.append(users.get(i)["token"])
                    if token not in tokens:
                        break
                    con = sqlite3.connect("Databases\\Users.sqlite")
                    cur = con.cursor()
                    res = cur.execute(f"INSERT INTO users VALUES ('{info.get('name')}', '{info.get('password')}', '{info.get('user_role')}', '{token}')")
                    con.commit()
                    loger.info("URAccount", f"Account was created with name-{info.get('name')} and password-{info.get('password')}")
                    User().update_token()
                    log_message = f"Account with name: {info.get('name')} was created"
                    loger.info("URAccount", log_message)
                    return jsonify({"status": True, "info": log_message, "token": token}), 200
            else:
                log_message = f"The account has already been created"
                loger.info("URAccount", log_message)
                return jsonify({"status": False, "info": log_message}), 400
            
        @app.route("/DeleteAccount", methods=['POST'])
        @access.check_user(user_role="SuperAdmin", loger_module=self.loger_module)
        def DeleteAccount():
            info = request.json
            users:dict = globals()["users"]
            if info.get("name") in users:
                if users[info.get("name")]["role"] not in {"SuperAdmin", "System"}:
                    con = sqlite3.connect("Databases\\Users.sqlite")
                    cur = con.cursor()
                    res = cur.execute(f"DELETE FROM 'users' WHERE name = '{info.get('name')}'")
                    con.commit()
                    User().update_token()
                    log_message = f"Account with name: {info.get('name')} was deleted"
                    loger.info("URAccount", log_message)
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
                            loger.error("URAccount", f"Password incorrect")
                            return jsonify({"status": False, "info": "Password incorrect"}), 400
                    else:
                        loger.error("URAccount", f"Account data with the System role cannot be transferred") # TODO: add ip address user to log
                        return jsonify({"status": False, "info": "Account data with the System role cannot be transferred"}), 400
                else:
                    loger.error("URAccount", f"Name not in users")
                    return jsonify({"status": False, "info": "Name not in users"}), 404
            else:
                loger.error("URAccount", f"Server token incorrect")
                return jsonify({"status": False, "info": "Server token incorrect"}), 400

        # change password
        @app.route("/ChangePass", methods=['POST'])
        @access.check_user(user_role="SuperAdmin", loger_module=self.loger_module)
        def change_password():
            info = request.json
            users:dict = globals()["users"]
            if info.get("name") in users:
                if info.get("name") != "":
                    con = sqlite3.connect("Databases\\Users.sqlite")
                    cur = con.cursor()
                    cur.execute(f"UPDATE users SET password = '{info.get('password')}' WHERE name = '{info.get('name')}'")
                    con.commit()
                    con.close()
                    User().update_token()
                    log_message = f"Password was changed for account with name: {info.get('name')}"
                    loger.info("URAccount", )
                    return jsonify({"status": True, "info": log_message}), 200
                loger.error("URAccount", f"You try change password system account")
                return jsonify({"status": False, "info": "You try change password system account"}), 400
            else:
                loger.error("URAccount", f"Name not in users")
                return jsonify({"status": False, "info": "Name not in users"}), 404
        # get user token
        @app.route("/GetToken", methods=['POST'])
        @access.check_user(user_role="SuperAdmin", loger_module=self.loger_module)
        def get_user_token():
            info = request.json
            users:dict = globals()["users"]
            if info.get("name") in users:
                if info.get("name") != "":
                    con = sqlite3.connect("Databases\\Users.sqlite")
                    cur = con.cursor()
                    cur.execute(f"SELECT token FROM users WHERE name = '{info.get('name')}, password = '{info.get('password')}'")
                    token = cur.fetchone()
                    con.commit()
                    con.close()
                    return jsonify({"status": True, "info": "", "token": token}), 200
                else:
                    loger.error("URAccount", f"You try get token system account")
                    return jsonify({"status": False, "info": "You try get token system account"}), 400
            else:
                loger.error("URAccount", f"Name not in users")
                return jsonify({"status": False, "info": "Name not in users"}), 404

        # change user token
        @app.route("/ChangeToken", methods=['POST'])
        @access.check_user(user_role="SuperAdmin", loger_module=self.loger_module)
        def changedoken():
            info = request.json
            users:dict = globals()["users"]
            while True:
                token = secrets.token_hex(32)
                tokens = []
                for i in [i for i in users]:
                    tokens.append(users.get(i)["token"])
                if token not in tokens:
                    break
            con = sqlite3.connect("Databases\\Users.sqlite")
            cur = con.cursor()
            cur.execute(f"UPDATE users SET token = '{token}' WHERE name = '{info.get('name')}' and password = '{info.get('password')}' WHERE role != 'System' and role != 'robot'")
            con.commit()
            con.close()
            log_message = f"Token was changed for account with name: {info.get('name')}"
            loger.info("URAccount", log_message)
            return jsonify({"status": True, "info": log_message, "token": token}), 200

        return app