import pyodbc

# Function to get a database connection
def get_db_connection():
    server = 'JONSNEWFLOPPY'
    database = 'groceries_db'
    trusted_connection = 'yes'

    try:
        db_connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection}')
        return db_connection
    except pyodbc.Error as e:
        print("\nError occurred while connecting to the database:", e)
        return None

# Function to close a database connection
def close_db_connection(connection):
    try:
        if connection:
            connection.close()
    except pyodbc.Error as e:
        print("\nError occurred while closing the database connection:", e)
        