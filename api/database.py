""" Defines modules for the app """
import os
import psycopg2
import psycopg2.extras
from pprint import pprint
from environs import Env

# import urlparse
# 
# CONN = psycopg2.connect(DATABASE_URL, sslmode='require')
print(os.getenv('APP_SETTINGS'))

class DatabaseConnection:
    """ handles database connections. """
    
    def __init__(self):
        """ initialise connection to db. """
        try:
            env = Env()
            env.read_env()

            DATABASE_HOST = env.str("DATABASE_HOST")
            DATABASE_URL = env.str("DATABASE_URL")
            APP_SETTINGS = env.str("APP_SETTINGS")
            
            # if APP_SETTINGS== "TESTING" and DATABASE_HOST == "localhost":
            # # if DATABASE_HOST == "localhost:
            #     # self.connection = psycopg2.connect(DATABASE_URL)
            #     self.connection = psycopg2.connect(env.str("DATABASE_TEST_URL"))
            # else:
            #     self.connection = psycopg2.connect(DATABASE_URL, sslmode='require')
            if APP_SETTINGS== "TESTING":
                self.connection = psycopg2.connect(env.str("DATABASE_TEST_URL"))
            elif APP_SETTINGS== "DEVELOPMENT":
                self.connection = psycopg2.connect(env.str("DATABASE_URL"))
            else:
                self.connection = psycopg2.connect(DATABASE_URL, sslmode='require')
            
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except AttributeError as ae:
            pprint("Can't connect to database" + ae)
        
    def create_fooditem_table(self):
        """ create table to store menu. """
        try:
            create_command = "CREATE TABLE IF NOT EXISTS fooditems(id serial PRIMARY KEY, name varchar, category varchar, price integer NOT NULL)"
            self.cursor.execute(create_command)
        except AttributeError:
            print("Error creating table")
        return "table created"

    def create_users_table(self):
        """ create table to store users. """
        try:
            create_command = "CREATE TABLE IF NOT EXISTS users(id serial PRIMARY KEY, name varchar, email varchar, password varchar, gender varchar, user_type varchar DEFAULT 'Customer')"
            self.cursor.execute(create_command)
        except AttributeError:
            print("Error creating table")
        return "table created"

    def create_orders_table(self):
        """ create table to store orders. """
        try:
            create_command = "CREATE TABLE IF NOT EXISTS orders(id serial PRIMARY KEY, item varchar, quantity integer, status varchar, user_id integer)"
            self.cursor.execute(create_command)
        except AttributeError:
            print("Error creating table")
        return "table created"

    def create_all(self):
        """ create all tables. """
        self.create_fooditem_table()
        self.create_users_table()
        self.create_orders_table()

    def drop_all(self):
        """ delete all tables. """
        self.cursor.execute("DROP TABLE fooditems")
        self.cursor.execute("DROP TABLE users")
        self.cursor.execute("DROP TABLE orders")

