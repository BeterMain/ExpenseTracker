from flask import Flask, request, render_template, send_file
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
        match modify:
            case "clear": # Clear all expenses
                db.clear_all_expenses()
            case "remove" if expense_ids: # Clear selected expenses from db by id
                db.clear_expenses(expense_ids)
            case "add" if amount and category and description and date:  # add new expense to db
                db.add_expense(amount, category, description, date)

    sort_by = request.form.get("sort")    
    if sort_by:
        expenses = db.get_expenses(sort_by)
    else:
        expenses = db.get_expenses() # get all expenses from db
    return render_template("home.html", expenses=expenses)

@app.route("/download_csv")
def download_csv():
    csv_file = db.convert_to_csv()
    return send_file(csv_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)