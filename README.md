# Expense Tracker

![Expense Tracker UI](static/image-new.png)

## Description

Expense Tracker is a secure web application for tracking your personal expenses. Users can register, log in, and manage their own expenses. Features include adding, removing, clearing, sorting, and exporting expenses to CSV. The backend is built with Flask and MySQL, and environment variables are used for secure configuration.

---

## Features

- User registration and login (hashed passwords, JWT authentication)
- Add, remove, and clear expenses
- Sort expenses by amount, category, description, or date
- Export expenses to CSV
- Responsive and clean UI

---

## Project Structure

```
ExpenseTracker/
│
├── app.py
├── Database.py
├── requirements.txt
├── .env
├── README.md
│
├── models/
│   └── models.py
│
├── static/
│   ├── home.css
│   ├── auth.css
│   ├── down.png
│   └── image-new.png
│
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── signup.html
│   └── index.html
│
└── expenses.csv
```

---

## Setup

### Prerequisites

- Python 3.11+
- MySQL server

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ExpenseTracker.git
   cd ExpenseTracker
   ```

2. **Install required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the MySQL database:**
   ```sql
   CREATE DATABASE expense_tracker;
   USE expense_tracker;

   CREATE TABLE accounts (
       account_id INT AUTO_INCREMENT PRIMARY KEY,
       public_id VARCHAR(100) NOT NULL,
       username VARCHAR(100) NOT NULL,
       password VARCHAR(255) NOT NULL,
       email VARCHAR(255) NOT NULL
   );

   CREATE TABLE expenses (
       expense_id INT AUTO_INCREMENT PRIMARY KEY,
       amount DECIMAL(10, 2) NOT NULL,
       category VARCHAR(255) NOT NULL,
       description TEXT,
       date DATE NOT NULL,
       account_id INT,
       FOREIGN KEY (account_id) REFERENCES accounts(account_id)
   );
   ```

4. **Create a `.env` file in the project root:**
   ```env
   MYSQLHOST=localhost
   MYSQLUSER=your_mysql_username
   MYSQLPASSWORD=your_mysql_password
   MYSQLDATABASE=expense_tracker
   ```

---

## Running the Application

1. **Start the Flask application:**
   ```bash
   python app.py
   ```

2. **Open your browser and go to:**  
   `http://127.0.0.1:5000/`

---

## Usage

- **Sign Up / Login:** Register a new account or log in with your credentials.
- **Add Expense:** Fill in the form with amount, category, description, and date, then click "Add Expense".
- **Remove Selected:** Select expenses using the checkboxes and click "Remove Selected".
- **Clear All Data:** Click "Clear All Data" to remove all your expenses.
- **Sort Data:** Click the down arrow next to each column name to sort by that column.
- **Export to CSV:** Click "Convert to CSV" to download your expenses as a CSV file.

---

## Security

- Passwords are hashed using Werkzeug.
- User authentication is handled with JWT tokens stored in cookies.
- Database credentials are managed via environment variables.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Author

Justin Toliver

---
