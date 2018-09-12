""" Class to manage CRUD operations on user objects"""
from werkzeug.security import generate_password_hash, check_password_hash

class User(object):
    """ docstring for User. """
    def __init__(self):
        """ define attributes for user. """
        self.users = []

    def create_user(self, user_data):
        """ add user to users list """
        user = user_data
        user['id'] = len(self.users) + 1
        user['user_type'] = 'customer'
        user['password'] = generate_password_hash(user_data['password'])
        self.users.append(user)
        return user

    def fetch_all_users(self):
        """ retrieve all users from list but exclude passwords """
        temp_users = []
        for user in self.users:
            if 'password' in user:
                del user['password']
            temp_users.append(user)
        return temp_users

    def get_user(self, user_id):
        """ retrieve user with given id & exclude password. """
        user = [user for user in self.users if user['id'] == user_id]
        if 'password' in user:
            del user['password']
        return user

    def login(self, user_data):
        """ check user login """
        user = [user for user in self.users if user['email'] == user_data['email']]
        if user and check_password_hash(user[0]['password'], user_data['password']):
            return True

# Unused - not a priority at the moment
    def update_user(self, user_id, user_data):
        """ update user details. """
        user = self.get_user(user_id)
        user[0]['email'] = user_data['email']
        return user
