# import for testing
import sqlite3


# Function - creating DB and connecting to it
def create_connect_db(db_name:str):
    '''
    - db_name = name of database with ending .db (e.g. "zoo.db")
    - create and connect to unique database within your folder
    '''
    global cursor
    global connection
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        print("db_env: DONE - connected and created database: ", db_name)
    except:
        print("db_env: ERROR - can not create/connect to DB. Check connection or if database-name already exists")


# Function - creating table
def create_table_sql(sql_string:str):
    '''
    - sql_string = SQL-CREATE statement which creates table
    - create table function which uses string as an input
    - e.g. "DROP TABLE IF EXISTS CUSTOMERS;CREATE TABLE CUSTOMERS(NAME VARCHAR(30),AGE INTEGER, ORDER_ID INTEGER);"
    - Info: uses executescript instead of execute so that more than one sql statement in one execute is possible'''
    try:
        cursor.executescript(sql_string)
        connection.commit
        print("db_env: DONE - created table")
    except:
        print("db_env: ERROR - can not create table. Please check inserted string and if databbase exists")