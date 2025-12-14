import hashlib
import json

class AuthenticationManager:
    '''AuthenticationManager class handles creating accouns and
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
    
#this file is empty for now
#name is subject to change

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
      transaction = Transaction(amount, "withdrawal", self._username , None) 
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
      other_user.deposit(amount)
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
    print(f'Your last five transactions')
    reverse_transaction_history = self.transaction_history[::-1]
    for i in range(min(len(reverse_transaction_history), 5)):
      reverse_transaction_history[i].display()
 
