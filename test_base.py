import base as b
from transaction import Transaction
from authentication import AuthenticationManager

# Wallet tests
def test_wallet_multiple_deposits():
    """
    Makes sure multiple deposits stack correctly
    """
    wallet = b.Wallet()
    wallet.deposit(5)
    wallet.deposit(15)
    assert wallet.get_balance() == 20

def test_wallet_withdraw_happy_path():
    """
    Tests withdrawing money when there are enough funds
    """
    wallet = b.Wallet()
    wallet.deposit(20)
    wallet.withdraw(5)
    assert wallet.get_balance() == 15

def test_wallet_withdraw_insufficient_funds():
    """
    Edge case - withdrawing more than balance should fail safely
    """
    wallet = b.Wallet()
    wallet.withdraw(10)
    assert wallet.get_balance() == 0

def test_wallet_reset_clears_balance_and_history():
    """
    Tests that reset_wallet properly clears everything
    """
    wallet = b.Wallet()
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
    assert t.get_amount() == 25.0
    assert t.get_type() == "deposit"

def test_transaction_to_dict():
    """
    Makes sure transaction converts to dictionary correctly
    """
    t = Transaction(10, "withdrawal")
    data = t.to_dict()

    assert data["amount"] == 10.0
    assert data["type"] == "withdrawal"
    assert "timestamp" in data

def test_transaction_from_dict():
    """
    Tests recreating a transaction from saved data
    """
    t = Transaction(30, "deposit")
    data = t.to_dict()

    new_t = Transaction.from_dict(data)
    assert new_t.get_amount() == 30.0
    assert new_t.get_type() == "deposit"

# Autethication manager tests
def test_create_user_happy_path():
    """
    Test that creates a new user successfully
    """
    auth = AuthenticationManager()
    auth.create_user("rixa", "password123")

    assert auth.user_exists("rixa") is True

def test_create_duplicate_user_raises_error():
    """
    Edge case - creating a user that already exists
    """
    auth = AuthenticationManager()
    auth.create_user("rixa", "password123")

    try:
        auth.create_user("rixa", "password123")
        assert False  
    except ValueError:
        assert True

def test_login_wrong_username_returns_none():
    """
    Edge case - logging in with a username that doesn't exist
    """
    auth = AuthenticationManager()
    result = auth.login("ghost", "password")
    assert result is None

def test_password_hashing_and_verification():
    """
    makes sure password hashing and verification works
    """
    auth = AuthenticationManager()
    hashed = auth.hash_password("secret")

    assert auth.verify_password("secret", hashed) is True
    assert auth.verify_password("wrong", hashed) is False

def test_remove_user():
    """
    test that remove a user from the system
    """
    auth = AuthenticationManager()
    auth.create_user("nahomi", "password123")

    removed = auth.remove_user("nahomi")
    assert removed is not None
    assert auth.user_exists("nahomi") is False
