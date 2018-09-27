""" Defines modules for the app """
import os
import psycopg2
import psycopg2.extras
from pprint import pprint
from environs import Env

# import urlparse
# 
# CONN = psycopg2.connect(DATABASE_URL, sslmode='require')

class DatabaseConnection:
    """ handles database connections. """
    
    def __init__(self):
        """ initialise connection to db. """
        try:
            env = Env()
            env.read_env()

            DATABASE_NAME = env.str("DATABASE_NAME")
            DATABASE_USER = env.str("DATABASE_USER")
            DATABASE_PASSWORD = env.str("DATABASE_PASSWORD")
            DATABASE_HOST = env.str("DATABASE_HOST")
            DATABASE_PORT = env.str("DATABASE_PORT")

            self.connection_variables = 'dbname='+ DATABASE_NAME+' user='+ DATABASE_USER+'  password='+ DATABASE_PASSWORD+'  host='+ DATABASE_HOST+'  port='+ DATABASE_PORT
            self.connection = psycopg2.connect(self.connection_variables)
            
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
            create_command = "CREATE TABLE IF NOT EXISTS users(id serial PRIMARY KEY, email varchar, password varchar)"
            self.cursor.execute(create_command)
        except AttributeError:
            print("Error creating table")
        return "table created"

    def create_orders_table(self):
        """ create table to store orders. """
        try:
            create_command = "CREATE TABLE IF NOT EXISTS orders(id serial PRIMARY KEY, item varchar, quantity integer, user_id integer)"
            self.cursor.execute(create_command)
        except AttributeError:
            print("Error creating table")
        return "table created"

