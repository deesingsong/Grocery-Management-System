import utils
import re
from datetime import datetime

class Customer:
    def __init__(self, name, address, email, contact_number, gender, date_of_birth, username, password):
        self.name = name
        self.address = address
        self.email = email
        self.contact_number = contact_number
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.username = username
        self.password = password
        self.logged_in = False
        self.target_username = None

    def login(self):
        print("\nCustomer Login:")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        customer = self.validate_login(username, password)

        if customer:
            self.logged_in = True
            self.target_username = customer.username
            print(f"\nLogin successful. Welcome, {customer.name}!")
        else:
            print("\nInvalid username or password. Login failed.")
    def validate_login(self, username, password):
        db_connection = utils.get_db_connection()

        if db_connection:
            cursor = db_connection.cursor()
            select_query = "SELECT * FROM customers WHERE username = ? AND password = ?"
            cursor.execute(select_query, (username, password))
            customer = cursor.fetchone()
            cursor.close()
            utils.close_db_connection(db_connection)

            if customer:
                return Customer(*customer[1:])
            else:
                return None
    def logout(self):
        print("\nLogging out from the registered customer account.")
        self.logged_in = False

    # Function to check if username is available
    def is_username_available(self, new_username, customer_id):
        try:
            db_connection = utils.get_db_connection()
            cursor = db_connection.cursor()

            select_query = "SELECT id FROM customers WHERE username = ?"
            cursor.execute(select_query, (new_username,))
            existing_id = cursor.fetchone()

            cursor.close()
            db_connection.close()
            if existing_id is None or existing_id[0] == customer_id:
                return True
            else:
                print("\nUsername is already taken.")
                return False
        except Exception as e:
            print("\nError occurred while checking username availability:", e)
            return False

    # Function to get the customer's ID based on their username
    def get_customer_id(self):
        try:
            db_connection = utils.get_db_connection()
            cursor = db_connection.cursor()

            select_id_query = "SELECT id FROM customers WHERE username = ?"
            cursor.execute(select_id_query, (self.target_username,))
            customer_id = cursor.fetchone()[0]

            cursor.close()
            utils.close_db_connection(db_connection)

            return customer_id
        except Exception as e:
            print("\nError occurred while getting customer ID:", e)
            return None
        
    # Function to enable customer to place an order
    def place_order(self, groceries):
        try:
            customer_id = self.get_customer_id()
            if customer_id is not None:
                db_connection = utils.get_db_connection()
                cursor = db_connection.cursor()
                
                groceries.view_groceries()

                # Ask the customer to select a grocery item and specify quantity and order date
                grocery_id = int(input("\nEnter the ID of the grocery you want to order: "))
                quantity = int(input("Enter the quantity: "))
                order_date = input("Enter the order date (YYYY-MM-DD): ")

                grocery_data = groceries.get_grocery_by_id(grocery_id, cursor)

                if grocery_data:
                    grocery_name = grocery_data[1]

                    # Insert the order into the orders table with the customer's ID, username, selected grocery's ID, name, quantity, and order date
                    insert_order_query = """
                    INSERT INTO orders (customer_id, customer_username, grocery_id, grocery_name, quantity, order_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """
                    cursor.execute(insert_order_query, (customer_id, self.target_username, grocery_id, grocery_name, quantity, order_date))
                    db_connection.commit()
                    print("\nOrder placed successfully.")
                else:
                    print("\nNo grocery found for the given ID.")
                    return
            else:
                print("\nNo customer ID found for the given username.")
                return
        except Exception as e:
            print("\nError occurred while placing the order:", e)
        finally:
            cursor.close()
            utils.close_db_connection(db_connection)

    # Function to view all existing orders placed by the customer
    def view_own_order(self):
        orders_exist = False
        try:
            db_connection = utils.get_db_connection()
            cursor = db_connection.cursor()

            select_query = """
            SELECT o.id, o.quantity, o.order_date, g.name
            FROM orders o
            JOIN groceries g ON o.grocery_id = g.id
            WHERE o.customer_username = ?
            """
            cursor.execute(select_query, (self.target_username,))
            orders = cursor.fetchall()
            if orders:
                orders_exist = True
                print("\nYour Orders:")
                for order in orders:
                    print(f"\nOrder ID: {order[0]} | Order Date: {order[2]}")
                    print(f"Grocery Name: {order[3]} | Quantity: {order[1]}")
            else:
                print("\nYou have no existing orders.")
        except Exception as e:
            print("\nError occurred while fetching orders:", e)
        finally:
            cursor.close()
            utils.close_db_connection(db_connection)
        return orders_exist

    # Function to enable customers to delete existing orders
    def delete_orders(self):
        orders_exist = self.view_own_order()
        try:
            db_connection = utils.get_db_connection()
            cursor = db_connection.cursor()
            if orders_exist:
                choice = input("\nDo you want to delete any orders? (y/n): ")
                if choice.lower() == "y":
                    order_id = input("Enter the ID of the order you want to delete: ")
                    try:
                        order_id = int(order_id)
                        # Delete an order by the order ID
                        delete_query = "DELETE FROM orders WHERE id = ?"
                        cursor.execute(delete_query, (order_id,))
                        db_connection.commit()
                        print("\nOrder deleted successfully.")
                    except ValueError:
                        print("\nInvalid order ID. Please enter a valid number.")
        except Exception as e:
            print("\nError occurred while deleting orders:", e)
        finally:
            cursor.close()
            utils.close_db_connection(db_connection)

    # Function to enable customers to view their account information
    def view_personal_info(self):
        try:
            db_connection = utils.get_db_connection()
            cursor = db_connection.cursor()

            select_query = "SELECT name, address, email, contact_number, gender, date_of_birth, username FROM customers WHERE username = ?"
            cursor.execute(select_query, (self.target_username,))
            customer_info = cursor.fetchone()

            if customer_info:
                print("\nPersonal Information:")
                print(f"Name:           {customer_info[0]}")
                print(f"Address:        {customer_info[1]}")
                print(f"Email:          {customer_info[2]}")
                print(f"Contact Number: {customer_info[3]}")
                print(f"Gender:         {customer_info[4]}")
                print(f"Date of Birth:  {customer_info[5]}")
                print(f"Username:       {customer_info[6]}")
            else:
                print("\nNo customer information found.")

            cursor.close()
            utils.close_db_connection(db_connection)
        except Exception as e:
            print("\nError occurred while fetching personal information:", e)
    
    # Function to enable customers to edit their account information
    def edit_personal_info(self):
        print("\nEdit Account Information:")

        db_connection = utils.get_db_connection()
        cursor = db_connection.cursor()
        select_query = "SELECT name, address, email, contact_number, gender, date_of_birth, username FROM customers WHERE username = ?"
        cursor.execute(select_query, (self.target_username,))
        current_info = cursor.fetchone()
        cursor.close()
        db_connection.close()

        print("\nCurrent Account Information:")
        print(f"1. Name: {current_info[0]}")
        print(f"2. Address: {current_info[1]}")
        print(f"3. Email: {current_info[2]}")
        print(f"4. Contact Number: {current_info[3]}")
        print(f"5. Gender: {current_info[4]}")
        print(f"6. Date of Birth: {current_info[5]}")
        print(f"7. Username: {current_info[6]}")
        print("8. Password: ********")

        choice = input("Choose which information you would like to change (1-8): ")

        if choice in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            new_value = input(f"\nEnter your new {'Name' if choice == '1' else 'Address' if choice == '2' else 'Email' if choice == '3' else 'Contact Number' if choice == '4' else 'Gender' if choice == '5' else 'Date of Birth' if choice == '6' else 'Username' if choice == '7' else 'Password'}: ")
            confirm = input("Are you sure you want to update this information? (y/n): ").lower()
            if confirm == "y":
                try:
                    db_connection = utils.get_db_connection()
                    cursor = db_connection.cursor()
                    customer_id = self.get_customer_id()
                    update_query = None
                    update_orders_query = None
                    # Update Name
                    if choice == "1":
                        update_query = "UPDATE customers SET name = ? WHERE id = ?"
                        changed_info = "Name"
                    # Update Address
                    elif choice == "2":
                        update_query = "UPDATE customers SET address = ? WHERE id = ?"
                        changed_info = "Address"
                    # Update Email with formatting
                    elif choice == "3":
                        if not re.match(r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$", new_value):
                            print("Invalid email format. Email not updated.")
                            return
                        update_query = "UPDATE customers SET email = ? WHERE id = ?"
                        changed_info = "Email"
                    # Update Contact Number with formatting
                    elif choice == "4":
                        cleaned_new_contact_number = new_value.replace(" ", "").replace("-", "")
                        if not cleaned_new_contact_number.isdigit():
                            print("Invalid contact number format. Contact number not updated.")
                            return
                        update_query = "UPDATE customers SET contact_number = ? WHERE id = ?"
                        changed_info = "Contact Number"
                    # Update Gender with formatting
                    elif choice == "5":
                        new_value = new_value.upper()
                        if new_value not in ['M', 'F']:
                            print("Invalid gender. Gender not updated.")
                            return
                        update_query = "UPDATE customers SET gender = ? WHERE id = ?"
                        changed_info = "Gender"
                    # Update Date with formatting
                    elif choice == "6":
                        try:
                            datetime.strptime(new_value, "%Y-%m-%d")
                        except ValueError:
                            print("Invalid date format. Date of Birth not updated.")
                            return
                        update_query = "UPDATE customers SET date_of_birth = ? WHERE id = ?"
                        changed_info = "Date"
                    # Update Username in customers table and Customer Username in orders table
                    # Reset username used for authentication
                    elif choice == "7":
                        if not self.is_username_available(new_value, customer_id):
                            print("Username is already taken. Please choose another.")
                            return
                        update_query = "UPDATE customers SET username = ? WHERE id = ?"
                        update_orders_query = "UPDATE orders SET customer_username = ? WHERE customer_id = ?"
                        self.target_username = new_value
                        changed_info = "Username"
                    # Update Password with confirmation
                    elif choice == "8":
                        new_rewrite_password = input("Re-enter your new password: ")
                        if new_value != new_rewrite_password:
                            print("Passwords do not match. Password not updated.")
                            return
                        update_query = "UPDATE customers SET password = ? WHERE id = ?"
                        changed_info = "Password"
                    # Execute selected information update
                    if update_query:
                        cursor.execute(update_query, (new_value, customer_id))
                        # Execute username change in orders table as well if username is changed
                        if choice == "7":
                            orders_cursor = db_connection.cursor()
                            orders_cursor.execute(update_orders_query, (new_value, customer_id))
                            orders_cursor.close()
                        db_connection.commit()
                        print(f"\n{changed_info} updated successfully.")
                except Exception as e:
                    print("\nError occurred while updating:", e)
                finally:
                    cursor.close()
                    db_connection.close()
            else:
                print("\nNo changes made.")
        else:
            print("\nInvalid choice.")