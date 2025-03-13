from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__, template_folder='.')
app.secret_key = "your_secret_key" 

def get_db_connection(): # to connect the database 
    try:
        return mysql.connector.connect(
            host="localhost",
            user="Teslim",
            password="Tesleem@123",
            database="mydatabase"
        )
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def add_expenses(name, expense_type, account, category, description, amount, quantity): 
    # Calculate total amount
    total_amount = amount * quantity

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO transactions (name, type, account, category, description, amount, quantity, total_amount)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (name, expense_type, account, category, description, amount, quantity, total_amount)
            cursor.execute(query, values)
            conn.commit()
            print("Expense added successfully!")
        except mysql.connector.Error as e:
            print(f"Error inserting expense: {e}")
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

@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    if request.method == 'POST':
        name = request.form['name']
        expense_type = request.form['expense_type']
        account = request.form['account']
        category = request.form['category']
        description = request.form['description']
        amount = float(request.form['amount'])
        quantity = int(request.form['quantity'])
        add_expenses(name, expense_type, account, category, description, amount, quantity)
        flash("Expense added successfully!", "success")
        return redirect(url_for('expenses'))
    return render_template('expenses.html')

@app.route('/total_expenses')
def total_expenses():
    total = sum_total_expenses()
    return render_template('Total_expenses.html', total=total)

if __name__ == '__main__':
    app.run(debug=True)
