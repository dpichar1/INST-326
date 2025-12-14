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
    