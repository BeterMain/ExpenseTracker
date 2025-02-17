import mysql.connector
import pandas as pd

class Database:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'username'
        self.password = 'password'
        self.database = 'expense_tracker'
    
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
        sql = "DELETE FROM expenses WHERE id IN (%s"
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
    def get_expenses(self, column='*'):
        # Attempt to connect to the database
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        cursor = conn.cursor()

        # Assigns the correct scope of SELECT query
        if column not in ['*', 'amount', 'category', 'description', 'date']:
            column = '*'

        cursor.execute(f"SELECT {column} FROM expenses ORDER BY date DESC")
        # Gathers results in list
        expenses = cursor.fetchall()
        
        conn.close()
        # Return results
        return expenses

    # TODO: Implement this function into separate page to display monthly summary with graphs
    def monthly_summary(self):
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        df = pd.read_sql_query("SELECT * FROM expenses", conn)
        conn.close()

        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df["date"].dt.strftime("%Y-%m")

        summary = df.groupby("month")["amount"].sum()
        return summary