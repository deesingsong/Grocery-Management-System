import pyodbc
from mysql.connector import Error
import utils

class Groceries:
    def __init__(self, name, exp_date, price, specification):
        self.name = name
        self.exp_date = exp_date
        self.price = price
        self.specification = specification

    # Function to fetch a specific grocery item by ID from the database
    def get_grocery_by_id(self, grocery_id, cursor):
        try:
            select_query = "SELECT * FROM groceries WHERE id = ?"
            cursor.execute(select_query, (grocery_id,))
            grocery_data = cursor.fetchone()

            if grocery_data:
                return grocery_data
            
            return None
        except Exception as e:
            print("\nError occurred while fetching grocery by ID:", e)
            return None
        
    # Function to print available groceries
    def view_groceries(self):
        try:
            db_connection = utils.get_db_connection()
            cursor = db_connection.cursor()
            select_query = "SELECT * FROM groceries"
            cursor.execute(select_query)
            groceries = cursor.fetchall()

            print("\nAvailable Groceries:")
            for grocery in groceries:
                print(f"ID: {grocery[0]}, Name: {grocery[1]}, Price: RM{grocery[3]}")
                print(f"       Expiry Date: {grocery[2]}, Specifications: {grocery[4]}")

            cursor.close()
            utils.close_db_connection(db_connection)
        except Exception as e:
            print("\nError occurred while fetching groceries:", e)

    # Function to insert a new grocery item into the database
    def insert_grocery(self, grocery):
        try:
            db_connection = utils.get_db_connection()
            cursor = db_connection.cursor()

            insert_query = """
            INSERT INTO groceries (name, exp_date, price, specification)
            VALUES (?, ?, ?, ?)
            """
            cursor.execute(insert_query, (grocery.name, grocery.exp_date, grocery.price, grocery.specification))
            db_connection.commit()
            cursor.close()
            utils.close_db_connection(db_connection)
            print("\nGrocery item added successfully.")
        except Error as e:
            print("\nError occurred while inserting grocery item:", e)

    # Query to update a grocery item in the database
    def update_grocery(self, updated_grocery, cursor):
        try:
            update_query = """
            UPDATE groceries
            SET name = ?, exp_date = ?, price = ?, specification = ?
            WHERE id = ?
            """
            cursor.execute(update_query, (updated_grocery.name, updated_grocery.exp_date, updated_grocery.price, updated_grocery.specification, updated_grocery.id))
            print("\nGrocery item updated successfully.")
        except pyodbc.Error as e:
            print("\nError occurred while updating grocery item:", e)

    # Function to delete a grocery item from the database by ID
    def delete_grocery(self, grocery_id):
        try:
            db_connection = utils.get_db_connection()
            cursor = db_connection.cursor()
            delete_query = "DELETE FROM groceries WHERE id = ?"
            cursor.execute(delete_query, (grocery_id,))
            db_connection.commit()
            cursor.close()
            utils.close_db_connection(db_connection)
            print("\nGrocery item deleted successfully.")
        except pyodbc.Error as e:
            print("\nError occurred while deleting grocery item:", e)

