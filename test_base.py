import pytest
from base import Wallet
from base import Transaction
from base import AuthenticationManager

# Wallet tests
def test_wallet_multiple_deposits():
    """
    Makes sure multiple deposits stack correctly
    """
    wallet = Wallet()
    wallet.deposit(5)
    wallet.deposit(15)
    assert wallet.get_balance() == 20

def test_wallet_withdraw_happy_path():
    """
    Tests withdrawing money when there are enough funds
    """
    wallet = Wallet()
    wallet.deposit(20)
    wallet.withdraw(5)
    assert wallet.get_balance() == 15

def test_wallet_withdraw_insufficient_funds():
    """
    Edge case - withdrawing more than balance should fail safely
    """
    wallet = Wallet()
    wallet.withdraw(10)
    assert wallet.get_balance() == 0

def test_wallet_reset_clears_balance_and_history():
    """
    Tests that reset_wallet properly clears everything
    """
    wallet = Wallet()
    wallet.deposit(50)
    wallet.reset_wallet()
    assert wallet.get_balance() == 0
    assert wallet.transaction_history == []

# Transaction tests
def test_transaction_creation():
    """
    Tests that a Transaction object is created correctly
    """
    t = Transaction(25, "deposit")
    assert t.amount == 25.0
    assert t.transaction_type == "deposit"

# Authentication manager tests
@pytest.fixture
def auth_manager():
    return AuthenticationManager()

def test_login_wrong_username_returns_none():
    """
    Edge case - logging in with a username that doesn't exist
    """
    auth = AuthenticationManager()
    result = auth.login("ghost", "password")
    assert result is None

def test_create_user_hashes_password(auth_manager):
    """
    makes sure password hashing and verification works
    """
    auth_manager.create_user("testuser", "password123")
    stored_hash = auth_manager.users["testuser"]
    assert stored_hash._hashed_password != "password123"
    assert auth_manager.verify_password("password123", stored_hash._hashed_password)

def test_create_user_duplicate_raises_error(auth_manager):
    """
    Edge case - creating a user that already exists
    """
    auth_manager.create_user("testuser", "password123")
    with pytest.raises(ValueError):
        auth_manager.create_user("testuser", "newpassword")
        
def test_user_exists(auth_manager):
    """
    Test that creates a new user successfully
    """
    auth_manager.create_user("testuser", "password123")
    assert auth_manager.user_exists("testuser") is True
    assert auth_manager.user_exists("someoneelse") is False

def test_verify_hash(auth_manager):
    """
    Test to see if a password hash passwords are working
    """
    hashed = auth_manager.hash_password("password123")
    assert auth_manager.login("testuser", "something") is None
    assert auth_manager.login("testuser", "else") is None

   
def test_login_success(auth_manager):
    """
    Test to see if a user logged in successfully 
    """
    auth_manager.create_user("testuser", "password123")
    assert auth_manager.login("testuser", "password123") is auth_manager.users.get("testuser")
    
    
def test_remove_user(auth_manager):
    """
    test that remove a user from the system
    """
    auth_manager.create_user("someone", "pass")
    assert auth_manager.remove_user("someone").get_username() is not None
    assert auth_manager.user_exists("someone") is False
    assert auth_manager.remove_user("someone") is None
    
def test_save_and_load_users():
    """
    test to see if loading a user are the same as its saved user 
    """
    auth1 = AuthenticationManager()
    auth1.create_user("user1", "pass")
    auth1.create_user("user2", "word")
    
    path = "users.json"
    auth1.save_users(path)
    
    auth2 = AuthenticationManager()
    auth2.load_users(path)
    
    assert auth2.users.get("user1")._hash_password == auth1.users.get("user1")._hash_password

def test_load_users_missing_file_starts_empty(tmp_path):
    """
    Edge case - attempting to load a user form a missing jason file 
    """
    auth = AuthenticationManager()
    auth.load_users(tmp_path / "nonexistent.json")
    assert auth.users == {}