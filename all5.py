from flask import Flask, render_template, request, redirect, session, flash, jsonify
import mysql.connector
from mysql.connector import Error
from flask_bcrypt import Bcrypt
import sqlite3
import re
from flask_mail import Mail, Message
import random
from itsdangerous import URLSafeTimedSerializer


app = Flask(__name__, template_folder='template', static_folder='static')
bcrypt = Bcrypt(app)
app.secret_key = "your_secret_key"


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'projectfinodido@gmail.com'  # Your email address
app.config['MAIL_PASSWORD'] = 'csqv yavo jcwj bghz'  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = 'FINCOM'  # 


mail = Mail(app)
def get_db_connection():
    """Establish a connection to the SQLite database with error handling."""
    try:
        conn = sqlite3.connect("mydatabase.db")
        conn.row_factory = sqlite3.Row  # Allows accessing columns by name
        print("Database connection established.")
        return conn
    except sqlite3.Error as e:
        print(f"Database connection failed: {e}")
        return None
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        nationality = request.form['nationality']
        customer_type = request.form['customer_type']
        currency = request.form['currency']

        # Check if all required fields are filled
        if not username or not email or not password or not customer_type or not currency:
            flash("All fields are required!", "error")
            return redirect('/signup')

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect('/signup')

        bcrypt = Bcrypt()
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()

        try:
            # Check if the username or email already exists
            cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
            existing_user = cursor.fetchone()
            if existing_user:
                flash("Username or email already exists!", "error")
                return redirect('/signup')

            # Generate a verification PIN
            pin = random.randint(100000, 999999)

            # Send the verification email
            msg = Message("Email Verification", recipients=[email])
            msg.body = f"Your verification PIN is: {pin}"
            mail.send(msg)

            # Store user data temporarily (you may want to store it in a session or database)
            session['pending_user'] = {
                'username': username,
                'fullname': fullname,
                'email': email,
                'password': hashed_password,
                'nationality': nationality,
                'customer_type': customer_type,
                'currency': currency,
                'pin': pin
            }

            flash("A verification PIN has been sent to your email. Please check your inbox.", "success")
            return redirect('/verify_pin')

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            flash("An error occurred while signing up. Please try again.", "error")
        
        finally:
            cursor.close()
            conn.close()

    return render_template('signup.html')



@app.route('/verify_pin', methods=['GET', 'POST'])
def verify_pin():
    if request.method == 'POST':
        entered_pin = request.form['pin']
        pending_user = session.get('pending_user')

        if pending_user and str(pending_user['pin']) == entered_pin:
            # Insert new user into the database
            conn = sqlite3.connect("mydatabase.db")
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO users (username, fullname, email, password, nationality, customer_type)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (pending_user['username'], pending_user['fullname'], pending_user['email'],
                      pending_user['password'], pending_user['nationality'], pending_user['customer_type']))
                conn.commit()
                flash("Signup successful! You can now log in.", "success")
                session.pop('pending_user', None)  # Clear the pending user data
                return redirect('/login')
            except sqlite3.Error as e:
                print(f"An error occurred: {e}")
                flash("An error occurred while signing up. Please try again.", "error")
            finally:
                cursor.close()
                conn.close()
        else:
            flash("Invalid PIN. Please try again.", "error")

    return render_template('verify_pin.html')

from itsdangerous import URLSafeTimedSerializer

# Flask-Mail Configuration (Already in your code)
app.config['MAIL_DEFAULT_SENDER'] = 'projectfinodido@gmail.com'

