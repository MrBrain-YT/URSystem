import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from main import app
from configuration.server_token import reg_token

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
        

class TestData():
    super_admin_login = "SuperAdmin"
    super_admin_password = "12345"
    super_admin_token = "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    new_account_name = "TestName"
    new_account_password = "12345"
    new_account_role = "user"
    server_token = reg_token
    base_name = "TestName"
    tool_name = "TestName"
    frame_name = "TestName"
    robot_name = "First"
    robot_secret_code = "654123"
