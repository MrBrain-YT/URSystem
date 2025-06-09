import pytest
import os
import sys

# Add project root to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from main import app
from configuration.server_token import reg_token
from databases.connection import users_table
from databases.database_manager import DBWorker

account_name = "TestName"
account_password = "12345"

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_create_account_success(client):
    # query = users_table.delete().where(users_table.columns.name == account_name)
    # DBWorker().send_query(query=query)
    json = {
        "name": account_name,
        "password": account_password,
        "role": "user",
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/create-account', json=json)
    print(response.get_json())
    assert response.status_code == 200
    json = response.get_json()
    assert "was created" in json["info"]
    assert json["status"] == True

def test_create_account_error_exist(client):
    json = {
        "name": account_name,
        "password": account_password,
        "role": "user",
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/create-account', json=json)
    json = response.get_json()
    assert response.status_code == 400
    assert json["info"] == "The account has already been created"
    assert json["status"] == False

# Additional functions





# ---------------------

def test_delete_account_success(client):
    json = {
        "name": account_name,
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/delete-account', json=json)
    json = response.get_json()
    assert response.status_code == 200
    assert "was deleted" in json["info"]
    assert json["status"] == True

def test_delete_account_error_not_found(client):
    json = {
        "name": account_name,
        "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb425"
    }
    response = client.post('/api/delete-account', json=json)
    json = response.get_json()
    assert response.status_code == 400
    assert json["info"] == "No such account exists"
    assert json["status"] == False