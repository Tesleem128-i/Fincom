import sqlite3

def run_sql_commands():
    # Connect to the SQLite database
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    # Example SQL command to create a table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        account TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        amount REAL NOT NULL,
        quantity INTEGER NOT NULL,
        total_amount REAL GENERATED ALWAYS AS (amount * quantity) STORED
    );
    """

    try:
        cursor.execute(create_table_sql)
        conn.commit()
        print("Table created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

# Run the function
run_sql_commands()