# Serializer for token generation
serializer = URLSafeTimedSerializer(app.secret_key)


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        try:
            conn = sqlite3.connect("mydatabase.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            conn.close()
        except Exception as e:
            flash("An error occurred while accessing the database.", "error")
            return render_template('forgot_password.html')

        if user:
            # Generate a secure token
            token = serializer.dumps(email, salt='password-reset')

            # Create reset link
            reset_url = f"http://127.0.0.1:5000/reset_password/{token}"

            # Send reset link via email
            msg = Message("Password Reset Request", recipients=[email])
            msg.body = f"Click the link below to reset your password:\n\n{reset_url}\n\nThis link expires in 10 minutes."

            try:
                mail.send(msg)
                flash("A password reset link has been sent to your email.", "success")
            except Exception as e:
                flash("Failed to send email. Please try again later.", "error")
        else:
            flash("No account found with that email!", "error")

    return render_template('forgot_password.html')


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        # Verify the token
        email = serializer.loads(token, salt='password-reset', max_age=600)  # 10 minutes expiration
    except Exception as e:
        flash("The password reset link is invalid or has expired.", "error")
        return render_template('forgot_password.html')

    if request.method == 'POST':
        new_password = request.form['new_password']
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')  # Hash the new password
        
        try:
            conn = sqlite3.connect("mydatabase.db")
            cursor = conn.cursor()
            # Update the user's password in the database
            cursor.execute("UPDATE users SET password = ? WHERE email = ?", (hashed_password, email))
            conn.commit()
            cursor.close()
            conn.close()
            flash("Your password has been updated successfully.", "success")
            return redirect('/login')  # Redirect to login page after successful reset
        except Exception as e:
            flash("An error occurred while updating the password.", "error")

    return render_template('reset_password.html', token=token)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = sqlite3.connect("mydatabase.db")
            cursor = conn.cursor()
            
            # Query user by username
            cursor.execute("SELECT id, username, password, customer_type FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

            if user:
                user_id, db_username, stored_password, customer_type = user
                if bcrypt.check_password_hash(stored_password, password):
                    # Store user info in session
                    session['user_id'] = user_id
                    session['username'] = db_username
                    session['customer_type'] = customer_type

                    flash("Login successful!", "success")

                    # Redirect based on customer type
                    return redirect('/home1' if customer_type.lower() == 'individual' else '/home')
                else:
                    flash("Invalid password!", "error")
            else:
                flash("User not found!", "error")

        except sqlite3.Error as e:
            flash(f"An error occurred: {e}", "error")
        finally:
            cursor.close()
            conn.close()

        return redirect('/login')  # Redirect back to login on failure

    # Render the login page for GET requests
    return render_template('login.html')


@app.route('/some_action')
def some_action():
    return "You chose Action 1!"

@app.route('/another_action')
def another_action():
    return "You chose Action 2!"

@app.route('/yet_another_action')
def yet_another_action():
    return "You chose Action 3!"

def generate_welcome_message(username, customer_type):
    if customer_type.lower() == "individual":
        return f"Welcome, {username}! Enjoy your personal finance dashboard."
    else:
        return f"Welcome, {username}! Manage your business transactions efficiently."

    
@app.route('/home')
def home():
    if 'username' in session:
        username = session['username']
        customer_type = session['customer_type']
        welcome_message = generate_welcome_message(username, customer_type)
        return render_template('home.html', message=welcome_message)
    else:
        flash("You need to log in first!", "error")
        return redirect('/login')

@app.route('/home1')
def home1():
    if 'username' in session:
        username = session['username']
        customer_type = session['customer_type']
        welcome_message = generate_welcome_message(username, customer_type)
        return render_template('home1.html', message=welcome_message)  # Render a different template for home1
    else:
        flash("You need to log in first!", "error")
        return redirect('/login')
@app.route('/balances')
def balances():
    if 'user_id' not in session:
        flash("Please log in to view your balance.", "error")
        return redirect('/login')

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row  # Enables dictionary-like access
    cursor = conn.cursor()

    user_id = session.get('user_id')

    try:
        cursor.execute("""
            SELECT 
                COALESCE(SUM(CASE WHEN t.transaction_type = 'cash' THEN t.amount ELSE 0 END), 0) AS cash_balance,
                COALESCE(SUM(CASE WHEN t.transaction_type = 'card' THEN t.amount ELSE 0 END), 0) AS card_balance
            FROM 
                transactions t 
            WHERE 
                t.user_id = ?;
        """, (user_id,))
        
        balance = cursor.fetchone()

        # Convert SQLite Row to dictionary
        balance_dict = dict(balance) if balance else {"cash_balance": 0, "card_balance": 0}

        # Determine home page dynamically
        customer_type = session.get("customer_type", "individual").lower()
        user_home = "home1" if customer_type == "individual" else "home"

        return render_template('balances.html', balance=balance_dict, user_home=user_home)

    except sqlite3.Error as e:
        flash(f"An error occurred: {e}", "error")
        return redirect('/error')  
    
    finally:
        cursor.close()
        conn.close()
        
def get_db_connection():
    """Establish a connection to the SQLite database with error handling."""
    try:
        conn = sqlite3.connect("mydatabase.db")
        conn.row_factory = sqlite3.Row  # Allows accessing columns by name
        return conn
    except sqlite3.Error as e:
        print(f"Database connection failed: {e}")
        return None


def get_db_connection():
    return sqlite3.connect('mydatabase.db')

def update_profit(username):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE users 
                SET profit = COALESCE(total_income, 0) - COALESCE(total_expenses, 0) 
                WHERE username = ?
            """, (username,))
            conn.commit()

            # Fetch user currency
            cursor.execute("SELECT currency FROM users WHERE username = ?", (username,))
            user_currency = cursor.fetchone()
            if user_currency:
                print(f"Updated profit for {username} in {user_currency[0]}")

        except sqlite3.Error as e:
            print(f"Error updating profit: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()


def add_expenses(submitter_name, expense_type, account, category, description, amount, quantity):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Fetch the user_id and currency based on the username
            cursor.execute("SELECT id, currency FROM users WHERE username = ?", (submitter_name,))
            user_row = cursor.fetchone()
            if not user_row:
                flash("User not found. Please log in again.", "error")
                return
            user_id, currency = user_row

            # Calculate total amount
            total_amount = amount * quantity

            # Insert expense with user_id and currency
            cursor.execute("""
                INSERT INTO transactions (user_id, name, type, account, category, description, amount, quantity, currency)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, submitter_name, expense_type, account, category, description, amount, quantity, currency))

            # Update user balance
            balance_column = f"{account}_balance"
            cursor.execute(f"""
                UPDATE users
                SET {balance_column} = COALESCE({balance_column}, 0) - ?,
                    total_expenses = COALESCE(total_expenses, 0) + ?
                WHERE id = ?
            """, (total_amount, total_amount, user_id))

            conn.commit()
            flash(f"Expense added successfully in {currency}!", "success")

        except sqlite3.Error as e:
            flash(f"Error inserting expense: {e}", "error")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    if request.method == 'POST':
        try:
            submitter_name = session.get('username')
            if not submitter_name:
                flash("User not logged in. Please log in to add expenses.", "error")
                return redirect('/login')

            expense_type = request.form['expense_type']
            account = request.form['account']
            category = request.form['category']
            description = request.form['description']
            amount = float(request.form['amount'])
            quantity = float(request.form['quantity'])

            add_expenses(submitter_name, expense_type, account, category, description, amount, quantity)

            return redirect('/home1')

        except (KeyError, ValueError):
            flash("Please fill in all fields correctly.", "error")
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")

    return render_template('expenses.html')

