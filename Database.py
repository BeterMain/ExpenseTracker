import mysql.connector
import csv
from dotenv import load_dotenv
import os 

class Database:
    def __init__(self):
        load_dotenv()
        self.host = os.getenv('HOSTNAME')
        self.user = os.getenv('USERNAME')
        self.password = os.getenv('PASSWORD')
        self.database = os.getenv('DB_NAME')
        self.sort_column = 'date'
    
    # Executes INSERT query on db to add an expense
    def add_expense(self, amount, category, description, date):
        # Attempt to connect to the database
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        cursor = conn.cursor()

        # Assigns the SQL query to insert a new expense into the database
        sql = "INSERT INTO expenses (amount, category, description, date) VALUES (%s, %s, %s, %s)"
        values = (amount, category, description, date)
        
        # Execute query and commit changes
        cursor.execute(sql, values)
        conn.commit()
        conn.close()
    
    # Executes DELETE query on db to clear all expenses
    def clear_all_expenses(self):
        # Attempt to connect to the database
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        cursor = conn.cursor()    

        # Assigns the SQL query to delete all expenses from the database
        sql = "DELETE FROM expenses"
        
        # Execute query and commit changes
        cursor.execute(sql)
        conn.commit()
        conn.close()
    
    # Executes DELETE query on db to clear selected expenses
    def clear_expenses(self, expense_id=[]):
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
        sql += ")" # adding closing tag

        # Converting list of ids to a tuple for SQL query
        values = ()
        if len(expense_id) > 0:
            values = tuple(expense_id)

        # Execute query and commit changes
        cursor.execute(sql, values)
        conn.commit()
        conn.close()

    # Executes SELECT query on db to fetch all expenses
    def get_expenses(self, column='date'):
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

        cursor.execute(f"SELECT * FROM expenses ORDER BY {self.sort_column} DESC")
        # Gathers results in list
        expenses = cursor.fetchall()
        
        conn.close()
        # Return results
        return expenses

    def convert_to_csv(self):
         # Attempt to connect to the database
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM expenses ORDER BY {self.sort_column} DESC")
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