import hashlib
import json

class AuthenticationManager:
    '''AuthenticationManager class handles creating accouns and
    logging users in. Stores all the users and hashes passwords.
    When someone logs in successfully, it gives you an User object.'''
    
    def __init__(self):
        self.users = {}
        
        
    def create_user(self, username, password):
        if self.user_exists(username):
            raise ValueError("User already exists.")
        
        self.users[username] = self.hash_password(password)

    def login(self, username, password):
        if not self.user_exists(username):
            return None

        stored_hash  = self.users[username]

        if self.verify_hash(password, stored_hash):
            pass #return User(username) this is where you would return a User object.
        return None

    def hash_password(self, password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()
        
    def verify_password(self, password, hashed):
        return self.hash_password(password) == hashed

    def verify_hash(self, password, hashed):
        return self.hash_password(password) == hashed
    
    def user_exists(self, username):
        return username in self.users
    
    def save_users(self, filepath):
        with open(filepath, 'w', encoding="utf-8") as f:
            json.dump(self.users, f)
            
    def load_users(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                self.users = json.load(f)
        except FileNotFoundError:
            self.users = {} #in case no user file exists yet.
            
    def remove_user(self, username):
        return self.users.pop(username, None)
    