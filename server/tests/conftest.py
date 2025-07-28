import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.config import client, TestData

# def pytest_sessionfinish(session, exitstatus):
#     # used service for checking 
#     json = {
#         "id": TestData.kinematic_name,
#         "token": TestData.super_admin_token
#     }
#     client.post('/api/delete-kinematic', json=json)