# Function to calculate total expenses grouped by currency
def sum_total_expenses():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT currency, COALESCE(SUM(amount * quantity), 0) 
                FROM transactions WHERE type='expense' 
                GROUP BY currency
            """)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error calculating total expenses: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

@app.route('/total_expenses')
def total_expenses():
    return render_template('total_expenses.html', total=sum_total_expenses())


# Function to add an income
def add_income(submitter_name, income_type, account, category, description, amount, quantity):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Fetch the user_id and currency based on the username
            cursor.execute("SELECT id, currency FROM users WHERE username = ?", (submitter_name,))
            user_row = cursor.fetchone()
            if not user_row:
                flash("User not found. Please log in again.", "error")
                return
            user_id, currency = user_row

            # Calculate total amount
            total_amount = amount * quantity

            # Insert income with user_id and currency
            cursor.execute("""
                INSERT INTO transactions (user_id, name, type, account, category, description, amount, quantity, currency)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, submitter_name, income_type, account, category, description, amount, quantity, currency))

            # Update user balance
            balance_column = f"{account}_balance"
            cursor.execute(f"""
                UPDATE users
                SET {balance_column} = COALESCE({balance_column}, 0) + ?,
                    total_income = COALESCE(total_income, 0) + ?
                WHERE id = ?
            """, (total_amount, total_amount, user_id))

            conn.commit()
            flash(f"Income added successfully in {currency}!", "success")

        except sqlite3.Error as e:
            flash(f"Error inserting income: {e}", "error")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

