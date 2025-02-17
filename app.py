from flask import Flask, request, render_template, url_for, session
import Database as db

app = Flask(__name__)

db = db.Database()

@app.route('/')
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Assign form data into variables
        amount = request.form.get("amount")
        category = request.form.get("category")
        description = request.form.get("description")
        date = request.form.get("date")

        modify = request.form.get("modify")
        expense_ids = request.form.getlist("expense_id")

        # Check form for modification type
        if modify == "clear": # Clear all expenses
            db.clear_all_expenses()
        elif modify == "remove" and expense_ids: # Clear selected expenses from db by id
            db.clear_expenses(expense_ids)
        elif amount and category and description and date and modify == "add": # add new expense to db
            db.add_expense(amount, category, description, date)

    expenses = db.get_expenses() # get all expenses from db
    return render_template("home.html", expenses=expenses)

# TODO: Implement login page
@app.route("/login", methods=["GET", "POST"])
def login():
    pass

# TODO: Implement summary page
@app.route("/summary", methods=["GET", "POST"])
def summary():
    pass

if __name__ == "__main__":
    app.run(debug=True)