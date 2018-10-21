""" Defines operations to database for the app """
import psycopg2
import psycopg2.extras
from environs import Env

class DatabaseConnection(object):
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
        self.connection = None
        self.cursor = None


    def connect_db(self):
        """ establish connection to database depending on app settings. """
        try:
            if self.APP_SETTINGS == "TESTING":
                self.connection = psycopg2.connect(self.DATABASE_TEST_URL)
            elif self.APP_SETTINGS == "DEVELOPMENT":
                self.connection = psycopg2.connect(self.DATABASE_URL)
            elif self.APP_SETTINGS == "PRODUCTION":
                self.connection = psycopg2.connect(self.DATABASE_URL, sslmode='require')

            self.connection.autocommit = True
            return self.connection
        except AttributeError as _ae:
            print("Can't connect to database" + _ae)

    def create_all_tables(self):
        """ create all tables in db. """
        commands = (
            """
            CREATE TABLE IF NOT EXISTS fooditems (
                item_id serial PRIMARY KEY,
                name varchar,
                category varchar,
                price integer NOT NULL,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status varchar DEFAULT 'Published'
            )
            """,
            """ CREATE TABLE IF NOT EXISTS users (
                    id serial PRIMARY KEY,
                    name varchar,
                    email varchar,
                    password varchar,
                    gender varchar,
                    user_type varchar DEFAULT 'Customer',
                    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
            """,
            """
            CREATE TABLE IF NOT EXISTS orders (
                    id serial PRIMARY KEY,
                    item integer,
                    quantity integer,
                    status varchar,
                    user_id integer,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
        """ drop all db tables. """
        drop_commands = (
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
            for command in drop_commands:
                self.cursor.execute(command)
            self.connection.close()
        except (psycopg2.DatabaseError) as error:
            print(error)

    def close_connection(self):
        """ drop all connection """
        self.cursor.close()
        self.connection.close()
