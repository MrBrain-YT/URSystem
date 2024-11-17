import secrets
import sqlite3

from flask import Flask, request

from utils.loger import Loger

class AccountManager:
    
    def __init__(self, users:dict=None):
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
        
        @app.route("/CreateAccount", methods=['POST'])
        def CreateAccount():
            info = request.form
            users:dict = globals()["users"]
            if User.role_access(info.get("token"), "administrator"):
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
                        loger.info("URAccount", f"Фccount with name: {info.get('name')} was created")
                        return token
                else:
                    loger.info("URAccount", f"The account has already been created")
                    return "The account has already been created"
            else:
                loger.warning("URAccount", f"User access denied to create account. User with token: {info.get('token')}")
                return "You don't have enough rights"
            
        @app.route("/DeleteAccount", methods=['POST'])
        def DeleteAccount():
            info = request.form
            users:dict = globals()["users"]
            if User.role_access(info.get("token"), "SuperAdmin"):
                if info.get("name") in users:
                    con = sqlite3.connect("Databases\\Users.sqlite")
                    cur = con.cursor()
                    res = cur.execute(f"DELETE FROM 'users' WHERE name = '{info.get('name')}'")
                    con.commit()
                    User().update_token()
                    loger.info("URAccount", f"Фccount with name: {info.get('name')} was deleted")
                    return "True"
                else:
                    return "No such account exists"
            else:
                loger.warning("URAccount", f"User access denied to delete account. User with token: {info.get('token')}")
                return "You don't have enough rights"
            
        # get account
        @app.route("/GetAccounts", methods=['POST'])
        def GetAccounts():
            info = request.form
            users:dict = globals()["users"]
            if User.role_access(info.get("token"), "SuperAdmin"):
                user = {}
                for i in users.copy():
                    user[i] = users.get(i) if users[i]["role"] != "SuperAdmin" else None
                User().update_token()
                return user
            else:
                loger.warning("URAccount", f"User access denied to get accounts. User with token: {info.get('token')}")
                return "You don't have enough rights"
            
        # get role account
        @app.route("/GetRoleAccount", methods=['POST'])
        def GetRoleAccount():
            info = request.form
            users:dict = globals()["users"]
            if info.get("server_token") == server_token.reg_token:
                User().update_token()
                if info.get("name") in users:
                    if users[info.get("name")]["password"] == info.get("password"):
                        return f"{users[info.get('name')]['role']},{users[info.get('name')]['token']}"
                    else:
                        loger.error("URAccount", f"Password incorrect")
                        return "False"
                else:
                    loger.error("URAccount", f"Name not in users")
                    return "False"
            else:
                loger.error("URAccount", f"Server token incorrect")
                return "Server token incorrect"

        # change password
        @app.route("/ChangePass", methods=['POST'])
        def change_password():
            info = request.form
            users:dict = globals()["users"]
            if User.role_access(info.get("token"), "SuperAdmin"):
                con = sqlite3.connect("Databases\\Users.sqlite")
                cur = con.cursor()
                cur.execute(f"UPDATE users SET password = '{info.get('password')}' WHERE name = '{info.get('name')}'")
                con.commit()
                con.close()
                User().update_token()
                loger.info("URAccount", f"Password was changed for account with name: {info.get('name')}")
                return "True"
            else:
                loger.warning("URAccount", f"User access denied to change password. User with token: {info.get('token')}")
                return "You don't have enough rights"
            
        # get user token
        @app.route("/GetToken", methods=['POST'])
        def get_user_token():
            info = request.form
            users:dict = globals()["users"]
            if User.role_access(info.get("token"), "SuperAdmin"):
                con = sqlite3.connect("Databases\\Users.sqlite")
                cur = con.cursor()
                cur.execute(f"SELECT token FROM users WHERE name = '{info.get('name')}, password = '{info.get('password')}'")
                token = cur.fetchone()
                con.commit()
                con.close()
                return token
            else:
                loger.warning("URAccount", f"User access denied to get token. User with token: {info.get('token')}")
                return "You don't have enough rights"
            
        # change user token
        @app.route("/ChangeToken", methods=['POST'])
        def changedoken():
            info = request.form
            users:dict = globals()["users"]
            if User.role_access(info.get("token"), "SuperAdmin"):
                while True:
                    token = secrets.token_hex(32)
                    tokens = []
                    for i in [i for i in users]:
                        tokens.append(users.get(i)["token"])
                    if token not in tokens:
                        break
                con = sqlite3.connect("Databases\\Users.sqlite")
                cur = con.cursor()
                cur.execute(f"UPDATE users SET token = '{token}' WHERE name = '{info.get('name')}' and password = '{info.get('password')}'")
                con.commit()
                con.close()
                loger.info("URAccount", f"Token was changed for account with name: {info.get('name')}")
                return token
            else:
                loger.warning("URAccount", f"User access denied to change token. User with token: {info.get('token')}")
                return "You don't have enough rights"
            
        return app