from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
from mysql.connector import Error
from flask_bcrypt import Bcrypt
import re
from flask_mail import Mail, Message
import random
from itsdangerous import URLSafeTimedSerializer


app = Flask(__name__, template_folder='template', static_folder='static')
bcrypt = Bcrypt(app)
app.secret_key = "your_secret_key"


# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'projectfinodido@gmail.com'  # Your email address
app.config['MAIL_PASSWORD'] = 'csqv yavo jcwj bghz'  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = 'FINCOM'  # Default sender

mail = Mail(app)
def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="Teslim",
            password="Tesleem@123",
            database="mydatabase"
        )
    except Error as e:
        print(f"Error connecting to database: {e}")
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

        # Check if all required fields are filled
        if not username or not email or not password or not customer_type:
            flash("All fields are required!", "error")
            return redirect('/signup')

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect('/signup')
        
        bcrypt = Bcrypt()
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                # Check if the username or email already exists
                cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
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
                    'pin': pin
                }

                flash("A verification PIN has been sent to your email. Please check your inbox.", "success")
                return redirect('/verify_pin')
            except Error as e:
                print(f"An error occurred: {e}")
                flash("An error occurred while signing up. Please try again.", "error")
            finally:
                cursor.close()
                conn.close()
        else:
            flash("Database connection failed!", "error")

    return render_template('signup.html')

