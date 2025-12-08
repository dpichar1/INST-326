class AuthenticationManager:
    '''AuthenticationManager class handles creating accouns and
    logging users in. Stores all the users and hashes passwords.
    When someone logs in successfully, it gives you an User object.'''
    
    def __init__(self):
        pass
    def create_user(self, username, password):
        pass
    def login(username, password):
        pass
    def hash_password(self, password):
        pass
    def verify_password(self, password, hashed):
        pass
    def verify_hash(self, password, hashed):
        pass
    def user_exists(self, username):
        pass
    def save_users(self, filepath):
        pass
    def load_users(self, filepath):
        pass
    def remove_user(self, username):
        pass