@app.route('/income', methods=['GET', 'POST'])
def income():
    if request.method == 'POST':
        try:
            submitter_name = session.get('username')
            if not submitter_name:
                flash("User not logged in. Please log in to add income.", "error")
                return redirect('/login')

            income_type = request.form['income_type']
            account = request.form['account']
            category = request.form['category']
            description = request.form['description']
            amount = float(request.form['amount'])
            quantity = float(request.form['quantity'])

            add_income(submitter_name, income_type, account, category, description, amount, quantity)

            return redirect('/home1')

        except (KeyError, ValueError):
            flash("Please fill in all fields correctly.", "error")
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")

    return render_template('income.html')

# Function to calculate total income grouped by currency
def sum_total_income():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT currency, COALESCE(SUM(amount * quantity), 0) 
                FROM transactions WHERE type='income' 
                GROUP BY currency
            """)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error calculating total income: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

@app.route('/total_income')
def total_income():
    return render_template('total_income.html', total=sum_total_income())




def get_db_connection():
    """Establish a connection to the SQLite database with error handling."""
    try:
        conn = sqlite3.connect("mydatabase.db")
        conn.row_factory = sqlite3.Row  # Allows accessing columns by name
        return conn
    except sqlite3.Error as e:
        print(f"Database connection failed: {e}")
        return None

def update_profit(user_id):
    """Calculate and update profit based on transactions for a user."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Calculate total income grouped by currency
            cursor.execute("""
                SELECT currency, COALESCE(SUM(amount), 0) FROM transactions 
                WHERE user_id = ? AND type = 'income' 
                GROUP BY currency;
            """, (user_id,))
            income_results = cursor.fetchall()
            total_income = {currency: amount for currency, amount in income_results}
            
            # Calculate total expenses grouped by currency
            cursor.execute("""
                SELECT currency, COALESCE(SUM(amount), 0) FROM transactions 
                WHERE user_id = ? AND type = 'expense' 
                GROUP BY currency;
            """, (user_id,))
            expense_results = cursor.fetchall()
            total_expenses = {currency: amount for currency, amount in expense_results}

            # Calculate profit for each currency
            profit_by_currency = {currency: total_income.get(currency, 0) - total_expenses.get(currency, 0) 
                                  for currency in set(total_income) | set(total_expenses)}
            
            # Update the users table with the calculated profit (assuming a column per currency or JSON storage)
            for currency, profit in profit_by_currency.items():
                cursor.execute("UPDATE users SET profit = ? WHERE id = ?", (profit, user_id))
            
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating profit: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

@app.route('/get_profit')
def profit_page():
    """Display the profit for the logged-in user."""
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to view profit.", "error")
        return redirect('/login')

    # Update profit before fetching
    update_profit(user_id)

    conn = get_db_connection()
    if conn is None:
        return "Database connection error", 500

    cursor = conn.cursor()
    try:
        # Fetch the updated profit grouped by currency
        cursor.execute("SELECT currency, COALESCE(profit, 0) FROM users WHERE id = ?", (user_id,))
        results = cursor.fetchall()
        profit_by_currency = {currency: float(profit) for currency, profit in results}

        return render_template("get_profit.html", total_profit=profit_by_currency)
    except sqlite3.Error as e:
        print(f"Error fetching profit: {e}")
        return "Database error", 500
    finally:
        cursor.close()
        conn.close()

        
        


