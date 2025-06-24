from flask import Flask, request, render_template, send_file, url_for, make_response, redirect, jsonify
import jwt
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone, timedelta
from functools import wraps
import Database as db

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'

db = db.Database()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('jwt_token')

        if not token:
            return jsonify({'message': 'Token is missing'}), 404
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = db.find_user(data['public_id'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/')
@app.route('/login', methods=["GET","POST"])
def login():
    msg = ''
    if request.method == "POST":
        # grab data
        name = request.form['username']
        password = request.form['password']
        user = db.find_user(name)

        if not user or not check_password_hash(user[0][3], password):
            msg = "Invalid email or password"
            return render_template('login.html', msg = msg)

        token = jwt.encode({'public_id': user[0][1], 'exp': datetime.now(timezone.utc) + timedelta(hours=1)},
                            app.config['SECRET_KEY'], algorithm="HS256")

        response = make_response(redirect(url_for('home')))
        response.set_cookie('jwt_token', token)

        return response

    return render_template('login.html', msg = msg)

@app.route('/signup', methods=["GET","POST"])
def signup():
    msg = ''
    if request.method == "POST":
        # Grab data from the form
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # See if user exists
        existing_user = db.find_by_email(email)
        if existing_user:
            msg = 'User already exists. Please login.'
            return render_template('signup.html', msg = msg)
        
        # Hash password for security
        hashed_password = generate_password_hash(password)

        # add user to db
        db.add_new_user(str(uuid.uuid4()), name, hashed_password, email)

        # Redirect to login page to login
        return redirect(url_for('login'))


    return render_template('signup.html', msg = msg)

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