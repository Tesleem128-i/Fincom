from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
from mysql.connector import Error
from flask_bcrypt import Bcrypt
import re
from flask_mail import Mail, Message
import random

app = Flask(__name__, template_folder='.')
bcrypt = Bcrypt(app)
app.secret_key = "your_secret_key"


# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'projectfinodido@gmail.com'  # Your email address
app.config['MAIL_PASSWORD'] = 'csqv yavo jcwj bghz'  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = 'projectfinodido@gmail.com'  # Default sender

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
        nationality = request.form['Nationality']
        customer_type = request.form['customer_type']

        # Check if all required fields are filled
        if not username or not email or not password or not customer_type:
            flash("All fields are required!", "error")
            return redirect('/signup')

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect('/signup')

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
                        session['user_id'] = user['id']
                        session['username'] = user['username']
                        session['customer_type'] = user['customer_type']

                        flash("Login successful!", "success")

                        # Trim and check customer type
                        if user['customer_type'].strip().lower() == 'individual':
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

        return redirect('/login')

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
@app.route('/home')
def home():
    if 'username' in session:
        username = session['username']
        customer_type = session['customer_type']

        # Customize the welcome message based on the customer_type
        if customer_type == 'individual':
            welcome_message = f"Welcome, {username}! We're glad to have you here."
        elif customer_type == 'family':
            welcome_message = f"Welcome, {username}! Your family is important to us."
        elif customer_type == 'company':
            welcome_message = f"Welcome, {username}! Thank you for choosing us for your business needs."
        else:
            welcome_message = "Welcome!"

        return render_template('home.html', message=welcome_message)
    else:
        flash("You need to log in first!", "error")
        return redirect('/login')

@app.route('/home1')
def home1():
    if 'username' in session:
        username = session['username']
        customer_type = session['customer_type']

        # Customize the welcome message based on the customer_type
        if customer_type == 'individual':
            welcome_message = f"Welcome, {username}! We're glad to have you here."
        elif customer_type == 'family':
            welcome_message = f"Welcome, {username}! Your family is important to us."
        elif customer_type == 'company':
            welcome_message = f"Welcome, {username}! Thank you for choosing us for your business needs."
        else:
            welcome_message = "Welcome!"

        return render_template('home.html', message=welcome_message)
    else:
        flash("You need to log in first!", "error")
        return redirect('/login')
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)