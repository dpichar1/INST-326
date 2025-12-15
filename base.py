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
        
        # password verification
        if user.verify_password(password):
            return user

    def hash_password(self, password):
        """Hashes the given password using SHA-256."""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()
        
    def verify_password(self, password, hashed):
        """Verifies that the given password matches the hashed password."""
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
        
        self.users = {username: User.from_dict(user_data) for username, user_data in raw_data.items()}        
        
    def remove_user(self, username):
        """Removes a user by username, returning true if removed or false if not found."""
        return self.users.pop(username, None)
      
    def __eq__(self, other: AuthenticationManager):
        if not isinstance(other, AuthenticationManager):
          return NotImplemented
        return self.users == other.users

# User class
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
        self._wallet = Wallet()

    # Username handling
    def set_username(self, name: str) -> None:
        """Updates username (display name)"""
        self._username = name

    def get_username(self) -> str:
        """Returns username."""
        return self._username

    # password handling
    def set_password(self, password: str) -> None:
        """
        Hashes and updates password
        Simple SHA-256 hash
        """
        self._hashed_password = self._hash_password(password)

    def verify_password(self, password: str) -> bool:
        """Compares entered password with stored hash (login credential check)."""
        return self._hash_password(password) == self._hashed_password

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    #class wallet 
    def get_wallet(self):
        """Returns the wallet object."""
        return self._wallet


    # Methods for saving or loading users
    def to_dict(self):
        """Converts the User object into a dictionary for JSON storage."""
        return {
            "username": self._username,
            "hashed_password": self._hashed_password,
            "wallet": {
                "balance": self._wallet.get_balance(),
                "transaction_history": [
                    {
                        "amount": t.amount,
                        "transaction_type": t.transaction_type,
                        "from_user": t.from_user,
                        "to_user": t.to_user,
                        "timestamp": t.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    for t in self._wallet.get_transaction_history()
                ]
            }
        }
    def __eq__(self, other:User):
        if not isinstance(other, User):
          return NotImplemented
        return self._username == other._username and self._hashed_password == other._hashed_password and self._wallet == other._wallet

    @staticmethod
    def from_dict(data):
        """Creates a user object from a dictionary which is used for loading JSON)"""
        user = User(data["username"], data["hashed_password"])
        wallet_data = data.get("wallet", {})
        user._wallet.balance = wallet_data.get("balance", 0.0)

        for t_data in wallet_data.get("transaction_history", []):
            t = Transaction(
                amount=t_data["amount"],
                transaction_type=t_data["transaction_type"],
                from_user=t_data.get("from_user"),
                to_user=t_data.get("to_user")
            )
            t.timestamp = datetime.strptime(t_data["timestamp"], "%Y-%m-%d %H:%M:%S")
            user._wallet.add_transactions(t)

        return user


# Wallet class
class Wallet:
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
        if not isinstance(amount, (int,float)):
            print("Amount must be a float or int value")
            return
        if amount < 0:
            print("Amount can't be a negative value")
            return
        self.balance += amount
        transaction = Transaction(amount, "deposit")
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
        if not isinstance(amount, (int,float)):
            print("Amount must be a float or int value")
            return
        if amount < 0:
            print("Amount can't be a negative value")
            return
        if amount > self.balance:
            print("Insufficient funds")
            return
        self.balance -= amount
        transaction = Transaction(amount, "withdrawal")
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
        if not isinstance(amount,(int, float)):
            print("Amount must be a float or int value")
            return
        if not isinstance(other_user, User):
            print("Invalid user for transfer")
            return
        if amount < 0:
            print("Amount can't be negative")
            return
        if amount > self.balance:
            print("Insufficient funds")
            return
        self.withdraw(amount)
        other_user.get_wallet().deposit(amount)
        transaction = Transaction(amount, "transfer", to_user=other_user.get_username())
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
    def __eq__(self, other:Wallet):
        """
        Check if this wallet object is the same as another waller object 
        
        :param self: Description
        :param other: Description
        :type other: Wallet
        """
        if not isinstance(other, Wallet):
          return NotImplemented
        return self.balance == other.balance and self.transaction_history == other.transaction_history

# Transaction class
class Transaction:
    """ This class represents a single money related action in the wallet system such as a deposit, withdrawal
    or transfer. 
    """

    def __init__(self, amount, transaction_type, from_user=None, to_user=None):
        """ Creates a new transaction such as :
        - amount: how much money was involved
        -transaction_type: type of transaction such as deposit, withdrawal or transfer
        - from_user/to_user: users involved in the transaction
        """
        self.amount = float(amount)
        self.transaction_type = transaction_type
        self.from_user = from_user
        self.to_user = to_user
        #records when the trasaction happened 
        self.timestamp = datetime.now()

    def display(self):
        """
        Displays the transaction details in a readable format for the user's transaction history
        """
        time_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        if self.transaction_type == "deposit":
            print(f"[{time_str}] Deposit of ${self.amount:.2f}")
        elif self.transaction_type == "withdrawal":
            print(f"[{time_str}] Withdrawal of ${self.amount:.2f}")
        elif self.transaction_type == "transfer":
            print(f"[{time_str}] Transfer of ${self.amount:.2f} to {self.to_user}")
        else:
            print(f"[{time_str}] ${self.amount:.2f} - {self.transaction_type}")

#runnable main that handles user log in or account creation, then provides a menu to manage wallet actions
if __name__ == "__main__":
    
    #create the authentication manages and load saved users, if theres any saved
    auth = AuthenticationManager()
    auth.load_users("users.json")

    #app welcome message
    print("Welcome to the Wallet App")
    print("-------------------------")
    
    #login or account creation loop, it keeps runing until the user successfully logs in or creates an account
    while True:
        choice = input("Do you have an account? (yes/no): ").strip().lower()
        
        if choice == "yes":
            #for existing user log in
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            login_user = auth.login(username, password)

            if login_user:
                print(f"Welcome back, {login_user.get_username()}!")
                break
            else:
                print("Login failed. Please check your username and password.")
        
        elif choice == "no":
            #new user account creation 
            username = input("Create a username: ").strip()

            #keeps asking for a password until the user enters something valid
            while True:
                password = input("Create a password: ").strip()
                if password:
                    break
                print("Invalid password. Must enter a password.")

            #Checks if the the username already exists, otherwise creates the new user and log them in
            if auth.user_exists(username):
                print("That username already exists. Try logging in instead.")
            else:
                login_user = auth.create_user(username, password)
                print(f"Account created successfully. Welcome, {login_user.get_username()}!")
                break  
        #handles invalid input 
        else:
            print("Please type 'yes' or 'no'.")

    #gets the wallet for the logged in user
    wallet = login_user.get_wallet()

    #main wallet menu loop
    while True:
        print("\n1. Deposit\n2. Withdraw\n3. Transfer\n4. View balance\n5. Last Transactions\n6. Exit")
        choice = input("Enter choice: ")

        # Choice 1: deposit money into wallet 
        if choice == "1":
            try:
                amt = float(input("Enter amount to deposit: "))
                wallet.deposit(amt)
            except ValueError:
                print("Invalid amount. Please enter a number.")
        #chouce 2: Withdraw money from wallet
        elif choice == "2":
            try:
                amt = float(input("Enter amount to withdraw: "))
                wallet.withdraw(amt)
            except ValueError:
                print("Invalid amount. Please enter a number.")
        #Choice 3: transfer money to another user, it also prevents transfering to yourself and checks if the 
        #receiving user exits 
        elif choice == "3":
            try:
                amt = float(input("Enter amount to transfer: "))
                to_username = input("Username to transfer to: ")
                if to_username == login_user.get_username():
                    print("Cannot transfer to yourself.")
                    continue
                if not auth.user_exists(to_username):
                    print(f"User '{to_username}' does not exist. Creating new account for them.")
                    new_user = auth.create_user(to_username, "default123")
                else:
                    new_user = auth.users[to_username]
                wallet.transfer_to(amt, new_user)
            except ValueError:
                print("Invalid amount. Please enter a number.")

        #Choice 4: displats current wallet balance
        elif choice == "4":
            print(f"Current balance: ${wallet.get_balance():.2f}")
        
        #choice 5: shows recent transaction history
        elif choice == "5":
            wallet.summary()
        #choice 6: saves users before exiting the program 
        elif choice == "6":
            auth.save_users("users.json")
            print("Goodbye!")
            break
        else:
            #handles invalid menu input
            print("Invalid option. Try again.")


