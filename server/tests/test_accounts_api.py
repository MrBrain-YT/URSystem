import pytest
import os
import sys

# Add project root to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from configuration.server_token import reg_token

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_account_data_success(client):
    # Example token for testing; replace with a valid test token if needed

    json = {
        "name": "SuperAdmin",
        "password": "12345",
        "server_token": reg_token
    }
    response = client.post('/api/get-account-data', json=json)
    assert response.status_code == 200
    data = response.get_json()
    assert "data" in data
    # Additional checks can be added here based on expected data structure
