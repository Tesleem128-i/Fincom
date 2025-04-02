import sqlite3

def create_budgets_table():
    # Connect to the SQLite database
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()

    # SQL command to create the budgets table
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category TEXT,
        amount REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    '''

    try:
        # Execute the SQL command
        cursor.execute(create_table_query)
        print("Budgets table created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while creating the budgets table: {e}")
    finally:
        # Commit changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()

# Call the function to create the table
create_budgets_table()