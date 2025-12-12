#this file is empty for now
#name is subject to change


class wallet:
  """
  stores the current balance of the user and conducts transactions along holding the users transaction history 
  
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
    
    None
    
  def get_balance(self):
    """
    Returns the current balance back to the user show how much money the user holds 
    
    Returns:
      float: the current balance 
    """

    None
  def deposit(self, amount:float):
    """
    Adds money into the balance and creates and transaction object to add into the transaction history
    
    Args:
      amount(float):  the amount of money to deposit
    
    Raises:
      valueError: if the amount is a negative value
    """
  
    None
  def withdraw(self, amount:float):
    """
    Subtracts money from the balance if there is enough and creates and traction object and adds to the transaction history 
    
    Args:
      amount(float):  the amount of money to withdraw
      
    Raises:
      valueError: if the amount is a negative value or when there is insufficient funds to withdraw
    """
  
    None
  def transfer_to(self,amount:float, other_wallet:wallet  ):
    """
    Subtracts money from the balance if there is enough and creates and traction object and adds to the transaction history 
    
    Args:
      amount(float):  the amount of money to transfer
      other_wallet(wallet): The other user wallet to transfer to 
      
    Raises:
      valueError: if the amount is a negative value or when there is insufficient funds to transfer 
    """
    None
  def add_transactions(self, transaction):
    """
    Appends a transaction to the transaction history list to keep a record 
    
    Args:
      transaction(transaction):  the transaction being done
    """
    None
  def get_transaction_history(self):
    """
    Returns the list of transaction of the user to see their history of deposit, withdrawals and transfers 
    
    Return:
      list[transaction]: all the transactions done in the wallet
    """
    
    None
  def reset_wallet():
    """
    reset the wallet setting back the balance back to 0 and clearing the transaction history list
    """
    
    None
  def summary():
    """
    Prints out the current balance total and the last five transactions 
    """
