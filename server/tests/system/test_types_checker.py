import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tests.config import client, TestData

def test_get_base_type_error(client):
    json = {
        "id": 5,
        "token": TestData.super_admin_token
    }
    response = client.post('/api/get-base', json=json)
    assert response.status_code == 400
    json = response.get_json()
    assert "data" not in json
    assert json["status"] == False