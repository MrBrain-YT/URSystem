from flask import Blueprint, request, jsonify

from services.accounts_manager import AccountManager
from api.access_checker import Access

class AccountManagerAPI:
    access = Access()
    
    def __init__(self, users:dict=None) -> None:
        self.logger_module = "URAccounts"
        if users is not None:
            self.accounts_manager = AccountManager(users)
        else:
            self.accounts_manager = AccountManager()
    
    def __call__(self) -> Blueprint:
        
        accounts_bp = Blueprint("accounts_api", __name__, url_prefix="/api")

        @accounts_bp.route("/create-account", methods=['POST'])
        @self.access.check_user(user_role="administrator", logger_module=self.logger_module)
        def create_account():
            info = request.json
            user_name = info.get('name')
            user_password = info.get('password')
            user_role = info.get('role')
            response, code = self.accounts_manager.create_account(name=user_name, password=user_password, role=user_role)
            return jsonify(response), code
            
        @accounts_bp.route("/delete-account", methods=['POST'])
        @self.access.check_user(user_role="SuperAdmin", logger_module=self.logger_module)
        def delete_account():
            info = request.json
            user_name = info.get('name')
            response, code = self.accounts_manager.delete_account(name=user_name)
            return jsonify(response), code
            
        # get accounts
        @accounts_bp.route("/get-accounts", methods=['POST'])
        @self.access.check_user(user_role="SuperAdmin", logger_module=self.logger_module)
        def get_accounts():
            response, code = self.accounts_manager.get_accounts()
            return jsonify(response), code
            
        # get role account
        @accounts_bp.route("/get-account-data", methods=['POST'])
        def get_account_data():
            info = request.json
            user_name = info.get('name')
            password = info.get('password')
            server_token = info.get('server_token')
            response, code = self.accounts_manager.get_account_data(
                    name=user_name,
                    password=password,
                    server_token=server_token
                )
            return jsonify(response), code

        # change password
        @accounts_bp.route("/change-password", methods=['POST'])
        @self.access.check_user(user_role="SuperAdmin", logger_module=self.logger_module)
        def change_password():
            info = request.json
            user_name = info.get('name')
            password = info.get('password')
            response, code = self.accounts_manager.change_password(name=user_name, password=password)
            return jsonify(response), code
            
        # get user token
        @accounts_bp.route("/get-token", methods=['POST'])
        @self.access.check_user(user_role="SuperAdmin", logger_module=self.logger_module)
        def get_user_token():
            info = request.json
            user_name = info.get('name')
            response, code = self.accounts_manager.get_user_token(name=user_name)
            return jsonify(response), code

        # change user token
        @accounts_bp.route("/change-token", methods=['POST'])
        @self.access.check_user(user_role="SuperAdmin", logger_module=self.logger_module)
        def change_token():
            info = request.json
            user_name = info.get('name')
            response, code = self.accounts_manager.change_token(name=user_name)
            return jsonify(response), code
        
        return accounts_bp