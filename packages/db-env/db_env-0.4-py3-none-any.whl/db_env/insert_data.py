# import for testing
import sqlite3



# Function - INSERT INTO TABLE
def insert_into_sql_manually(sql_string:str, db_name:str):
    '''
    - sql_string = SQL-INSERT INTO statement as string (e.g. "INSERT INTO ORDERS (ID, NAME) VALUES (1, 'Frank');"
    - db_name = Name of database as string
    '''
    # Connecting to database
    try:
        global cursor
        global connection
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        print("DONE - connected to DB")
    except:
        print("ERROR - can't connect to DB. Check connection and/or db_name if exists")
    # Inserting data into database
    try:
        cursor.execute(sql_string)
        connection.commit()
        print("DONE - inserted data into table")
    except:
        print("ERROR - can't insert data into table. Check sql_string and if DB exists")