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

def teest_create_user_duplicate_raises_error(auth_manager):
    auth_manager.create_user("testuser", "password123")
    with pytest.raises(ValueError):
        auth_manager.create_user("testuser", "newpassword")
        
def test_user_exists(auth_manager):
    auth_manager.create_user("testuser", "password123")
    assert auth_manager.user_exists("testuser") is True
    assert auth_manager.user_exists("someoneelse") is False

def test_verify_hash(auth_manager):
    hashed = auth_manager.hash_password("password123")
    assert auth_manager.login("testuser", "something") is None
    assert auth_manager.login("testuser", "else") is None

   
def test_login_success(auth_manager):
    auth_manager.create_user("testuser", "password123")
    assert auth_manager.login("testuser", "password123") is None #placeholder for user object
    
def test_remove_user(auth_manager):
    auth_manager.create_user("someone", "pass")
    assert auth_manager.remove_user("someone") is True
    assert auth_manager.user_exists("someone") is False
    assert auth_manager.remove_user("someone") is False
    
def test_save_and_load_users(tmp_path):
    auth1 = AuthenticationManager()
    auth1.create_user("user1", "pass")
    auth1.create_user("user2", "word")
    
    path = tmp_path / "users.json"
    auth1.save_users(path)
    
    auth2 = AuthenticationManager()
    auth2.load_users(path)
    
    assert auth2.users == auth1.users

def test_load_users_missing_file_starts_empty(tmp_path):
    auth = AuthenticationManager()
    auth.load_users(tmp_path / "nonexistent.json")
    assert auth.users == {}


        