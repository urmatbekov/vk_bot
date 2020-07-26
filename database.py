import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # conn.execute('''CREATE TABLE weather
        #          (current_date   CURRENT_DATE  NOT NULL,
        #          date    CHAR(50)    NOT NULL UNIQUE,
        #          temp            CHAR(50)     NOT NULL,
        #          pressure        CHAR(50),
        #          humidity         CHAR(50));''')
        #
    except Error as e:
        print(e)
    finally:
        if conn:
            return conn

