from flask import Flask, request, jsonify

from services.accounts_manager import AccountManager
from API.access_checker import Access

class AccountManagerAPI:
    access = Access()
    
    def __init__(self, users:dict=None) -> None:
        self.logger_module = "URAccounts"
        if users is not None:
            self.accounts_manager = AccountManager(users)
        else:
            self.accounts_manager = AccountManager()
    
    def __call__(self, app:Flask) -> Flask:

        @app.route("/create-account", methods=['POST'])
        @self.access.check_user(user_role="administrator", logger_module=self.logger_module)
        def create_account():
            info = request.json
            user_name = info.get('name')
            user_password = info.get('password')
            user_role = info.get('role')
            responce, code = self.accounts_manager.create_account(name=user_name, password=user_password, role=user_role)
            return jsonify(responce), code
            
        @app.route("/delete-account", methods=['POST'])
        @self.access.check_user(user_role="SuperAdmin", logger_module=self.logger_module)
        def delete_account():
            info = request.json
            user_name = info.get('name')
            responce, code = self.accounts_manager.delete_account(name=user_name)
            return jsonify(responce), code
            
        # get account
        @app.route("/get-accounts", methods=['POST'])
        @self.access.check_user(user_role="SuperAdmin", logger_module=self.logger_module)
        def get_accounts():
            responce, code = self.accounts_manager.get_accounts()
            return jsonify(responce), code
            
        # get role account
        @app.route("/get-account-data", methods=['POST'])
        def get_account_data():
            info = request.json
            user_name = info.get('name')
            password = info.get('password')
            server_token = info.get('server_token')
            responce, code = self.accounts_manager.get_account_data(
                    name=user_name,
                    password=password,
                    server_token=server_token
                )
            return jsonify(responce), code

        # change password
        @app.route("/change-password", methods=['POST'])
        @self.access.check_user(user_role="SuperAdmin", logger_module=self.logger_module)
        def change_password():
            info = request.json
            user_name = info.get('name')
            password = info.get('password')
            responce, code = self.accounts_manager.change_password(name=user_name, password=password)
            return jsonify(responce), code
            
        # get user token
        @app.route("/get-token", methods=['POST'])
        @self.access.check_user(user_role="SuperAdmin", logger_module=self.logger_module)
        def get_user_token():
            info = request.json
            user_name = info.get('name')
            password = info.get('password')
            responce, code = self.accounts_manager.get_user_token(name=user_name, password=password)
            return jsonify(responce), code

        # change user token
        @app.route("/change-token", methods=['POST'])
        @self.access.check_user(user_role="SuperAdmin", logger_module=self.logger_module)
        def change_token():
            info = request.json
            user_name = info.get('name')
            password = info.get('password')
            responce, code = self.accounts_manager.change_token(name=user_name, password=password)
            return jsonify(responce), code

        return app