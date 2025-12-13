from datetime import datetime

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
        # This allows to see exactly when the action took place
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
    # This is used when saving transaction history to a file
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
    # This is how transaction history is restored when the app starts again
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

    # Prints a clean, readable version of the transaction
    # This is what users see when they check their transaction history
    def display(self):
        # Format the timestamp so it looks nice and readable
        time_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")

        if self.transaction_type == "deposit":
            print(f"[{time_str}] Deposit of ${self.amount:.2f}")

        elif self.transaction_type == "withdrawal":
            print(f"[{time_str}] Withdrawal of ${self.amount:.2f}")

        elif self.transaction_type == "transfer":
            print(f"[{time_str}] Transfer of ${self.amount:.2f} "
                  f"from {self.from_user} to {self.to_user}")

        else:
            # Fallback just in case a new transaction type gets added later
            print(f"[{time_str}] ${self.amount:.2f} - {self.transaction_type}")
