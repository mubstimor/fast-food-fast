""" Defines modules for the app """
import psycopg2
import psycopg2.extras
from pprint import pprint
from environs import Env
from psycopg2 import pool

class DatabaseConnection:
    """ handles database connections. """
    
    def __init__(self):
        """ initialise connection to db. """
        env = Env()
        env.read_env()
        self.DATABASE_URL = env.str("DATABASE_URL")
        self.DATABASE_TEST_URL = env.str("DATABASE_TEST_URL")
        self.APP_SETTINGS = env.str("APP_SETTINGS")
        self.DATABASE_HOST = env.str("DATABASE_HOST")
        self.DATABASE_USER = env.str("DATABASE_USER")
        self.DATABASE_PASSWORD = env.str("DATABASE_PASSWORD")
        self.DATABASE_NAME = env.str("DATABASE_NAME")
        self.DATABASE_TEST = env.str("DATABASE_TEST")
        self.DATABASE_PORT = env.str("DATABASE_PORT")
        self.DATABASE_TEST_USER = env.str("DATABASE_TEST_USER")
        self.DATABASE_TEST_PASSWORD = env.str("DATABASE_TEST_PASSWORD")
        self.DATABASE_TEST_HOST = env.str("DATABASE_TEST_HOST")

        # try:            
        #     if self.APP_SETTINGS== "TESTING":
        #         self.connection = psycopg2.connect(self.DATABASE_TEST_URL)
        #     elif self.APP_SETTINGS== "DEVELOPMENT":
        #         self.connection = psycopg2.connect(self.DATABASE_URL)
        #     elif self.APP_SETTINGS== "PRODUCTION":
        #         self.connection = psycopg2.connect(self.DATABASE_URL, sslmode='require')
                 
        #     self.connection.autocommit = True
        #     self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # except AttributeError as ae:
        #     pprint("Can't connect to database" + ae)

    def connect_db(self):
        try:            
            if self.APP_SETTINGS== "TESTING":
                self.connection = psycopg2.connect(self.DATABASE_TEST_URL)
            elif self.APP_SETTINGS== "DEVELOPMENT":
                self.connection = psycopg2.connect(self.DATABASE_URL)
            elif self.APP_SETTINGS== "PRODUCTION":
                self.connection = psycopg2.connect(self.DATABASE_URL, sslmode='require')
                 
            self.connection.autocommit = True
            # self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            return self.connection
        except AttributeError as ae:
            pprint("Can't connect to database" + ae)
        
        # try:
        #     if self.APP_SETTINGS== "TESTING":
        #         self.pg_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user=self.DATABASE_TEST_USER, password=self.DATABASE_TEST_PASSWORD,
        #                                                     host=self.DATABASE_TEST_HOST, port=self.DATABASE_PORT, database=self.DATABASE_TEST)
        #     elif self.APP_SETTINGS== "DEVELOPMENT":
        #         self.pg_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD,
        #                                                     host=self.DATABASE_HOST, port=self.DATABASE_PORT, database=self.DATABASE_NAME)
        #     elif self.APP_SETTINGS== "PRODUCTION":
        #         self.pg_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD,
        #                                                     host=self.DATABASE_HOST, port=self.DATABASE_PORT, database=self.DATABASE_NAME)
        #     if self.pg_pool:
        #         print("connection pool created successfully")
        #     self.connection = self.pg_pool.getconn()
        #     self.connection.autocommit = True
        #     if self.connection:
        #         print("connection received successfully")
        #     self.cursor = self.connection.cursor()
        #     # self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        #     # return (self.connection, self.cursor)

        # except (AttributeError, psycopg2.DatabaseError) as _e:
        #     print(_e)

    # def get_db(self):
    #     """ get connection to database """
    #     try:
    #         if self.APP_SETTINGS== "TESTING":
    #             self.pg_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD,
    #                                                         host=self.DATABASE_HOST, port=self.DATABASE_PORT, database=self.DATABASE_TEST)
    #         elif self.APP_SETTINGS== "DEVELOPMENT":
    #             self.pg_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD,
    #                                                         host=self.DATABASE_HOST, port=self.DATABASE_PORT, database=self.DATABASE_NAME)
    #         elif self.APP_SETTINGS== "PRODUCTION":
    #             self.pg_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD,
    #                                                         host=self.DATABASE_HOST, port=self.DATABASE_PORT, database=self.DATABASE_NAME)
    #         if self.pg_pool:
    #             print("connection pool created successfully")
    #         self.connection = self.pg_pool.getconn()
    #         self.connection.autocommit = True
    #         self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #         return (self.connection, self.cursor)

    #     except psycopg2.DatabaseError as e:
    #         print(e)

    def create_all_tables(self):
        """ create all tables. """
        commands = (
        """
        CREATE TABLE IF NOT EXISTS fooditems (
            item_id serial PRIMARY KEY,
            name varchar,
            category varchar,
            price integer NOT NULL
        )
        """,
        """ CREATE TABLE IF NOT EXISTS users (
                id serial PRIMARY KEY,
                name varchar,
                email varchar,
                password varchar,
                gender varchar,
                user_type varchar DEFAULT 'Customer'
                )
        """,
        """
        CREATE TABLE IF NOT EXISTS orders (
                id serial PRIMARY KEY,
                item integer,
                quantity integer,
                status varchar,
                user_id integer,
                FOREIGN KEY (item)
                    REFERENCES fooditems (item_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (user_id)
                    REFERENCES users (id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)
        try:
            self.connection = self.connect_db()
            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) 
            for command in commands:
                self.cursor.execute(command)
            self.connection.close()
        except (psycopg2.DatabaseError) as error:
            print(error)

    def drop_all_tables(self):
        """ delete all tables. """
        commands = (
        """
        DROP TABLE IF EXISTS fooditems CASCADE
        """,
        """ DROP TABLE IF EXISTS users CASCADE
        """,
        """
        DROP TABLE IF EXISTS orders CASCADE
        """)
        try:
            self.connection = self.connect_db()
            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            for command in commands:
                self.cursor.execute(command)
            self.connection.close()
        except (psycopg2.DatabaseError) as error:
            print(error)


    def drop_connection(self):
        """ drop single connection """
        # if self.pg_pool:
        #     self.pg_pool.putconn(self.connection)
        print("connection closed")

    def close_connection(self):
        """ drop all connection """
        self.cursor.close()
        self.connection.close()
        # if self.pg_pool:
        #     self.pg_pool.closeall
        #     print("pg connections closed")

