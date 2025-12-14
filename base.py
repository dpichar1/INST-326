#this file is empty for now
#name is subject to change
from datetime import datetime

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
      #Need to add transaction
      """
      transaction = transaction(amount, "deposit", self.user, self.user) 
      transaction_history.append(transaction)
      """
      
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
      #Need to add transaction
      """
      transaction = transaction(amount, "deposit", self.user, self.user) 
      add_transactions(transaction)
      """
      
  def transfer_to(self, amount:float, other_user):
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
      if not isinstance(other_user, Wallet):
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
      Wallet.deposit(amount)
      #Need to add transaction
      """
      transaction = transaction(amount, "deposit", other_user, self.user) 
      add_transactions(transaction)
      """
  def add_transactions(self, transaction):
    """
    Appends a transaction to the transaction history list to keep a record 
    
    Args:
      transaction(transaction):  the transaction being done
    """
    "transaction_history.append(transaction)"
    
  def get_transaction_history(self):
    """
    Returns the list of transaction of the user to see their history of deposit, withdrawals and transfers 
    
    Return:
      list[transaction]: all the transactions done in the wallet
    """
    "return transaction_history"
    
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
    #Need to transaction
    "print(f'Your last five transactions')"
    "reverse_transaction_history = traction_history[::-1]"
    """
    print(f'Your last five transactions')
    reverse_transaction_history = traction_history[::-1]
    for i in range(5):
      print(reverse_transaction_history[i])
    """
    


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

