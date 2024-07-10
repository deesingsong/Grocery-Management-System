# Grocery Management System

## Description
This project is a grocery management system. The project is implemented using Python and utilizes an SQL Server database from MSSQL for data storage.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation
To install and set up this project, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/deesingsong/Grocery-Management-System.git
    cd Grocery-Management-System
    ```

2. **Set up a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure your database:**
   Ensure you have a SQL Server database set up and update the connection details in `utils.py`:
    ```python
    import pyodbc

    def get_db_connection():
        server = 'Your_Server_Name'
        database = 'groceries_db'
        trusted_connection = 'yes'

        try:
            conn = pyodbc.connect(f'SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection}')
            return conn
        except pyodbc.Error as e:
            print("Error occurred while connecting to the database:", e)
            return None

    def close_db_connection(connection):
        try:
            if connection:
                connection.close()
                print("Database connection closed.")
        except pyodbc.Error as e:
            print("Error occurred while closing the database connection:", e)
    ```

## Usage
1. **Run the application:**
    ```bash
    python main.py
    ```

2. **Admin operations:**
   - **Login as Admin**
   - **Upload Groceries**
   - **Update Groceries**
   - **Delete Groceries**
   - **View All Groceries**
   - **View All Orders**
   - **Search Orders**

3. **Customer operations:**
   - **View Groceries**
   - **Register as a New Customer**
   - **Login as a Registered Customer**
   - **Place Orders**
   - **View Personal Information**

## Contributing
Contributions are welcome! Please fork this repository and create a pull request with your changes. Ensure your code follows the project's coding standards and includes appropriate tests.

## License
This project is licensed under the [MIT License](LICENSE).

## Contact
For any questions or inquiries, please contact:
- Name: Jonathan Chieng
- Email: jofartjobs@gmail.com
- GitHub: [deesingsong](https://github.com/deesingsong)
