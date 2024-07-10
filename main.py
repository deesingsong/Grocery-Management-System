from admin import Admin
from customer import Customer
from groceries import Groceries
import utils
import re
from datetime import datetime

def main():
    print("Welcome to the Online Groceries Management System (OGMS)")
    groceries = Groceries("", "", 0.0, "")
    while True:
        print("\nChoose user type:")
        print("1. Admin")
        print("2. New Customer")
        print("3. Registered Customer")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            admin = Admin()
            admin.login()
            if admin.logged_in:
                admin_menu(admin, groceries)
        elif choice == "2":
            register_new_customer()
        elif choice == "3":
            customer = Customer("", "", "", "", "", "", "username", "password")
            customer.login()
            if customer.logged_in:
                registered_customer_menu(customer, groceries)
        elif choice == "4":
            print("\nThank you for using Online Groceries Management System (OGMS). Goodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")

def admin_menu(admin, groceries):
    while True:
        print("\nAdmin Menu:")
        print("1. Upload Groceries")
        print("2. View All Groceries")
        print("3. Update Groceries")
        print("4. Delete Groceries")
        print("5. View All Orders")
        print("6. View all Customer Information")
        print("7. Logout")
        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            admin.upload_groceries(groceries)
        elif choice == "2":
            groceries.view_groceries()
        elif choice == "3":
            admin.update_groceries(groceries)
        elif choice == "4":
            admin.delete_groceries(groceries)
        elif choice == "5":
            admin.view_all_orders()
        elif choice == "6":
            admin.view_customer_info()
        elif choice == "7":
            admin.logout()
            break
        else:
            print("\nInvalid choice. Please try again.")

def register_new_customer():
    db_connection = utils.get_db_connection()
    print("\nNew Customer Registration:")
    # Name
    name = input("\nEnter your name: ")
    if not re.match("^[A-Za-z\s]+$", name):
        print("\nInvalid name format. Please enter letters and spaces only.")
        return
    # Address
    address = input("Enter your mailing address: ")
    # Email
    email = input("Enter your email address: ")
    if not re.match(r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$", email):
        print("\nInvalid email format. Please enter a valid email address.")
        return
    # Contact number
    contact_number = input("Enter your contact number (01XXXXXXXX): ")
    cleaned_contact_number = contact_number.replace(" ", "").replace("-", "")
    if not cleaned_contact_number.isdigit():
        print("\nInvalid contact number. Please enter a numeric contact number without spaces or lines.")
        return
    # Gender input with formatting
    gender = input("Enter your gender (M/F): ")
    gender = gender.upper()
    if gender not in ['M', 'F']:
        print("\nInvalid gender. Please enter 'M' for Male or 'F' for Female.")
        return
    # DOB input with formatting
    date_of_birth = input("Enter your date of birth (YYYY-MM-DD): ")
    try:
        datetime.strptime(date_of_birth, "%Y-%m-%d")
    except ValueError:
        print("\nInvalid date format. Please enter a valid date in YYYY-MM-DD format.")
        return
    # Username input with availability check
    customer = Customer("", "", "", "", "", "", "username", "password")
    username = input("Choose a username: ")
    if not customer.is_username_available(username, None):
        return
    # Confirmation to proceed with registration
    proceed = input("\nIs the above information correct? Enter (y/n) if you would like to proceed: ")
    if proceed.lower() != 'y':
        print("\nRegistration cancelled.")
        return
    # Password input with confirmation
    password = input("\nChoose a password: ")
    rewrite_password = input("Re-enter your password: ")
    if password != rewrite_password:
        print("\nPasswords do not match. Registration failed.")
        return
    # Complete registration
    try:
        insert_query = """
        INSERT INTO customers (name, address, email, contact_number, gender, date_of_birth, username, password)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor = db_connection.cursor()
        cursor.execute(insert_query, (name, address, email, contact_number, gender, date_of_birth, username, password))
        db_connection.commit()
        cursor.close()
        print("\nRegistration successful. Welcome, {}!".format(name))
    except Exception as e:
        print("\nError occurred while registering customer:", e)
    finally:
        db_connection.close()

def registered_customer_menu(customer, groceries):
    groceries = Groceries("", "", 0.0, "")

    while True:
        print("\nRegistered Customer Menu:")
        print("1. View Groceries")
        print("2. Place Order")
        print("3. View Own Order")
        print("4. Delete Existing Orders")
        print("5. View Personal Information")
        print("6. Edit Personal Information")
        print("7. Logout")
        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            groceries.view_groceries()
        elif choice == "2":
            customer.place_order(groceries)
        elif choice == "3":
            customer.view_own_order()
        elif choice == "4":
            customer.delete_orders()
        elif choice == "5":
            customer.view_personal_info()
        elif choice == "6":
            customer.edit_personal_info()
        elif choice == "7":
            customer.logout()
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