@app.route('/verify_pin', methods=['GET', 'POST'])
def verify_pin():
    if request.method == 'POST':
        entered_pin = request.form['pin']
        pending_user = session.get('pending_user')

        if pending_user and str(pending_user['pin']) == entered_pin:
            # Insert new user into the database
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("""
                        INSERT INTO users (username, fullname, email, password, nationality, customer_type)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (pending_user['username'], pending_user['fullname'], pending_user['email'],
                          pending_user['password'], pending_user['nationality'], pending_user['customer_type']))
                    conn.commit()
                    flash("Signup successful! You can now log in.", "success")
                    session.pop('pending_user', None)  # Clear the pending user data
                    return redirect('/login')
                except Error as e:
                    print(f"An error occurred: {e}")
                    flash("An error occurred while signing up. Please try again.", "error")
                finally:
                    cursor.close()
                    conn.close()
            else:
                flash("Database connection failed!", "error")
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

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                user = cursor.fetchone()
                cursor.close()
            except Exception as e:
                flash("An error occurred while accessing the database.", "error")
                return render_template('forgot_password.html')
            finally:
                conn.close()

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
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # Update the user's password in the database
                cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_password, email))
                conn.commit()
                cursor.close()
                flash("Your password has been updated successfully.", "success")
                return render_template('login.html')  # Redirect to login page after successful reset
            except Exception as e:
                flash("An error occurred while updating the password.", "error")
            finally:
                conn.close()

    return render_template('reset_password.html', token=token)





@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()

                if user:
                    stored_password = user['password']
                    if bcrypt.check_password_hash(stored_password, password):
                        # Store user information in the session
                        session['user_id'] = user['id']
                        session['username'] = user['username']
                        session['customer_type'] = user['customer_type']

                        flash("Login successful!", "success")

                        # Redirect based on customer type
                        if user['customer_type'].lower() == 'individual':
                            return redirect('/home1')
                        else:  
                            return redirect('/home')
                    else:
                        flash("Invalid password!", "error")
                else:
                    flash("User  not found!", "error")
            except Error as e:
                flash(f"An error occurred: {e}", "error")
            finally:
                cursor.close()
                conn.close()
        else:
            flash("Database connection failed!", "error")

        return redirect('/login')  # Redirect back to login on failure

    # If the request method is GET, render the login page
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
    """Generate a welcome message based on the username and customer type."""
    if customer_type == 'individual':
        return f"Welcome, {username}! We're glad to have you here."
    elif customer_type == 'family':
        return f"Welcome, {username}! Your family is important to us."
    elif customer_type == 'company':
        return f"Welcome, {username}! Thank you for choosing us for your business needs."
    else:
        return "Welcome!"

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
        return redirect('/login')  # Redirect to login instead of rendering the login page

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    user_id = session.get('user_id')

    try:
        cursor.execute("""
            SELECT 
                COALESCE(SUM(CASE WHEN t.transaction_type = 'cash' THEN t.amount ELSE 0 END), 0) AS cash_balance,
                COALESCE(SUM(CASE WHEN t.transaction_type = 'card' THEN t.amount ELSE 0 END), 0) AS card_balance
            FROM 
                transactions t 
            WHERE 
                t.user_id = %s;
        """, (user_id,))
        
        balance = cursor.fetchone()

        # Determine home page dynamically
        customer_type = session.get("customer_type", "individual").lower()
        user_home = "home1" if customer_type == "individual" else "home"

        return render_template('balances.html', balance=balance, user_home=user_home)

    except Error as e:
        flash(f"An error occurred: {e}", "error")
        return redirect('/error')  
    
    finally:
        cursor.close()  # Close the cursor
        conn.close() 


def add_expenses(submitter_name, expense_type, account, category, description, amount, quantity):
    total_amount = amount * quantity
    conn = get_db_connection()

    if conn:
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO transactions (name, type, account, category, description, amount, quantity, total_amount)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (submitter_name, expense_type, account, category, description, amount, quantity, total_amount)
            cursor.execute(query, values)

            if account == 'cash':
                cursor.execute("""
                    UPDATE users
                    SET cash_balance = cash_balance - %s,
                        total_expenses = total_expenses + %s
                    WHERE username = %s
                """, (total_amount, total_amount, submitter_name))
            elif account == 'card':
                cursor.execute("""
                    UPDATE users
                    SET card_balance = card_balance - %s,
                        total_expenses = total_expenses + %s
                    WHERE username = %s
                """, (total_amount, total_amount, submitter_name))

            conn.commit()
            update_profit(submitter_name)  # Update profit after expense update
            print("Expense added and balances updated successfully!")
        except mysql.connector.Error as e:
            print(f"Error inserting expense or updating balances: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

def sum_total_expenses():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT SUM(total_amount) FROM expenses")
            total = cursor.fetchone()[0]
            return total if total is not None else 0
        except mysql.connector.Error as e:
            print(f"Error calculating total expenses: {e}")
            return 0
        finally:
            cursor.close()
            conn.close()

from flask import session

@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    if request.method == 'POST':
        try:
            # Retrieve the user's name from the session
            submitter_name = session.get('username')  # Assuming 'username' is stored in the session
            if not submitter_name:
                flash("User  not logged in. Please log in to add expenses.", "error")
                return redirect('/login')  # Redirect to login if not logged in

            expense_type = request.form['expense_type']
            account = request.form['account']
            category = request.form['category']
            description = request.form['description']
            amount = float(request.form['amount'])
            quantity = float(request.form['quantity'])

            # Call the function to add expenses
            add_expenses(submitter_name, expense_type, account, category, description, amount, quantity)

            flash("Expense added successfully!", "success")
            

        except KeyError as e:
            flash(f"Missing field: {str(e)}", "error")
        except ValueError:
            flash("Please enter valid numeric values for amount and quantity.", "error")
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")

    return render_template('expenses.html')

  # Redirect to user list page

    

@app.route('/total_expenses')
def total_expenses():
    total = sum_total_expenses()
    return render_template('Total_expenses.html', total=total)




def add_income(submitter_name, income_type, account, category, description, amount, quantity):
    total_amount = amount * quantity
    conn = get_db_connection()

    if conn:
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO transactions (name, type, account, category, description, amount, quantity, total_amount)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (submitter_name, income_type, account, category, description, amount, quantity, total_amount)
            cursor.execute(query, values)

            if account == 'cash':
                cursor.execute("""
                    UPDATE users
                    SET cash_balance = cash_balance + %s,
                        total_income = total_income + %s
                    WHERE username = %s
                """, (total_amount, total_amount, submitter_name))
            elif account == 'card':
                cursor.execute("""
                    UPDATE users
                    SET card_balance = card_balance + %s,
                        total_income = total_income + %s
                    WHERE username = %s
                """, (total_amount, total_amount, submitter_name))

            conn.commit()
            update_profit(submitter_name)  # Update profit after income update
            print("Income added and balances updated successfully!")
        except mysql.connector.Error as e:
            print(f"Error inserting income or updating balances: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
            

# Function to calculate total income
def sum_total_income():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT SUM(total_amount) FROM transactions")  # Correct table name
            total = cursor.fetchone()[0]
            return total if total is not None else 0
        except mysql.connector.Error as e:
            print(f"Error calculating total income: {e}")
            return 0
        finally:
            cursor.close()
            conn.close()

# Route to handle income submission
@app.route('/income', methods=['GET', 'POST'])
def income():
    if request.method == 'POST':
        try:
            # Retrieve the user's name from the session
            submitter_name = session.get('username')  # Assuming 'username' is stored in the session
            if not submitter_name:
                flash("User not logged in. Please log in to add income.", "error")
                return redirect(url_for('login'))  # Redirect to login if not logged in

            income_type = request.form['income_type']
            account = request.form['account']
            category = request.form['category']
            description = request.form['description']
            amount = float(request.form['amount'])
            quantity = float(request.form['quantity'])

            # Call the function to add income
            add_income(submitter_name, income_type, account, category, description, amount, quantity)

            flash("Income added successfully!", "success")
            return redirect(url_for('income'))  # Redirect to avoid form resubmission

        except KeyError as e:
            flash(f"Missing field: {str(e)}", "error")
        except ValueError:
            flash("Please enter valid numeric values for amount and quantity.", "error")
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")

    return render_template('income.html')

# Route to display total income
@app.route('/total_income')
def total_income():
    total = sum_total_income()
    return render_template('Total_income.html', total=total)


def update_profit(username):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE users 
                SET profit = (total_income - total_expenses) 
                WHERE username = %s
            """, (username,))
            conn.commit()
        except mysql.connector.Error as e:
            print(f"Error updating profit: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
            
def get_profit():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT SUM(profit) FROM users")
            profit = cursor.fetchone()[0]
            return profit if profit is not None else 0
        except mysql.connector.Error as e:
            print(f"Error calculating profit: {e}")
            return 0
        finally:
            cursor.close()
            conn.close()            

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)

