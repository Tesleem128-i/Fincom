import sqlite3

def init_db():
    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()

    # Create the users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            fullname TEXT,
            profession TEXT,
            email TEXT UNIQUE,
            password TEXT,
            nationality TEXT,
            customer_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create the workers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            worker_name TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    init_db()  # Call the function to initialize the database
    
    
import sqlite3

def add_company_id_column():
    # Connect to the SQLite database
    conn = sqlite3.connect('mydatabase.db')  # Replace 'mydatabase.db' with your database name
    cursor = conn.cursor()

    # SQL command to add the company_id column
    add_column_query = """
    ALTER TABLE workers
    ADD COLUMN company_id INTEGER;
    """

    try:
        # Execute the SQL command
        cursor.execute(add_column_query)
        print("Column 'company_id' added successfully to the 'workers' table.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Commit changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()

# Call the function to add the company_id column
add_company_id_column()