import json
import pytest
from base import AuthenticationManager

@pytest.fixture
def auth_manager():
    return AuthenticationManager()

def test_initialize(auth_manager):
    assert auth_manager.users == {}
    
def test_create_user(auth_manager):
    auth_manager.create_user("testuser", "password123")
    assert auth_manager.user_exists("testuser")
    with pytest.raises(ValueError):
        auth_manager.create_user("testuser", "newpassword")

def test_create_user_hashes_password(auth_manager):
    auth_manager.create_user("testuser", "password123")
    stored_hash = auth_manager.users["testuser"]
    assert stored_hash != "password123"
    assert auth_manager.verify_password("password123", stored_hash)
    
def test_login_sucess(auth_manager):
    auth_manager.create_user("testuser", "password123")
    user = auth_manager.login("testuser", "password123")
    assert user is not None
    
#more to be added here

        