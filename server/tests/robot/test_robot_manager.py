import pytest
import os
import sys

# Add project root to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from main import app

name_frame = "TestName"

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
