import mysql.connector
import csv
from dotenv import load_dotenv
import os 
from models.models import User

class Database:
    def __init__(self):
        load_dotenv()
        self.host = os.getenv('MYSQLHOST')
        self.user = os.getenv('MYSQLUSER')
        self.password = os.getenv('MYSQLPASSWORD')
        self.database = os.getenv('MYSQLDATABASE')
        self.sort_column = 'date'
    
    # Executes INSERT query on db to add an expense
    def add_expense(self, amount, category, description, date, account_id):
        # Attempt to connect to the database
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        cursor = conn.cursor()

        # Assigns the SQL query to insert a new expense into the database
        sql = "INSERT INTO expenses (amount, category, description, date, account_id) VALUES (%s, %s, %s, %s, %s)"
        values = (amount, category, description, date, account_id)
        
        # Execute query and commit changes
        cursor.execute(sql, values)
        conn.commit()
        conn.close()
    
    # Executes DELETE query on db to clear all expenses
    def clear_all_expenses(self, account_id):
        # Attempt to connect to the database
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        cursor = conn.cursor()    

        # Assigns the SQL query to delete all expenses from the database
        sql = f"DELETE FROM expenses WHERE account_id = {account_id}"
        
        # Execute query and commit changes
        cursor.execute(sql)
        conn.commit()
        conn.close()
    
    # Executes DELETE query on db to clear selected expenses
    def clear_expenses(self, expense_id, account_id):
        # Attempt to connect to the database
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        cursor = conn.cursor()    

        # Assigns the SQL query to delete selected expenses from the database
        sql = "DELETE FROM expenses WHERE expense_id IN (%s"
        for i in range(len(expense_id)-1): # appending each need value to the sql string
            sql += ", %s"
        sql += f") AND account_id = {account_id}" # adding closing tag and extra case

        # Converting list of ids to a tuple for SQL query
        values = ()
        if len(expense_id) > 0:
            values = tuple(expense_id)

        # Execute query and commit changes
        cursor.execute(sql, values)
        conn.commit()
        conn.close()

    # Executes SELECT query on db to fetch all expenses
    def get_expenses(self, column, account_id):
        # Attempt to connect to the database
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        cursor = conn.cursor()

        # Assigns the correct scope of SELECT query
        if column not in ['amount', 'category', 'description', 'date']:
            column = 'date'
        self.sort_column = column

        cursor.execute(f"SELECT expense_id, amount, category, description, date FROM expenses INNER JOIN accounts ON expenses.account_id = accounts.account_id WHERE accounts.account_id = {account_id} ORDER BY {self.sort_column} DESC")
        # Gathers results in list
        expenses = cursor.fetchall()
        
        conn.close()
        # Return results
        return expenses

    def convert_to_csv(self, account_id):
         # Attempt to connect to the database
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        cursor = conn.cursor()

        cursor.execute(f"SELECT amount, category, description, date FROM expenses INNER JOIN accounts ON expenses.account_id = accounts.account_id WHERE accounts.account_id = {account_id} ORDER BY {self.sort_column} DESC")
        rows = cursor.fetchall()

        columns = [col[0] for col in cursor.description]
        conn.close()
        
        # Convert rows into JSON
        data = [dict(zip(columns, row)) for row in rows]
        
        # Convert JSON to CSV
        csv_file_path = 'expenses.csv'
        
        with open(csv_file_path, 'w') as file:
            csv_writer = csv.writer(file)
            
            # Write header
            if data:
                header = data[0].keys()
                csv_writer.writerow(header)
                
                # Write data rows
                for item in data:
                    csv_writer.writerow(item.values())

        return csv_file_path

    # Accounts
    def add_new_user(self, public_id, name, password, email):
        # Attempt to connect to the database
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        cursor = conn.cursor()

        # execute query
        sql = "INSERT INTO accounts (public_id, username, password, email) VALUES (%s, %s, %s, %s)"
        values = (public_id, name, password, email)
        cursor.execute(sql, values)
        conn.commit()
        conn.close()

    def find_by_email(self, email):
        # Attempt to connect to the database
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        cursor = conn.cursor()
        
        # Execute find query based on email
        cursor.execute(f"SELECT * FROM accounts WHERE email='{email}'")
        
        # Getting data
        row = cursor.fetchall()
        conn.close()

        # Check if there are any entries
        if row:
            print(row)
            return True
        
        return False

    # Finds user by public id and returns a User object that contains their information
    def find_by_public_id(self, public_id: str):
        # Attempt to connect to the database
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        cursor = conn.cursor()
        
        # Execute find query based on email
        cursor.execute(f"SELECT * FROM accounts WHERE public_id='{public_id}'")
        
        # Getting data
        row = cursor.fetchall()
        conn.close()
        
        data = row[0]

        # Turn row data into User object
        return User(data[2], data[3], data[4], data[0], data[1])

    def find_by_username(self, name):
        # Attempt to connect to the database
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        cursor = conn.cursor()
        
        # Execute find query based on email
        cursor.execute(f"SELECT * FROM accounts WHERE username='{name}'")
        
        # Getting data
        row = cursor.fetchall()
        conn.close()

        # Check if there are any entries
        return row