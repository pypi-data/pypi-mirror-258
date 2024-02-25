**Version 0.4**

--- What can db_env do? --- 
db_env aims to make it easier and more straight forward to create relational database environments within Python. db_env uses SQLite and Pandas as dependencies. Currently db_env holds the following functions:
- create_connect_db --> connecting to newly created database
- create_table_sql --> connecting to database and creating tables within
- insert_data_sql --> connecting to database and inserting data
- select_data_sql --> connecting and fetching data from chosen tables. It automatically creates a new Pandas dataframe for further analysis.


--- important Info: --- 
- this library needs SQLite3 and Pandas in addition. As dependencies all packages will be installed automatically.
- SQL-Usage: db_env uses SQLite and therefore SQL-statements for creating, calling and manipulating data. 
- it is encouraged to import your writen SQL-strings from another py-file as a variable (e.g. ENUM). However, you can directly insert your SQL-statement as a string into the function.

--- Example SQL-statements for existing functions: --- 
--> create_table_sql = 
"DROP TABLE IF EXISTS ORDERS; CREATE TABLE ORDERS(ID INTEGER, NAME VARCHAR(30));"

--> insert_data_sql = 
"INSERT INTO ORDERS (ID, NAME) VALUES (1, 'Frank');" 
or 
(f'''INSERT INTO ORDERS (ID, NAME) VALUES 
                         (5, 'John'),
                         (6, 'Tobias'),
                         (7, 'Lisa');''', "orders.db")

--> select_data_sql = 
"SELECT * FROM ORDERS;"


--- Goal for upcoming versions: --- 
- Functions which give user the option to write his own SQL-statements into an extra Python file and call writen SQL-strings as variables into your working environment.
- Functions to collect and insert data from called API.


-------------- CHANGES in VERSION 0.4 --------------
2024-02-24

- installed dependencies (SQLite, Pandas)
- created function to select data from db and create dataframe
- created function to insert data into database manually

----------------------------------------------------