""" Defines modules for the app """
import os
import psycopg2
from pprint import pprint
import urlparse
# 
# CONN = psycopg2.connect(DATABASE_URL, sslmode='require')

class DatabaseConnection:
    """ handles database connections. """
    
    def __init__(self):
        """ initialise connection to db. """
        try:
            DATABASE_NAME = os.environ["DATABASE_NAME"]
            DATABASE_USER = os.environ["DATABASE_USER"]
            DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]
            DATABASE_HOST = os.environ["DATABASE_HOST"]
            DATABASE_PORT = os.environ["DATABASE_PORT"]


            DATABASE_URL = os.environ["DATABASE_URL"]
            url = urlparse.urlparse(DATABASE_URL)
            self.db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
            self.connection = psycopg2.connect(self.db)
            
            # self.connection_variables = 'dbname=fastfoodfast user=postgres password=pgadmin host=localhost port=5432'
            # self.connection_variables = 'dbname='+ DATABASE_NAME+' user='+ DATABASE_USER+'  password='+ DATABASE_PASSWORD+'  host='+ DATABASE_HOST+'  port='+ DATABASE_PORT
            # self.connection = psycopg2.connect(self.connection_variables)
            
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except Exception:
            pprint("Can't connect to database")
        
    def create_fooditem_table(self):
        """ create table to store menu. """
        try:
            # price integer NOT NULL
            create_command = "CREATE TABLE IF NOT EXISTS fooditems(id serial PRIMARY KEY, name varchar, category varchar, price varchar)"
            self.cursor.execute(create_command)
        except Exception:
            print("Error creating table")
        return "table created"

    def insert_fooditem(self):
        new_item = ("Chips", "Foods", '7000')
        insert_command = "INSERT INTO fooditems(name, category, price) VALUES('"+ new_item[0] + "', '" + new_item[1] + "', '"+ new_item[2] +"')"
        pprint(insert_command)
        self.cursor.execute(insert_command)

    def query_all(self):
        self.cursor.execute("SELECT * FROM fooditems")
        fooditems = self.cursor.fetchall()
        for item in fooditems:
            pprint("each item : {0}".format(item))

    def update_record(self):
        update_command = "UPDATE fooditems SET name='Fish', price=6000 WHERE id=1"
        self.cursor.execute(update_command)
