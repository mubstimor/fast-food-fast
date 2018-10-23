""" Class to manage CRUD operations on user objects"""
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import psycopg2.extras
from api.db.database import DatabaseConnection

class User(object):
    """ docstring for User. """
    def __init__(self):
        self._db = DatabaseConnection()
        self.connection = None
        self.cursor = None

    def create_user(self, user_data):
        """ add user to users table"""
        self.connection = self._db.connect_db()
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        user = user_data
        user['name'] = str(user_data['name'])
        user['email'] = str(user_data['email'])
        user['gender'] = str(user_data['gender'])
        user['password'] = generate_password_hash(str(user_data['password']))
        user['user_type'] = str(user_data['user_type'])
        if not user['user_type']:
            user['user_type'] = 'Customer'
        self.cursor.execute("INSERT INTO users(name, email, password, \
                            gender, user_type) \
                            VALUES('"+ user['name'] + "','"+ user['email']
                            +"', '" + user['password']+"', '"+ \
                            user['gender']+"','"+
                            user['user_type']+"') RETURNING id")
        user_id = self.cursor.fetchone()[0]
        del user['password']
        user['user_type'] = 'Customer'
        user['id'] = user_id
        self.connection.close()
        return user

    def check_if_user_exists(self, email):
        """ retrieve item with similar email"""
        self.connection = self._db.connect_db()
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        self.cursor.execute("SELECT * FROM users where email='"+email+"'")
        rows_found = self.cursor.rowcount
        self.connection.close()
        if rows_found > 0:
            return True

    def authenticate(self, user_data):
        """ check user login """
        self.connection = self._db.connect_db()
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        user = user_data
        user['email'] = str(user_data['email'])
        user['password'] = str(user_data['password'])
        self.cursor.execute(
            "SELECT * FROM users where email='"+user['email']+"'")
        userdata = self.cursor.fetchone()
        self.connection.close()
        login_status = check_password_hash(userdata['password'],
                                           user['password'])
        if login_status:
            user = {"id": userdata['id'], "email": userdata['email'],
                    "role": userdata['user_type']}
            return user
