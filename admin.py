import pyodbc
from groceries import Groceries
import utils

class Admin:
    def __init__(self):
        self.logged_in = False

    def login(self):
        print("\nAdmin Login:")
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")
        if self.validate_login(username, password):
            self.logged_in = True
            print("\nLogin successful. Welcome, admin!")
        else:
            print("\nInvalid username or password. Login failed.")
    def validate_login(self, username, password):
        admin_credentials = {
            "admin": "admin123"
        }
        if username in admin_credentials and admin_credentials[username] == password:
            return True
        return False
    def logout(self):
        print("\nLogging out from admin account.")
        self.logged_in = False
    
    # Function for admin to upload new groceries
    def upload_groceries(self, groceries):
        print("\nUpload Groceries:")
        name = input("Enter grocery name: ")
        exp_date = input("Enter expiry date (YYYY-MM-DD): ")
        price = float(input("Enter price: "))
        specification = input("Enter specification: ")

        new_grocery = Groceries(name, exp_date, price, specification)
        groceries.insert_grocery(new_grocery)

    # Function for admin to update existing groceries
    def update_groceries(self, groceries):
        groceries.view_groceries()

        print("\nUpdate Groceries:")
        grocery_id = int(input("Enter the ID of the grocery to update: "))

        try:
            db_connection = utils.get_db_connection()
            cursor = db_connection.cursor()

            grocery = groceries.get_grocery_by_id(grocery_id, cursor)
            if grocery:

                print("\nSelected grocery: ")
                print(f"ID: {grocery[0]}, Name: {grocery[1]}, Price: RM{grocery[3]}")
                print(f"       Expiry Date: {grocery[2]}, Specifications: {grocery[4]}")
                name = input("\nUpdate grocery name: ")
                exp_date = input("Update expiry date (YYYY-MM-DD): ")
                price = float(input("Update price: "))
                specification = input("Update specification: ")

                updated_grocery = Groceries(name, exp_date, price, specification)
                updated_grocery.id = grocery[0]
                groceries.update_grocery(updated_grocery, cursor)
                db_connection.commit()
            else:
                print("\nGrocery not found.")

            cursor.close()
            utils.close_db_connection(db_connection)
        except Exception as e:
            print("\nError occurred while updating grocery:", e)

    # Function for admin to delete existing groceries
    def delete_groceries(self, groceries):
        groceries.view_groceries()

        print("\nDelete Groceries:")
        grocery_id = int(input("Enter the ID of the grocery to delete: "))

        try:
            db_connection = utils.get_db_connection()
            cursor = db_connection.cursor()

            confirm = input("Are you sure you want to delete this grocery? (y/n): ").lower()
            if confirm == "y":
                groceries.delete_grocery(grocery_id)
            else:
                print("\nDeletion canceled.")

            cursor.close()
            utils.close_db_connection(db_connection)
        except Exception as e:
            print("\nError occurred while deleting grocery:", e)

    # Function for admin to view all orders placed by customers
    def view_all_orders(self):
        try:
            db_connection = utils.get_db_connection()

            if db_connection:
                cursor = db_connection.cursor()
                select_query = "SELECT * FROM orders"
                cursor.execute(select_query)
                orders = cursor.fetchall()
                cursor.close()
                utils.close_db_connection(db_connection)

                if orders:
                    print("\nAll Orders:")
                    for order in orders:
                        print(f"\nOrder ID:  {order[0]}")
                        print(f"Customer ID: {order[1]}           Customer Username: {order[5]}")
                        print(f"Grocery ID:  {order[2]}           Grocery Name: {order[6]} | Quantity: {order[3]}")
                        print(f"Order Date:  {order[4]}")
                else:
                    print("\nNo orders found.")

            else:
                print("\nFailed to establish a database connection.")
        except pyodbc.Error as e:
            print("\nError occurred while fetching orders:", e)

    # Function for admin to view all customers and their account information
    def view_customer_info(self):
        try:
            db_connection = utils.get_db_connection()
            cursor = db_connection.cursor()

            select_query = """
            SELECT c.id, c.name, c.address, c.email, c.contact_number, c.gender, c.date_of_birth, 
                   COUNT(o.id) AS order_count, STRING_AGG(CONVERT(VARCHAR, o.id), ', ') AS order_ids
            FROM customers c
            LEFT JOIN orders o ON c.id = o.customer_id
            GROUP BY c.id, c.name, c.address, c.email, c.contact_number, c.gender, c.date_of_birth
            """
            cursor.execute(select_query)
            customers = cursor.fetchall()

            if customers:
                print("\nAll Customers' Account Information:")
                for customer in customers:
                    print(f"\nCustomer ID: {customer[0]}")
                    print(f"Name: {customer[1]}, Gender: {customer[5]}, Date of Birth: {customer[6]}")
                    print(f"Address: {customer[2]}")
                    print(f"Email: {customer[3]}, Contact Number: {customer[4]}")
                    print(f"Number of Orders: {customer[7]} | Order IDs: {customer[8]}")
            else:
                print("\nNo customers found.")

            cursor.close()
            utils.close_db_connection(db_connection)
        except pyodbc.Error as e:
            print("\nError occurred while fetching customers' account information:", e)
