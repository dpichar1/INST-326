from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, Optional
import hashlib
import json

class AuthenticationManager:
    '''AuthenticationManager class handles creating accounts and
    logging users in. Stores all the users and hashes passwords.
    When someone logs in successfully, it gives you an User object.'''
    
    def __init__(self):
        """
        Initializes the AuthenticationManager with an empty user store (dictionary).
        """
        self.users = {}
        
        
    def create_user(self, username, password):
        """Creates a new user with the given username and password.
        Raises ValueError if the user already exists. Then stores the
        user with the hashed password. At the end, returns the User object."""
        if self.user_exists(username):
            raise ValueError("User already exists.")
        
        hashed_password = self.hash_password(password)
        user = User(username=username, hashed_password=hashed_password)
        self.users[username] = user
        return user

    def login(self, username, password):
        """Logs in a user with their username and password.
        returns the User object if successful, None if it wasn't."""
        user = self.users.get(username)
        if user is None:
            return None
        
        #Password verification
        if user.verify_password(password):
            return user

    def hash_password(self, password):
        """Hashes the given password using SHA-256 (via hashlib)."""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()
        
    def verify_password(self, password, hashed):
        """Verifies that the given password matchesn the hashed password."""
        return self.hash_password(password) == hashed

    def verify_hash(self, password, hashed):
        """Compares a password to a hashed password and returns True if it's a match."""
        return self.hash_password(password) == hashed
    
    def user_exists(self, username):
        """Checks if a user with the given username exists. Returns True/False."""
        return username in self.users
    
    def save_users(self, filepath):
        """Saves the current users to a JSON file (via JSON library).
           Where User.to_dict() is used to convert User object to a dictionary.
        """
        data = {username: user.to_dict() for username, user in self.users.items()}
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            
    def load_users(self, filepath):
        """Loads users from a JSON file (via JSON library). 
           Where User.from_dict() is used to convert dictionary to User object.
           FileNotFoundError is there to handle missing files with an empty user store as a result.
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
        except FileNotFoundError:
            self.users = {}
            return
        
        users = {}
        for username, user_data in raw_data.items():
            user = User.from_dict(user_data)
            users[user.get_username()] = user
        self.users = users        
        
            
    def remove_user(self, username):
        """Removes a user by username, returning true if removed or false if not found."""
        return self.users.pop(username, None)
    
class User:
    """
    User class:
    - Stores username + hashed_password
    - Creates/owns one wallet
    """

    def __init__(self, username: str, hashed_password: str):
        self._username: str = username
        self._hashed_password: str = hashed_password

        # Creates a wallet (import here to avoid circular imports)
        # wallet.py should exist in your project
        self._wallet = Wallet()

    # -------------------------
    # Username
    # -------------------------
    def set_username(self, name: str) -> None:
        """Updates username (display name)."""
        self._username = name

    def get_username(self) -> str:
        """Returns username."""
        return self._username

    # -------------------------
    # Password
    # -------------------------
    def set_password(self, password: str) -> None:
        """
        Hashes and updates password.
        (Simple SHA-256 hash for a class project.)
        """
        self._hashed_password = self._hash_password(password)

    def verify_password(self, password: str) -> bool:
        """Compares entered password with stored hash (login credential check)."""
        return self._hash_password(password) == self._hashed_password

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    # -------------------------
    # Wallet
    # -------------------------
    def get_wallet(self):
        """Returns the wallet object."""
        return self._wallet

    # -------------------------
    # Save / Load
    # -------------------------
    def to_dict(self) -> Dict[str, Any]:
        """Converts user data to dictionary (for saving)."""
        data: Dict[str, Any] = {
            "username": self._username,
            "hashed_password": self._hashed_password,
        }

        # Save wallet if it supports to_dict()
        if hasattr(self._wallet, "to_dict"):
            data["wallet"] = self._wallet.to_dict()

        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        """Restores user from saved dictionary."""
        user = cls(
            username=data.get("username", ""),
            hashed_password=data.get("hashed_password", ""),
        )

        # Restore wallet if present and Wallet supports from_dict()
        wallet_data: Optional[Dict[str, Any]] = data.get("wallet")
        if wallet_data is not None:
            from wallet import Wallet
            if hasattr(Wallet, "from_dict"):
                user._wallet = Wallet.from_dict(wallet_data)

        return user

    # -------------------------
    # Debug
    # -------------------------
    def display_information(self) -> None:
        """Print basic user information (debug)."""
        print(f"User: {self._username}")
        if hasattr(self._wallet, "get_balance"):
            print(f"Balance: {self._wallet.get_balance()}")

class Wallet(User):
  """
  stores the current balance of the user and conducts transactions along with holding the users transaction history 
  
  Attributes:
    balance(int): an empty balance
    transaction_history(list): An empty list which will hold all the transaction that happens
    
  Methods:
    get_balance(): returns float value of the users current balance 
    deposit(amount:float): add money into wallet balance and creates an transaction object and adds it to transaction history list 
    withdraw(amount:float): subtracts money from the wallet balance and creates and transaction object and adds it to transaction history list 
    transfer_to(amount:float, other_wallet:wallet): Send money to another users wallet and create traction object and adds it to transaction history list 
    add_transaction(transaction:transaction) append a transaction to transaction history list
    get_transaction_history(): Returns back list of transaction object from the transaction history list
    reset_wallet(): set the current balance back to 0 and clears transaction history list 
    summary(): prints out the current user wallet balance and the last five transaction from transaction history list
  """
  def __init__(self):
    """
    Initializes an balance of 0 and creates an empty list for transaction history to be stored 
    
    Attributes:
      balance(float): the money the user is holding set to 0 at first: 
      transaction_history(list): empty list to hold all the transaction conducted 
    """
    self.balance = 0.00
    self.transaction_history = []
    
  def get_balance(self):
    """
    Returns the current balance back to the user show how much money the user holds 
    
    Returns:
      float: the current balance 
    """
    return self.balance
  
  def deposit(self, amount:float):
    """
    Adds money into the balance and creates and transaction object to add into the transaction history
    
    Args:
      amount(float):  the amount of money to deposit
    
    Raises:
      typeError: if amount is not a int or float value 
      valueError: if the amount is a negative value
    """
    try:
      if not isinstance(amount, (int,float)):
        raise TypeError()
      if amount < 0:
        raise ValueError()
    except TypeError:
      print("Amount must be a float or int value")
    except ValueError:
      print("Amount can't be a negative value")
    else:
      self.balance += amount
      transaction = Transaction(amount, "deposit", None , self.get_username) 
      self.add_transactions(transaction)
      
      
  def withdraw(self, amount:float):
    """
    Subtracts money from the balance if there is enough and creates and traction object and adds to the transaction history 
    
    Args:
      amount(float):  the amount of money to withdraw
      
    Raises:
      typeError: if amount is not a int or float value 
      valueError: if the amount is a negative value or when there is insufficient funds to withdraw
    """
    try:
      if not isinstance(amount, (int,float)):
        raise TypeError()
      if amount <0:
        raise ValueError("Amount can't be a negative value")
      if amount > self.balance:
        raise ValueError("insufficient funds")
    except TypeError:
      print("Amount must be a float or int value")
    except ValueError as e:
      print(e)
    else:
      self.balance -= amount
      transaction = Transaction(amount, "withdrawal", self.get_username , None) 
      self.add_transactions(transaction)
      
      
  def transfer_to(self, amount:float, other_user: User):
    """
    Subtracts money from the balance if there is enough and creates and traction object and adds to the transaction history 
    
    Args:
      amount(float):  the amount of money to transfer
      other_wallet(wallet): The other user wallet to transfer to 
      
    Raises:
      valueError: if the amount is a negative value or when there is insufficient funds to transfer 
    """
    try:
      if not isinstance(amount,(int, float)):
        raise TypeError("Amount must be a float or int value")
      if not isinstance(other_user, (User)):
        raise TypeError("other_wallet must be a wallet object")
      if amount <0:
        raise ValueError("Amount can't be a negative value")
      if amount > self.balance:
        raise ValueError("insufficient funds")
    except TypeError as e:
      print(e)
    except ValueError as e:
      print(e)
    else:
      self.withdraw(amount)
      other_user.get_wallet().deposit(amount)
      transaction = Transaction(amount, "transfer", other_user.get_username , self.get_username) 
      self.add_transactions(transaction)
      
  def add_transactions(self, transaction):
    """
    Appends a transaction to the transaction history list to keep a record 
    
    Args:
      transaction(transaction):  the transaction being done
    """
    self.transaction_history.append(transaction)
    
  def get_transaction_history(self):
    """
    Returns the list of transaction of the user to see their history of deposit, withdrawals and transfers 
    
    Return:
      list[transaction]: all the transactions done in the wallet
    """
    return self.transaction_history
    
  def reset_wallet(self):
    """
    reset the wallet setting back the balance back to 0 and clearing the transaction history list
    """
    self.balance = 0
    self.transaction_history = [] 
    
  def summary(self):
    """
    Prints out the current balance total and the last five transactions 
    """
    print(f'Your current balance: {self.balance:.2f}')
    if self.transaction_history:
      print(f'Your last five transactions')
      reverse_transaction_history = self.transaction_history[::-1]
      for i in range(min(len(reverse_transaction_history), 5)):
        reverse_transaction_history[i].display()
 
class Transaction:
    # This class represents one money action in the system
    # It does not touch balances at all, like a receipt that gets created after something happens

    def __init__(self, amount, transaction_type, from_user=None, to_user=None):
        # amount: how much money was involved in the transaction
        # transaction_type: "deposit", "withdrawal", or "transfer"
        # from_user: who sent the money (None for deposits)
        # to_user: who received the money (None for withdrawals)

        # Makes sure amount is always stored as a number
        self.amount = float(amount)

        # Stores the type of transaction so we know what kind of action happened
        self.transaction_type = transaction_type

        # Stores the users involved (can be None depending on the type)
        self.from_user = from_user
        self.to_user = to_user

        # Timestamp is created when the transaction happens
        # allows to see exactly when the action took place
        self.timestamp = datetime.now()

    # Returns the transaction amount
    # Used when displaying history or summaries
    def get_amount(self):
        return self.amount

    # Returns the type of transaction (deposit, withdrawal, transfer)
    def get_type(self):
        return self.transaction_type

    # Returns the sender of the money
    # Mainly used for transfers
    def get_from_user(self):
        return self.from_user

    # Returns the receiver of the money
    def get_to_user(self):
        return self.to_user

    # Returns the time the transaction happened
    def get_timestamp(self):
        return self.timestamp

    # Converts the transaction into a dictionary
    # Used when saving transaction history to a file
    def to_dict(self):
        return {
            "amount": self.amount,
            "type": self.transaction_type,
            "from_user": self.from_user,
            "to_user": self.to_user,
            # We convert the timestamp to a string so it can be saved properly
            "timestamp": self.timestamp.isoformat()
        }

    # Recreates a Transaction object from saved dictionary data
    # How transaction history is restored when the app starts again
    @staticmethod
    def from_dict(data):
        transaction = Transaction(
            data["amount"],
            data["type"],
            data.get("from_user"),
            data.get("to_user")
        )

        # Convert the timestamp string back into a datetime object
        transaction.timestamp = datetime.fromisoformat(data["timestamp"])
        return transaction

    # Prints a clean a readable version of the transaction
    # This is what users see when they check their transaction history
    def display(self):
        time_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")

        if self.transaction_type == "deposit":
            print(f"[{time_str}] Deposit of ${self.amount:.2f}")

        elif self.transaction_type == "withdrawal":
            print(f"[{time_str}] Withdrawal of ${self.amount:.2f}")

        elif self.transaction_type == "transfer":
            print(f"[{time_str}] Transfer of ${self.amount:.2f} "
                  f"from {self.from_user} to {self.to_user}")
        else:
            print(f"[{time_str}] ${self.amount:.2f} - {self.transaction_type}")

class User:
    """
    User class:
    - Stores username + hashed_password
    - Creates/owns one wallet
    """

    def __init__(self, username: str, hashed_password: str):
        self._username: str = username
        self._hashed_password: str = hashed_password

        # Creates a wallet (import here to avoid circular imports)
        from wallet import Wallet 
        self._wallet = Wallet()

    # -------------------------
    # Username
    # -------------------------
    def set_username(self, name: str) -> None:
        """Updates username (display name)."""
        self._username = name

    def get_username(self) -> str:
        """Returns username."""
        return self._username

    # -------------------------
    # Password
    # -------------------------
    def set_password(self, password: str) -> None:
        """
        Hashes and updates password.
        (Simple SHA-256 hash for a class project.)
        """
        self._hashed_password = self._hash_password(password)

    def verify_password(self, password: str) -> bool:
        """Compares entered password with stored hash (login credential check)."""
        return self._hash_password(password) == self._hashed_password

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    # -------------------------
    # Wallet
    # -------------------------
    def get_wallet(self):
        """Returns the wallet object."""
        return self._wallet

    # -------------------------
    # Save / Load
    # -------------------------
    def to_dict(self) -> Dict[str, Any]:
        """Converts user data to dictionary (for saving)."""
        data: Dict[str, Any] = {
            "username": self._username,
            "hashed_password": self._hashed_password,
        }

        # Save wallet if it supports to_dict()
        if hasattr(self._wallet, "to_dict"):
            data["wallet"] = self._wallet.to_dict()

        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        """Restores user from saved dictionary."""
        user = cls(
            username=data.get("username", ""),
            hashed_password=data.get("hashed_password", ""),
        )

        # Restore wallet if present and Wallet supports from_dict()
        wallet_data: Optional[Dict[str, Any]] = data.get("wallet")
        if wallet_data is not None:
            from wallet import Wallet
            if hasattr(Wallet, "from_dict"):
                user._wallet = Wallet.from_dict(wallet_data)

        return user

    # -------------------------
    # Debug
    # -------------------------
    def display_information(self) -> None:
        """Print basic user information (debug)."""
        print(f"User: {self._username}")
        if hasattr(self._wallet, "get_balance"):
            print(f"Balance: {self._wallet.get_balance()}")
            print(f"[{time_str}] ${self.amount:.2f} - {self.transaction_type}")
