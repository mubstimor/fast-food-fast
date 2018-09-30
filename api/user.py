""" Class to manage CRUD operations on user objects"""
from api.database import DatabaseConnection
from werkzeug.security import generate_password_hash, check_password_hash
from pprint import pprint

class User(object):
    """ docstring for User. """
    def __init__(self):
        """ define connections to food items table. """
        self.db = DatabaseConnection()
        self.db.create_users_table()

    def create_user(self, user_data):
        """ add user to users table"""
        user = user_data
        user['name'] = str(user_data['name'])
        user['email'] = str(user_data['email'])
        user['gender'] = str(user_data['gender'])
        user['password'] = generate_password_hash(str(user_data['password']))
        if not self.check_if_user_exists(user['email']):
            self.db.cursor.execute("INSERT INTO users(name, email, password, gender) \
            VALUES('"+ user['name'] + "','"+ user['email'] +"', '"+user['password']+"', '"+user['gender']+"') RETURNING id")
            user_id = self.db.cursor.fetchone()[0]
            user['user_type'] = 'Customer'
            user['id'] = user_id
            return user
        else:
            return "Unable to create user"

    def check_if_user_exists(self, email):
        """ retrieve item with similar email"""
        try:
            self.db.cursor.execute("SELECT * FROM users where email='"+email+"'")
        except TypeError as e:
            print(e)
        rows_found = self.db.cursor.rowcount
        if rows_found > 0:
            return True
        else:
            return False

    def fetch_all_users(self):
        """ retrieve all users from db """
        try:
            self.db.cursor.execute("SELECT * FROM users")
        except TypeError as e:
            print(e)
        useritems = self.db.cursor.fetchall()
        users = []
        for item in useritems:
            user = {"id": item['id'], "email": item['email']}
            users.append(user)
        return users

    def get_user(self, user_id):
        """ retrieve user with given id"""
        try:
            self.db.cursor.execute("SELECT * FROM users where id='"+str(user_id)+"'")
        except TypeError as e:
            print(e)
        user_item = self.db.cursor.fetchone()
        rows_found = self.db.cursor.rowcount
        if rows_found > 0:
            user = {"id": user_item['id'], "email": user_item['email']}
            return user
        else:
            return "not found"

    def login(self, user_data):
        """ check user login """
        user = user_data
        user['email'] = str(user_data['email'])
        user['password'] = generate_password_hash(str(user_data['password']))
        try:
            self.db.cursor.execute("SELECT * FROM users where email='"+user['email']+"' AND password='"+user['password']+"'")
            # pprint("SELECT * FROM users where email='"+user['email']+"' AND password='"+user['password']+"'")
        except TypeError as e:
            print(e)
        rows_found = self.db.cursor.rowcount
        if rows_found > 0:
            return True
        else:
            return False
        
