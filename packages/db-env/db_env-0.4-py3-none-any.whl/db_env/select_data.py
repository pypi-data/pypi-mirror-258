# import for testing
import sqlite3
import pandas



# Function - Selecting data from database and automatically creating dataframe
def select_values_sql(sql_string:str, db_name:str, df_name:str, *column_names:str):
    '''
    - sql_string = SQL-SELECT statement as string (e.g. "SELECT * FROM TABLE_CUSTOMER;")
    - db_name = Name of database as string
    - dataframe_name = Name of to be created pandas dataframe
    - column_names = *args = Name(s) of to be created columns within pandas dataframe. Accepts several arguments.

    Further Info:
    - cursor needs fetchall() in order to select/fetch data.
    - automatically generates Dataframe with right name and columns.
    - Info on globals()[dataframe_name]: dataframe_name is assigned to be a global variable.
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
    # Selecting data from database
    try:
        cursor.execute(sql_string)
        result = cursor.fetchall()
        print("DONE - selected values from DB")
        globals()[df_name] = pandas.DataFrame(result, columns =[*column_names])
        print("DONE - created dataframe")
    except:
        print("ERROR - can't select data from DB and/or create dataframe")


