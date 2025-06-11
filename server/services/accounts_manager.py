import secrets
import hashlib

import sqlalchemy as db

from utils.logger import Logger
from databases.connection import users_table
from databases.database_manager import DBWorker
from utils.user_updater import update_token
import configuration.server_token as server_auth_token

users = {}

class AccountManager:
    users = users
    logger = Logger()
    database_worker = DBWorker()
    
    def __init__(self, users:dict=None) -> None:
        self.logger_module = "URAccounts"
        if users is not None:
            self.users.update(users)
    
    def get_users(self) -> dict:
        return self.users
    
    def set_users(self, users:dict) -> None:
        self.users.update(users)

    def create_account(self, name:str, password:str, role:str) -> tuple:
        if name not in self.users:
            token:str
            tokens = []
            for i in [i for i in self.users]:
                tokens.append(self.users.get(i)["token"])
            while True:
                token = secrets.token_hex(32)
                if token not in tokens:
                    break
            
            # DB query send
            password = hashlib.sha256(password.encode(encoding="utf-8")).hexdigest()
            query = db.insert(users_table).values(name=name, password=password, role=role, token=token)
            self.database_worker.send_query(query=query)

            update_token()
            log_message = f"Account with name: {name} was created"
            self.logger.info(module=self.logger_module, msg=log_message)
            return {"status": True, "info": log_message, "token": token}, 200
        else:
            log_message = "The account has already been created"
            self.logger.info(module=self.logger_module, msg=log_message)
            return {"status": False, "info": log_message}, 400

    def delete_account(self, name:str) -> tuple:
        print(self.users)
        if name in self.users:
            if self.users[name]["role"] not in {"SuperAdmin", "System"}:
                # DB query send
                query = users_table.delete().where(users_table.columns.name == name)
                self.database_worker.send_query(query=query)
                del self.users[name]

                update_token()
                log_message = f"Account with name: {name} was deleted"
                self.logger.info(module=self.logger_module, msg=log_message)
                return {"status": True, "info": log_message}, 200
        else:
            return {"status": False, "info": "No such account exists"}, 400
        
    # get accounts
    def get_accounts(self) -> tuple:
        _users = {}
        for info in self.users.copy():
            if self.users[info]["role"] not in {"SuperAdmin", "System"}:
                _users[info] = self.users.get(info)
        update_token()
        return {"status": True, "info": "Found users", "data": _users}, 200
        
    # get role account
    def get_account_data(self, name:str, password:str, server_token:str) -> tuple:
        if server_token == server_auth_token.reg_token:
            update_token()
            if name in self.users:
                if self.users[name]["role"] != "System":
                    if self.users[name]["password"] == password:
                        return {"status": True, "info": "User found", "data": self.users[name]}, 200
                    else:
                        self.logger.error(module=self.logger_module, msg=f"Password incorrect")
                        return {"status": False, "info": "Password incorrect"}, 400
                else:
                    self.logger.error(module=self.logger_module, msg=f"Account data with the System role cannot be transferred") # TODO: add ip address user to log
                    return {"status": False, "info": "Account data with the System role cannot be transferred"}, 400
            else:
                self.logger.error(module=self.logger_module, msg=f"Name not in users")
                return {"status": False, "info": "Name not in users"}, 404
        else:
            self.logger.error(module=self.logger_module, msg=f"Server token incorrect")
            return {"status": False, "info": "Server token incorrect"}, 400

    # change password
    def change_password(self, name:str, password:str) -> tuple:
        if name in self.users:
            if name != "":
                # DB query send
                query = users_table.update().where(
                    users_table.columns.name == name).values(password=password)
                self.database_worker.send_query(query=query)

                update_token()
                log_message = f"Password was changed for account with name: {name}"
                self.logger.info(module=self.logger_module, msg=log_message)
                return {"status": True, "info": log_message}, 200
            self.logger.error(module=self.logger_module, msg=f"You try change password system account")
            return {"status": False, "info": "You try change password system account"}, 400
        else:
            self.logger.error(module=self.logger_module, msg=f"Name not in users")
            return {"status": False, "info": "Name not in users"}, 404
        
    # get user token
    def get_user_token(self, name:str) -> tuple:
        if name in self.users:
            if name != "":
                query = db.select(users_table.columns.token).where(db.and_(users_table.columns.name == name))
                token = self.database_worker.send_select_query(query=query).fetchone()._tuple()
                return {"status": True, "info": "User token", "data": {"token": token[0]}}, 200
            else:
                self.logger.error(module=self.logger_module, msg=f"You try get token system account")
                return {"status": False, "info": "You try get token system account"}, 400
        else:
            self.logger.error(module=self.logger_module, msg=f"Name not in users")
            return {"status": False, "info": "Name not in users"}, 404

    # change user token
    def change_token(self, name:str, token:str=None) -> tuple:
        if token is None:
            while True:
                token = secrets.token_hex(32)
                tokens = []
                for i in [i for i in self.users]:
                    tokens.append(self.users.get(i)["token"])
                if token not in tokens:
                    break
        # DB query send
        query = users_table.update().where(db.and_(
            users_table.columns.name == name,
            users_table.columns.role != "System",
            users_table.columns.role != "robot")).values(token=token)
        self.database_worker.send_query(query=query)

        log_message = f"Token was changed for account with name: {name}"
        self.logger.info(module=self.logger_module, msg=log_message)
        return {"status": True, "info": log_message, "data": {"token": token}}, 200