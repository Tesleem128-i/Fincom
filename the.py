from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__, template_folder='.')

# Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="Teslim",
        password="Tesleem@123",
        database="mydatabase"
    )

# Dashboard Route
@app.route('/')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('home.html', transactions=transactions)

# Route to Handle Adding Transactions
@app.route('/add', methods=['POST'])
def add_transaction():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    user_id = request.form['user_id']
    category = request.form['category']
    payment_mode = request.form['payment_mode']
    role = request.form['role']
    type_ = request.form['type']
    amount = request.form['amount']
    date = request.form['date']

    cursor.execute("""
        INSERT INTO transactions (user_id, category, payment_mode, role, type, amount, date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (user_id, category, payment_mode, role, type_, amount, date))

    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('dashboard'))

# Route to Handle Deleting Transactions
@app.route('/delete/<int:id>')
def delete_transaction(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
