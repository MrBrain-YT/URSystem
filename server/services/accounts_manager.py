import secrets
import hashlib

import sqlalchemy as db

from utils.logger import Logger
from databases.connection import users_table
from databases.database_manager import DBWorker
from utils.user_updater import update_token
from utils.validator import UserChecker, ServerChecker, validate_types

users = {}

class AccountManager:
    users = users
    logger = Logger()
    database_worker = DBWorker()
    user_checker = UserChecker()
    server_checker = ServerChecker()
    
    def __init__(self, users:dict=None) -> None:
        self.logger_module = "URAccounts"
        if users is not None:
            self.users.update(users)
    
    def get_users(self) -> dict:
        return self.users
    
    def set_users(self, users:dict) -> None:
        self.users.update(users)

    @validate_types
    def create_account(self, name:str, password:str, role:str) -> tuple:
        if not self.user_checker.is_user(name):
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

    @validate_types
    def delete_account(self, name:str) -> tuple:
        if self.user_checker.is_user(name):
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
    @validate_types
    def get_accounts(self) -> tuple:
        _users = {}
        for info in self.users.copy():
            if self.users[info]["role"] not in {"SuperAdmin", "System"}:
                _users[info] = self.users.get(info)
        update_token()
        return {"status": True, "info": "Found users", "data": _users}, 200
        
    # get role account
    @validate_types
    def get_account_data(self, name:str, password:str, server_token:str) -> tuple:
        if self.server_checker.is_server_token(server_token):
            update_token()
            if self.user_checker.is_user(name):
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
    @validate_types
    def change_password(self, name:str, password:str) -> tuple:
        if self.user_checker.is_user(name):
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
    @validate_types
    def get_user_token(self, name:str) -> tuple:
        if self.user_checker.is_user(name):
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
    @validate_types
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