# Business suggestion function
def suggest_business(capital, currency):
    businesses = {
        f"Very Low Budget (1 - 100 {currency})": [
            ("Dropshipping", "video1.mp4"),
            ("Freelance Writing", "writing.mp4"),
            ("Affiliate Marketing", "affiliate.mp4"),
            ("Social Media Management", "smm.mp4"),
            ("Tutoring", "tutoring.mp4"),
            ("Print-on-Demand", "printondemand.mp4"),
            ("Handmade Crafts", "handmade.mp4"),
        ],
        f"Low Budget (100 - 500 {currency})": [
            ("Mini Importation", "importation.mp4"),
            ("Local Snacks Business", "snacks.mp4"),
            ("Digital Marketing Agency", "digitalmarketing.mp4"),
            ("Graphic Design Services", "graphicdesign.mp4"),
            ("Car Wash Business", "carwash.mp4"),
            ("Online Course Selling", "onlinecourse.mp4"),
        ],
        f"Lower Medium Budget (500 - 2000 {currency})": [
            ("E-commerce Store", "ecommerce.mp4"),
            ("Photography/Videography", "photography.mp4"),
            ("Laundry Business", "laundry.mp4"),
            ("Clothing Brand", "clothing.mp4"),
            ("Barbershop or Salon Business", "barbershop.mp4"),
            ("Food Business", "food.mp4"),
        ],
        f"Upper Medium Budget (2000 - 5000 {currency})": [
            ("Small Scale Farming", "farming.mp4"),
            ("Car Rental Service", "carrental.mp4"),
            ("Tech Repairs & Services", "techrepair.mp4"),
            ("Cyber Café or Gaming Center", "gaming.mp4"),
            ("Event Planning & Rentals", "eventplanning.mp4"),
        ],
        f"Lower High Budget (5000 - 10,000 {currency})": [
            ("Logistics/Delivery Business", "logistics.mp4"),
            ("Fitness & Gym Center", "gym.mp4"),
            ("Real Estate Investment", "realestate.mp4"),
            ("Printing & Branding Business", "printing.mp4"),
            ("Mini Supermarket", "supermarket.mp4"),
        ],
        f"Upper High Budget (10,000 - 20,000 {currency})": [
            ("Import/Export Business", "importexport.mp4"),
            ("Restaurant & Lounge", "restaurant.mp4"),
            ("Auto Dealership", "autodealership.mp4"),
            ("Online Marketplace", "marketplace.mp4"),
            ("Tech Startup", "techstartup.mp4"),
        ],
        f"Very High Budget (20,000+ {currency})": [
            ("Large-Scale Real Estate", "largerealestate.mp4"),
            ("Hotel Business", "hotel.mp4"),
            ("Manufacturing", "manufacturing.mp4"),
            ("Automobile Dealership", "automobile.mp4"),
            ("Private School Business", "privateschool.mp4"),
        ],
    }

    if capital < 100:
        category = f"Very Low Budget (1 - 100 {currency})"
    elif 100 <= capital < 500:
        category = f"Low Budget (100 - 500 {currency})"
    elif 500 <= capital < 2000:
        category = f"Lower Medium Budget (500 - 2000 {currency})"
    elif 2000 <= capital < 5000:
        category = f"Upper Medium Budget (2000 - 5000 {currency})"
    elif 5000 <= capital < 10000:
        category = f"Lower High Budget (5000 - 10,000 {currency})"
    elif 10000 <= capital < 20000:
        category = f"Upper High Budget (10,000 - 20,000 {currency})"
    else:
        category = f"Very High Budget (20,000+ {currency})"

    return category, businesses[category]

@app.route("/Business_advice", methods=["GET", "POST"])
def Business_advice():
    if request.method == "POST":
        user_id = session.get('user_id')
        if not user_id:
            flash("Please log in to get business advice.", "error")
            return redirect('/login')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT currency FROM users WHERE id = ?", (user_id,))
        user_currency = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not user_currency:
            return render_template("Business_advice.html", error="User currency not found.")
        user_currency = user_currency[0]

        capital_input = request.form.get("capital")  # Use get to avoid KeyError
        if capital_input:
            try:
                capital = float(capital_input)
                if capital < 0:
                    return render_template("Business_advice.html", error="Capital cannot be negative.")
                
                category, suggestions = suggest_business(capital, user_currency)
                return render_template("result.html", category=category, suggestions=suggestions)
            except ValueError:
                return render_template("Business_advice.html", error="Please enter a valid amount.")
        else:
            return render_template("Business_advice.html", error="Please enter a capital amount.")

    return render_template("Business_advice.html")




@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)